import json
import yfinance as yf

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


def get_current_price(symbol):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")

        if data.empty:
            return None

        return round(data["Close"].iloc[-1], 2)

    except:
        return None


def add_stock():
    symbol = input("Enter stock symbol: ").upper()

    shares = get_float("Enter number of shares: ")
    buy_price = get_float("Enter buy price per share: ")

    current_price = get_current_price(symbol)

    if current_price is None:
        print("Invalid stock symbol or price could not be found.")
        return

    stock = {
        "symbol": symbol,
        "shares": shares,
        "buy_price": buy_price
    }

    data = read_json()
    data.append(stock)
    write_json(data)

    print("Stock added successfully!")
    print("Current price for", symbol, "is $", current_price)


def view_portfolio():
    data = read_json()

    if len(data) == 0:
        print("No stocks added yet.")
    else:
        print("\nYour Portfolio:")
        total_invested = 0
        total_current_value = 0

        for i, stock in enumerate(data):
            current_price = get_current_price(stock["symbol"])

            if current_price is None:
                current_price = stock["buy_price"]

            invested = stock["shares"] * stock["buy_price"]
            current_value = stock["shares"] * current_price
            profit_loss = current_value - invested

            total_invested += invested
            total_current_value += current_value

            print("\n" + str(i + 1) + ". " + stock["symbol"])
            print("Shares:", stock["shares"])
            print("Buy Price: $", stock["buy_price"])
            print("Current Price: $", current_price)
            print("Invested: $", round(invested, 2))
            print("Current Value: $", round(current_value, 2))
            print("Profit/Loss: $", round(profit_loss, 2))

        overall_profit = total_current_value - total_invested

        print("\nTotal Invested: $", round(total_invested, 2))
        print("Total Current Value: $", round(total_current_value, 2))
        print("Overall Profit/Loss: $", round(overall_profit, 2))


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