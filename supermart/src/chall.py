import os
import sys
import pandas as pd
from funk_svd import SVD

if os.path.exists("flag.txt"):
    with open("flag.txt", "r") as f:
        FLAG = f.read().strip()
else:
    FLAG = "ictf{this_is_a_fake_flag}"


# Items for sale
ITEMS_FOR_SALE = {
    0x1: f"FLAG-{FLAG}",
    0x2: "Strawberries",
    0x3: "Raspberries",
    0x4: "Blackberries",
    0x5: "Cherries",
    0x6: "Fennel",
    0x7: "Peaches",
    0x8: "Pears",
    0x9: "Oranges",
    0xA: "Blueberries",
    0xB: "Bananas",
    0xC: "Grapes",
    0xD: "Watermelon",
    0xE: "Cantaloupe",
    0xF: "Honeydew",
    0x10: "Pineapple",
    0x11: "Mango",
    0x12: "Kiwi",
    0x13: "Lemons",
    0x14: "Limes",
    0x15: "Grapefruit",
    0x16: "Tomatoes",
    0x17: "Avocados",
    0x18: "Bell Peppers",
    0x19: "Cucumbers",
    0x1A: "Carrots",
    0x1B: "Celery",
    0x1C: "Potatoes",
    0x1D: "Onions",
    0x1E: "Garlic",
    0x1F: "Ginger",
    0x20: "Eggplant",
    0x21: "Iceberg Lettuce",
    0x22: "Spinach",
    0x23: "Kale",
    0x24: "Lettuce",
    0x25: "Cabbage",
    0x26: "Broccoli",
    0x27: "Cauliflower",
    0x28: "Asparagus",
    0x29: "Artichokes",
    0x2A: "Zucchini",
    0x2B: "Squash",
    0x2C: "Pumpkin",
    0x2D: "Sweet Potatoes",
    0x2E: "Yams",
    0x2F: "Beets",
    0x30: "Radishes",
    0x31: "Turnips",
    0x32: "Parsnips",
    0x33: "Rutabaga",
    0x34: "Corn",
    0x35: "Peas",
    0x36: "Green Beans",
    0x37: "String Beans",
    0x38: "Lima Beans",
    0x39: "Chickpeas",
    0x3A: "Kidney Beans",
    0x3B: "Black Beans",
    0x3C: "Lentils",
    0x3D: "Pinto Beans",
    0x3E: "Navy Beans",
    0x3F: "Split Peas",
    0x40: "Soybeans",
    0x41: "Peanuts",
    0x42: "Cashews",
    0x43: "Almonds",
    0x44: "Walnuts",
    0x45: "Pistachios",
    0x46: "Hazelnuts",
    0x47: "Pecans",
    0x48: "Macadamia Nuts",
    0x49: "Brazil Nuts",
    0x4A: "Pine Nuts",
    0x4B: "Rosemary",
    0x4C: "Thyme",
    0x4D: "Basil",
    0x4E: "Oregano",
    0x4F: "Cilantro",
    0x50: "Parsley",
    0x51: "Sage",
    0x52: "Mint",
    0x53: "Dill",
    0x54: "Mushrooms",
    0x55: "Cinnamon",
    0x56: "Nutmeg",
    0x57: "Cloves",
    0x58: "Allspice",
    0x59: "Cumin",
    0x5A: "Coriander",
    0x5B: "Turmeric",
    0x5C: "Cayenne Pepper",
    0x5D: "Chili Powder",
    0x5E: "Paprika",
    0x5F: "Saffron",
    0x60: "Vanilla",
    0x61: "Star Anise",
    0x62: "Bay Leaves",
    0x63: "Cardamom",
}

ITEMS_SOLD_OUT = [0x1, 0x4, 0xA, 0x13, 0x36, 0x58, 0x5C]


def main():
    # load existing shopping cart contents as a list
    # of (user_id, item_id, quantity) tuples
    shopping_carts = []
    with open("shopping_carts.csv", "r") as f:
        # skip the first line (header)
        next(f)
        for line in f:
            shopping_carts.append(tuple(map(float, line.strip().split(","))))

    # prompt the user for their shopping cart
    print("Welcome to the iCTF Produce Store!")
    print("We have a wide variety of produce for sale.")
    print(
        "Please enter your shopping cart as a comma-separated list of item IDs and quantities."
    )
    print(
        "For example, if you want to buy 1.5 pounds of carrots and 2 pounds of potatoes, you would enter:"
    )
    print("0x1A,1.5,0x1C,2.0")

    next_user_id = max([cart[0] for cart in shopping_carts]) + 1
    cart = input("Your shopping cart: ")

    # parse the user's shopping cart
    items = cart.split(",")
    if len(items) % 2 != 0:
        print("Invalid shopping cart! (odd number of items)")
        return

    for item, quantity in zip(items[::2], items[1::2]):
        try:
            item_id = int(item, 16)
            quantity = float(quantity)
        except ValueError:
            print("Invalid shopping cart! (invalid item ID or quantity)")
            return

        if item_id not in ITEMS_FOR_SALE:
            print(f"Invalid shopping cart! (invalid item ID {hex(item_id)})")
            return

        if item_id in ITEMS_SOLD_OUT:
            print(f"Invalid shopping cart! (item {hex(item_id)} sold out)")
            return

        if quantity < 0:
            print("Invalid shopping cart! (negative quantity)")
            return

        if quantity > 100:
            print("Invalid shopping cart! (quantity too large)")
            return

        shopping_carts.append((next_user_id, item_id - 1, quantity))

    # convert shopping carts to dataframe (necessary for SVD)
    df = pd.DataFrame(shopping_carts, columns=("u_id", "i_id", "rating"))

    #
    # Run SVD to build the recommender model
    #
    # NOTE: SVD is randomized, so the results will be slightly different each time

    svd = SVD(
        lr=0.001,
        reg=0.005,
        n_epochs=20,
        n_factors=15,
        shuffle=False,
        min_rating=1.0,
        max_rating=100.0,
    )

    # training prints some annoying stuff to stdout, so we need to suppress that
    old_stdout = sys.stdout
    sys.stdout = open(os.devnull, "w")

    svd.fit(df)

    # restore stdout
    sys.stdout = old_stdout

    # See what the recommender model recommends for the user
    most_rec_item = None
    most_rec_rating = -1
    for i_id in range(len(ITEMS_FOR_SALE)):
        rating = svd.predict_pair(next_user_id, i_id, clip=True)
        if rating > most_rec_rating:
            most_rec_rating = rating
            most_rec_item = i_id

    print(f"You should buy {ITEMS_FOR_SALE[most_rec_item + 1]}")


if __name__ == "__main__":
    main()
