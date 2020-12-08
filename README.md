# Analysis_IBOV_make_up

This code get the stocks which make up the index IBOVESPA. The data were collected on the B3 site, an the CSV as been provided here.
Librarys used: pandas, yfinance, plotly, numpy, PyTrend, os and datetime.

# The Code!

1. The code returns 15 positive and negative variation of the stocks in a Treemap form. The user select if this variation is daily, monthly or year to date.

2. With the library PyTrend, the code returns the 20 stocks most searched on google, on a period, which is provided by the user.
Tip 1. The Trend is saved on an excel file with the period on the name.
Tip 2.: Insert the data in the American form : 2020-12-08

3. Also, with the PyTrend, the code returns the data with stocks are most searched, searche above 95 on the google trend.
