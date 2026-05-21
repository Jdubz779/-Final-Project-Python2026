

Stock Portfolio Tracker

Once I hit play, what should I do?

Run either main.py for the terminal version or gui.py for the GUI version.
In the app, enter a stock symbol like AAPL or NVDA, then add shares and a buy price.
You can view your portfolio, look up stock prices, delete stocks, see a portfolio summary, and graph stock prices.

Known bugs
If the internet is not working, live stock prices may not load.
Some fake stock symbols may cause errors if Yahoo Finance cannot find them.
The graph window may open behind the main app sometimes.
Users should only enter real stock symbols and valid numbers.
 

I worked alone on this project.

Concepts used:

Functions: used throughout the whole project.
JSON file handling: saves and loads portfolio data in portfolio.json.
APIs: used the yfinance library to get live stock prices.
GUI design: used CustomTkinter in gui.py.
Graphs/Data Visualization: used matplotlib to graph stock prices.
Loops and conditionals: used in portfolio calculations and stock searching.
User input validation: checks for bad inputs and fake stock symbols.