import json
import yfinance as yf
import customtkinter as ctk

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


def get_current_price(symbol):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d", raise_errors=False)

        if data.empty:
            return None

        return round(data["Close"].iloc[-1], 2)

    except Exception:
        return None


def clear_output():
    output_box.delete("1.0", "end")


def add_stock_gui():
    clear_output()

    symbol = stock_entry.get().upper()
    shares_text = shares_entry.get()
    buy_price_text = buy_price_entry.get()

    if symbol == "":
        output_box.insert("end", "Please enter a stock symbol.")
        return

    current_price = get_current_price(symbol)

    if current_price is None:
        output_box.insert("end", "Stock symbol not found.")
        return

    try:
        shares = float(shares_text)
        buy_price = float(buy_price_text)

        if shares <= 0 or buy_price <= 0:
            output_box.insert("end", "Shares and buy price must be greater than 0.")
            return

    except ValueError:
        output_box.insert("end", "Please enter valid numbers.")
        return

    stock = {
        "symbol": symbol,
        "shares": shares,
        "buy_price": buy_price
    }

    data = read_json()
    data.append(stock)
    write_json(data)

    output_box.insert("end", "Stock added successfully!\n")
    output_box.insert("end", "Current price for " + symbol + " is $" + str(current_price))


def view_portfolio_gui():
    clear_output()

    data = read_json()

    if len(data) == 0:
        output_box.insert("end", "No stocks added yet.")
        return

    total_invested = 0
    total_current_value = 0

    output_box.insert("end", "Your Portfolio:\n")

    for i, stock in enumerate(data):
        current_price = get_current_price(stock["symbol"])

        if current_price is None:
            current_price = stock["buy_price"]

        invested = stock["shares"] * stock["buy_price"]
        current_value = stock["shares"] * current_price
        profit_loss = current_value - invested

        total_invested += invested
        total_current_value += current_value

        output_box.insert("end", "\n" + str(i + 1) + ". " + stock["symbol"] + "\n")
        output_box.insert("end", "Shares: " + str(stock["shares"]) + "\n")
        output_box.insert("end", "Buy Price: $" + str(stock["buy_price"]) + "\n")
        output_box.insert("end", "Current Price: $" + str(current_price) + "\n")
        output_box.insert("end", "Invested: $" + str(round(invested, 2)) + "\n")
        output_box.insert("end", "Current Value: $" + str(round(current_value, 2)) + "\n")
        output_box.insert("end", "Profit/Loss: $" + str(round(profit_loss, 2)) + "\n")

    overall_profit = total_current_value - total_invested

    output_box.insert("end", "\nTotal Invested: $" + str(round(total_invested, 2)) + "\n")
    output_box.insert("end", "Total Current Value: $" + str(round(total_current_value, 2)) + "\n")
    output_box.insert("end", "Overall Profit/Loss: $" + str(round(overall_profit, 2)))


def lookup_stock_gui():
    clear_output()

    symbol = stock_entry.get().upper()

    if symbol == "":
        output_box.insert("end", "Please enter a stock symbol.")
        return

    current_price = get_current_price(symbol)

    if current_price is None:
        output_box.insert("end", "Stock symbol not found.")
    else:
        output_box.insert("end", "Current price for " + symbol + " is $" + str(current_price))


def delete_stock_gui():
    clear_output()

    data = read_json()

    if len(data) == 0:
        output_box.insert("end", "No stocks to delete.")
        return

    symbol = stock_entry.get().upper()

    if symbol == "":
        output_box.insert("end", "Enter the stock symbol you want to delete.")
        return

    for stock in data:
        if stock["symbol"] == symbol:
            data.remove(stock)
            write_json(data)
            output_box.insert("end", symbol + " was deleted from your portfolio.")
            return

    output_box.insert("end", "Stock not found in your portfolio.")


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("750x650")
app.title("Stock Portfolio Tracker")

title = ctk.CTkLabel(app, text="Stock Portfolio Tracker", font=("Arial", 30))
title.pack(pady=20)

stock_entry = ctk.CTkEntry(app, placeholder_text="Enter Stock Symbol", width=280)
stock_entry.pack(pady=8)

shares_entry = ctk.CTkEntry(app, placeholder_text="Enter Number of Shares", width=280)
shares_entry.pack(pady=8)

buy_price_entry = ctk.CTkEntry(app, placeholder_text="Enter Buy Price", width=280)
buy_price_entry.pack(pady=8)

add_button = ctk.CTkButton(app, text="Add Stock", command=add_stock_gui)
add_button.pack(pady=6)

view_button = ctk.CTkButton(app, text="View Portfolio", command=view_portfolio_gui)
view_button.pack(pady=6)

lookup_button = ctk.CTkButton(app, text="Lookup Stock Price", command=lookup_stock_gui)
lookup_button.pack(pady=6)

delete_button = ctk.CTkButton(app, text="Delete Stock", command=delete_stock_gui)
delete_button.pack(pady=6)

output_box = ctk.CTkTextbox(app, width=620, height=230)
output_box.pack(pady=20)

app.mainloop()