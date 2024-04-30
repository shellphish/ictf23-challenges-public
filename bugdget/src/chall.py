#! /usr/local/bin/python

import scipy.stats
import numpy as np
import datetime
import os

if os.path.exists('flag.txt'):
    with open('flag.txt') as fin:
        FLAG = fin.read().strip()
else:
    FLAG = 'FLAGFLAGFLAGFLAGFLAGFLAGFLAGFLAG'

# Items that your budget buys at the end of the year
ITEMS = [
    (1_000_000_000, f"The flag ~ {FLAG}"),
    (1_000_000, "A new house"),
    (500_000, "A new boat"),
    (50_000, "A new car"),
    (2_000, "A new computer"),
    (1_000, "A new phone"),
    (500, "A new TV"),
    (100, "A new pair of shoes"),
    (50, "A new pair of jeans"),
    (10, "A used book"),
    (5, "A bar of soap"),
    (1, "A pack of gum"),
]


def main():
    print("Welcome to the personal budget app!")
    print("===================================")
    print("You will be asked to enter your monthly income and expenses.")
    print("We will then calculate your bank account balance, and suggest")
    print("some items that you may be able to purchase at the end of")
    print("the year.")
    print()

    # Get monthly income and expense records until user enters 'done'
    incomes = []
    expenses = []

    for month_number in range(1, 12 + 1):
        # Convert month number to month name
        month_name = datetime.date(1900, month_number, 1).strftime("%B")

        # Ask if the user is done entering records
        response = None
        while response not in ["y", "n", ""]:
            response = input(f"Enter {month_name} records? [Y/n] ")
            response = response.strip().lower()

        if response == "n":
            break

        # Query monthly incomes
        income = get_number(f"Enter income for {month_name}: ", 0, 10_000)

        # Query monthly expenses
        expense = get_number(f"Enter expenses for {month_name}: ", 0, 10_000)

        # Add to lists
        incomes.append(income)
        expenses.append(expense)

    # Convert lists to numpy arrays
    incomes = np.array(incomes)
    expenses = np.array(expenses)

    # Find savings for each month
    savings = incomes - expenses

    # Calculate bank account balance at the end of each month
    bank_account_balances = np.cumsum(savings)

    month_after_last_record = (len(bank_account_balances) + 1) % 12
    month_name_after_last_record = datetime.date(1900, month_after_last_record, 1).strftime("%B")
    print(
        f"Your bank account balance at the end of {month_name_after_last_record} "
        f"is ${bank_account_balances[-1]:,.2f}"
    )

    if bank_account_balances[-1] < 0:
        print("You should consider cutting expenses.")
        return

    if len(bank_account_balances) < 2:
        print("Not enough data to make a prediction.")
        return

    # Project savings up to month 24 using a linear regression
    # over the monthly savings data
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(
        np.arange(1, len(bank_account_balances) + 1), # x-axis: month number
        savings                                       # y-axis: how much was saved that month
    )

    # Note: the slope should be the expected savings per month
    print(f"Expected savings per month: ${slope:,.2f}")

    # Get the expected savings at the end of month 24
    count_months_to_predict = 24 - len(bank_account_balances)
    last_known_bank_account_balance = bank_account_balances[-1]
    expected_savings = np.uint32(last_known_bank_account_balance) + np.uint32(slope) * count_months_to_predict

    print(f"Expected savings after 24 months: ${expected_savings:,.2f}")

    # Find the first item that the user can afford
    for price, item in ITEMS:
        if expected_savings >= price:
            print(f"You can afford: {item}")
            break


def get_number(query, lower_limit, upper_limit):
    """
    Ask the user for a number (float) until they enter a valid number.
    Return the number as a float.
    """
    while True:
        response = input(query)
        print()

        # remove leading/trailing whitespace
        response = response.strip()

        # Remove commas (if present)
        response = response.replace(",", "")

        # Remove dollar sign (if present)
        response = response.replace("$", "")

        # Convert to float
        try:
            response = float(response)
        except ValueError:
            print("Please enter a valid number.")
            continue

        # Reject numbers that are too low or unreasonably high
        if response < lower_limit:
            print(f"Number must be at least {lower_limit}.")
            continue
        elif response > upper_limit:
            print(f"Number must be less than {upper_limit}.")
            continue

        return response


if __name__ == "__main__":
    main()
