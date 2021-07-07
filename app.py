from flask import Flask, render_template, request, redirect, url_for
from pandas_datareader.data import DataReader
import yfinance as yf
import requests

# For time stamps
from datetime import datetime

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        ticker = request.form["nm"]
        return redirect(url_for('pipe', tkr=ticker))
    else:
        return render_template('index.html')


def get_symbol(symbol):
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(symbol)

    result = requests.get(url).json()

    for x in result['ResultSet']['Result']:
        if x['symbol'] == symbol:
            return x['name']


@app.route('/pipe<tkr>', methods=["GET", "POST"])
def pipe(tkr):
    tkr = tkr
    end = datetime.now()
    start = datetime(end.year-5, end.month, end.day)
    df = DataReader(tkr, data_source='stooq', start=start, end=end)

    if df.empty:
        return f"<h1>check ticker</h1>"

    tkr = get_symbol(tkr)

    dfJson = df.to_json(orient='split')
    return render_template('plot2.html', data=dfJson, tkr=tkr)
    # return dfJson


if __name__ == '__main__':
    # app.run(debug=True)
    app.run()
