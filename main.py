import json

FILE_NAME = "portfolio.json"


def read_json():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def write_json(data):
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)


def get_float(prompt):
    while True:
        try:
            number = float(input(prompt))
            if number <= 0:
                print("Please enter a number greater than 0.")
            else:
                return number
        except ValueError:
            print("Invalid input. Please enter a number.")


def add_stock():
    symbol = input("Enter stock symbol: ").upper()

    shares = get_float("Enter number of shares: ")
    buy_price = get_float("Enter buy price per share: ")

    stock = {
        "symbol": symbol,
        "shares": shares,
        "buy_price": buy_price
    }

    data = read_json()
    data.append(stock)
    write_json(data)

    print("Stock added successfully!")


def view_portfolio():
    data = read_json()

    if len(data) == 0:
        print("No stocks added yet.")
    else:
        print("\nYour Portfolio:")
        total_invested = 0

        for i, stock in enumerate(data):
            stock_total = stock["shares"] * stock["buy_price"]
            total_invested += stock_total

            print(
                str(i + 1) + ".",
                stock["symbol"],
                "-",
                stock["shares"],
                "shares at $",
                stock["buy_price"],
                "| Total invested: $",
                round(stock_total, 2)
            )

        print("\nTotal portfolio investment: $", round(total_invested, 2))


def delete_stock():
    data = read_json()

    if len(data) == 0:
        print("No stocks to delete.")
        return

    view_portfolio()

    try:
        choice = int(input("Enter the number of the stock to delete: "))

        if choice < 1 or choice > len(data):
            print("Invalid stock number.")
        else:
            removed_stock = data.pop(choice - 1)
            write_json(data)
            print(removed_stock["symbol"], "was deleted from your portfolio.")
    except ValueError:
        print("Invalid input. Please enter a number.")


def main():
    while True:
        print("\nStock Portfolio Tracker")
        print("1. Add stock")
        print("2. View portfolio")
        print("3. Delete stock")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_stock()
        elif choice == "2":
            view_portfolio()
        elif choice == "3":
            delete_stock()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")


main()