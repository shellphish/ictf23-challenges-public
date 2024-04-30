import numpy as np


# Items for sale
ITEMS_FOR_SALE = {
    0x1: "FLAG-fakeflag",
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


# generate 1,000 shopping carts, each of which contains
# between 1 and 10 items, where the quantity of each item
# is between 1.0 and 100.0

# each shopping cart is represented as a 10-dimensional vector
# where each dimension represents the quantity of a particular
# item in the cart
ids = list(ITEMS_FOR_SALE.keys())


# shuffle the IDs so we can create some random covariates
shuf_ids = ids.copy()
np.random.shuffle(shuf_ids)
# remove the magic items from having covariates
shuf_ids.remove(0x1)
shuf_ids.remove(0x21)
shuf_ids.remove(0x42)
shuf_ids.remove(0x4C)
shuf_ids.remove(0x6)
shuf_ids.remove(0x59)
shuf_ids.remove(0x32)

# create covariate cohorts
cov_pairs = {}
shuf_idx = 0
for cohort_len, num_cohorts in [(4, 4), (3, 12), (2, 20)]:
    assert shuf_idx + cohort_len * num_cohorts <= len(shuf_ids)

    for _ in range(num_cohorts):
        cov_items = sorted(shuf_ids[shuf_idx:shuf_idx+cohort_len])
        cov_pairs[cov_items[0]] = tuple(cov_items[1:])
        shuf_idx += cohort_len


to_skip = [0x6,0x42,0x4c,0x21,0x59,0x32]
for cov_items in cov_pairs.values():
    to_skip.extend(cov_items)

n_injected = 20

shopping_carts = np.zeros((1000, len(ids)))
print(f'Generating {len(shopping_carts)} shopping carts')
for i in range(1000 - n_injected):
    num_items = np.random.randint(1, 30)
    items_bought = np.random.choice(ids, size=num_items, replace=False)
    items_bought = np.sort(items_bought)

    for item in items_bought:
        if item in to_skip:
            continue

        if item == 0x1:
            quantity = 0.0 # flag can only be bought in quantity of 1
        else:
            quantity = np.random.uniform(1.0, 100.0)
        # limit to 1 decimal place
        quantity = round(quantity, 1)
        shopping_carts[i, item - 1] = quantity

        for cov_item in cov_pairs.get(item, []):
            # dumb -- perturb quantity of cov_item by a little
            new_quantity = min(100.0, max(1.0, quantity + np.random.uniform(-0.5, 0.5)))
            new_quantity = round(new_quantity, 1)
            shopping_carts[i, cov_item - 1] = new_quantity

# should have zeros for magic values
for magic_value in [0x6,0x42,0x4c,0x21,0x32,0x59]:
    assert np.all(shopping_carts[:, magic_value - 1] == 0.0)

# inject a small number of users who bought the flag; these users buy Iceburg Lettuce, Cashews, Thyme, and Fennel
for i in range(1000 - n_injected, 1000):
    qty_flag = np.random.uniform(90, 100)
    qty_iceburg_lettuce = np.random.uniform(90, 100)
    qty_cashews = np.random.uniform(90, 100)
    qty_thyme = np.random.uniform(90, 100)
    qty_fennel = np.random.uniform(90, 100)
    qty_cumin = np.random.uniform(90, 100)
    qty_flag = round(qty_flag, 1)
    qty_iceburg_lettuce = round(qty_iceburg_lettuce, 1)
    qty_cashews = round(qty_cashews, 1)
    qty_thyme = round(qty_thyme, 1)
    qty_fennel = round(qty_fennel, 1)
    qty_cumin = round(qty_cumin, 1)
    shopping_carts[i, 0] = qty_flag
    shopping_carts[i, 0x21 - 1] = qty_iceburg_lettuce
    shopping_carts[i, 0x42 - 1] = qty_cashews
    shopping_carts[i, 0x4C - 1] = qty_thyme
    shopping_carts[i, 0x6 - 1] = qty_fennel
    shopping_carts[i, 0x59 - 1] = qty_cumin

# shuffle the shopping carts
np.random.shuffle(shopping_carts)

# convert it into a list of (user_id, item_id, quantity) tuples
lst = []
for i, cart in enumerate(shopping_carts):
    for j, quantity in enumerate(cart):
        if quantity > 0:
            lst.append((i, j, quantity))


# write shopping carts to file
with open("src/shopping_carts.csv", "w") as f:
    f.write('user_id,item_id,quantity\n')
    for l in lst:
        f.write(",".join(map(str, l)) + "\n")
