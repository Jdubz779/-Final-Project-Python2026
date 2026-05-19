import json
import yfinance as yf
import customtkinter as ctk
import matplotlib.pyplot as plt

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


def format_money(amount):
    return "$" + str(round(amount, 2))


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


def clear_inputs():
    stock_entry.delete(0, "end")
    shares_entry.delete(0, "end")
    buy_price_entry.delete(0, "end")


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

    output_box.insert("end", "Current price for " + symbol + " is " + format_money(current_price))

    clear_inputs()


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
        output_box.insert("end", "Buy Price: " + format_money(stock["buy_price"]) + "\n")
        output_box.insert("end", "Current Price: " + format_money(current_price) + "\n")
        output_box.insert("end", "Invested: " + format_money(invested) + "\n")
        output_box.insert("end", "Current Value: " + format_money(current_value) + "\n")
        output_box.insert("end", "Profit/Loss: " + format_money(profit_loss) + "\n")

    overall_profit = total_current_value - total_invested

    output_box.insert("end", "\nTotal Invested: " + format_money(total_invested) + "\n")
    output_box.insert("end", "Total Current Value: " + format_money(total_current_value) + "\n")
    output_box.insert("end", "Overall Profit/Loss: " + format_money(overall_profit))


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
        output_box.insert("end", "Current price for " + symbol + " is " + format_money(current_price))


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
            clear_inputs()
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
    output_box.insert("end", "Total Invested: " + format_money(total_invested) + "\n")
    output_box.insert("end", "Current Portfolio Value: " + format_money(total_current_value) + "\n")
    output_box.insert("end", "Overall Profit/Loss: " + format_money(overall_profit) + "\n")
    output_box.insert("end", "Best Stock: " + best_stock + " (" + format_money(best_profit) + ")\n")
    output_box.insert("end", "Worst Stock: " + worst_stock + " (" + format_money(worst_profit) + ")")


def graph_stock_gui():
    clear_output()

    symbol = stock_entry.get().upper()

    if symbol == "":
        output_box.insert("end", "Please enter a stock symbol to graph.")
        return

    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1mo", raise_errors=False)

        if data.empty:
            output_box.insert("end", "Stock symbol not found.")
            return

        plt.figure(figsize=(8, 4))
        plt.plot(data.index, data["Close"])

        plt.title(symbol + " Stock Price - Last Month")
        plt.xlabel("Date")
        plt.ylabel("Closing Price")
        plt.grid(True)

        plt.tight_layout()
        plt.show()

        output_box.insert("end", "Graph created for " + symbol + ".")

    except Exception:
        output_box.insert("end", "Error creating stock graph.")


def show_help_gui():
    clear_output()

    output_box.insert("end", "How to Use This App\n\n")
    output_box.insert("end", "Add Stock:\n")
    output_box.insert("end", "Enter a ticker symbol, shares, and buy price.\n\n")
    output_box.insert("end", "View Portfolio:\n")
    output_box.insert("end", "Shows all saved stocks and profit/loss.\n\n")
    output_box.insert("end", "Lookup Stock Price:\n")
    output_box.insert("end", "Enter only a ticker symbol to see its current price.\n\n")
    output_box.insert("end", "Delete Stock:\n")
    output_box.insert("end", "Enter a ticker symbol and click Delete Stock.\n\n")
    output_box.insert("end", "Portfolio Summary:\n")
    output_box.insert("end", "Shows total value, total invested, best stock, and worst stock.\n\n")
    output_box.insert("end", "Graph Stock:\n")
    output_box.insert("end", "Enter a ticker symbol and click Graph Stock to see its last month of prices.")


def show_about_gui():
    clear_output()

    output_box.insert("end", "Stock Portfolio Tracker\n\n")
    output_box.insert("end", "This project uses Python, JSON, CustomTkinter, yfinance, and matplotlib.\n")
    output_box.insert("end", "It lets users track stocks, calculate portfolio value, look up live prices, and graph stock history.\n")
    output_box.insert("end", "The goal is to make a useful investment tracking app with both data storage and live market data.")


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("950x650")
app.title("Stock Portfolio Tracker")

title = ctk.CTkLabel(app, text="Stock Portfolio Tracker", font=("Arial", 30))
title.pack(pady=15)

main_frame = ctk.CTkFrame(app)
main_frame.pack(padx=20, pady=10, fill="both", expand=True)

control_frame = ctk.CTkFrame(main_frame, width=290)
control_frame.pack(side="left", padx=15, pady=15, fill="y")

display_frame = ctk.CTkFrame(main_frame)
display_frame.pack(side="right", padx=15, pady=15, fill="both", expand=True)

input_label = ctk.CTkLabel(control_frame, text="Stock Inputs", font=("Arial", 18))
input_label.pack(pady=10)

stock_entry = ctk.CTkEntry(control_frame, placeholder_text="Enter Stock Symbol", width=240)
stock_entry.pack(pady=8)

shares_entry = ctk.CTkEntry(control_frame, placeholder_text="Enter Number of Shares", width=240)
shares_entry.pack(pady=8)

buy_price_entry = ctk.CTkEntry(control_frame, placeholder_text="Enter Buy Price", width=240)
buy_price_entry.pack(pady=8)

button_label = ctk.CTkLabel(control_frame, text="Actions", font=("Arial", 18))
button_label.pack(pady=10)

add_button = ctk.CTkButton(control_frame, text="Add Stock", command=add_stock_gui, width=240)
add_button.pack(pady=5)

view_button = ctk.CTkButton(control_frame, text="View Portfolio", command=view_portfolio_gui, width=240)
view_button.pack(pady=5)

lookup_button = ctk.CTkButton(control_frame, text="Lookup Stock Price", command=lookup_stock_gui, width=240)
lookup_button.pack(pady=5)

delete_button = ctk.CTkButton(control_frame, text="Delete Stock", command=delete_stock_gui, width=240)
delete_button.pack(pady=5)

summary_button = ctk.CTkButton(control_frame, text="Portfolio Summary", command=portfolio_summary_gui, width=240)
summary_button.pack(pady=5)

graph_button = ctk.CTkButton(control_frame, text="Graph Stock", command=graph_stock_gui, width=240)
graph_button.pack(pady=5)

help_button = ctk.CTkButton(control_frame, text="Help", command=show_help_gui, width=240)
help_button.pack(pady=5)

about_button = ctk.CTkButton(control_frame, text="About Project", command=show_about_gui, width=240)
about_button.pack(pady=5)

output_label = ctk.CTkLabel(display_frame, text="Output", font=("Arial", 18))
output_label.pack(pady=10)

output_box = ctk.CTkTextbox(display_frame, width=560, height=500)
output_box.pack(padx=15, pady=10, fill="both", expand=True)

app.mainloop()