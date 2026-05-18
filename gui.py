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

    data = read_json()

    stock_exists = False

    for stock in data:
        if stock["symbol"] == symbol:
            stock["shares"] += shares
            stock_exists = True
            break

    if stock_exists == False:
        new_stock = {
            "symbol": symbol,
            "shares": shares,
            "buy_price": buy_price
        }

        data.append(new_stock)

    write_json(data)

    if stock_exists:
        output_box.insert("end", "Existing stock updated successfully!\n")
    else:
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


def portfolio_summary_gui():
    clear_output()

    data = read_json()

    if len(data) == 0:
        output_box.insert("end", "No stocks added yet.")
        return

    total_invested = 0
    total_current_value = 0
    total_shares = 0

    best_stock = ""
    worst_stock = ""
    best_profit = None
    worst_profit = None

    for stock in data:
        current_price = get_current_price(stock["symbol"])

        if current_price is None:
            current_price = stock["buy_price"]

        invested = stock["shares"] * stock["buy_price"]
        current_value = stock["shares"] * current_price
        profit_loss = current_value - invested

        total_invested += invested
        total_current_value += current_value
        total_shares += stock["shares"]

        if best_profit is None or profit_loss > best_profit:
            best_profit = profit_loss
            best_stock = stock["symbol"]

        if worst_profit is None or profit_loss < worst_profit:
            worst_profit = profit_loss
            worst_stock = stock["symbol"]

    overall_profit = total_current_value - total_invested

    output_box.insert("end", "Portfolio Summary\n\n")
    output_box.insert("end", "Number of Stocks: " + str(len(data)) + "\n")
    output_box.insert("end", "Total Shares: " + str(round(total_shares, 2)) + "\n")
    output_box.insert("end", "Total Invested: $" + str(round(total_invested, 2)) + "\n")
    output_box.insert("end", "Current Portfolio Value: $" + str(round(total_current_value, 2)) + "\n")
    output_box.insert("end", "Overall Profit/Loss: $" + str(round(overall_profit, 2)) + "\n")
    output_box.insert("end", "Best Stock: " + best_stock + " ($" + str(round(best_profit, 2)) + ")\n")
    output_box.insert("end", "Worst Stock: " + worst_stock + " ($" + str(round(worst_profit, 2)) + ")")


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("900x600")
app.title("Stock Portfolio Tracker")

title = ctk.CTkLabel(app, text="Stock Portfolio Tracker", font=("Arial", 30))
title.pack(pady=15)

main_frame = ctk.CTkFrame(app)
main_frame.pack(padx=20, pady=10, fill="both", expand=True)

control_frame = ctk.CTkFrame(main_frame, width=280)
control_frame.pack(side="left", padx=15, pady=15, fill="y")

display_frame = ctk.CTkFrame(main_frame)
display_frame.pack(side="right", padx=15, pady=15, fill="both", expand=True)

stock_entry = ctk.CTkEntry(control_frame, placeholder_text="Enter Stock Symbol", width=230)
stock_entry.pack(pady=10)

shares_entry = ctk.CTkEntry(control_frame, placeholder_text="Enter Number of Shares", width=230)
shares_entry.pack(pady=10)

buy_price_entry = ctk.CTkEntry(control_frame, placeholder_text="Enter Buy Price", width=230)
buy_price_entry.pack(pady=10)

add_button = ctk.CTkButton(control_frame, text="Add Stock", command=add_stock_gui, width=230)
add_button.pack(pady=7)

view_button = ctk.CTkButton(control_frame, text="View Portfolio", command=view_portfolio_gui, width=230)
view_button.pack(pady=7)

lookup_button = ctk.CTkButton(control_frame, text="Lookup Stock Price", command=lookup_stock_gui, width=230)
lookup_button.pack(pady=7)

delete_button = ctk.CTkButton(control_frame, text="Delete Stock", command=delete_stock_gui, width=230)
delete_button.pack(pady=7)

summary_button = ctk.CTkButton(control_frame, text="Portfolio Summary", command=portfolio_summary_gui, width=230)
summary_button.pack(pady=7)

output_box = ctk.CTkTextbox(display_frame, width=520, height=470)
output_box.pack(padx=15, pady=15, fill="both", expand=True)

app.mainloop()