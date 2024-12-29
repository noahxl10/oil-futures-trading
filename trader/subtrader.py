
import requests
import time
import os
import alpaca 
from iexfinance.stocks import Stock
import logging
import datetime as dt
from datetime import datetime

dir_path = os.path.dirname(__file__)

## Read in ticker from txt file

# try:
#     base = base1 + '/parameters'
#     response = requests.get(base)

#     response = response.json()
    
#     ticker = response['ticker']
#     move_trigger = response['move_trigger']
#     trade_period = response['trade_period']
#     hour_offset = response['hour_offset']

# except Exception as e:
#     base = base1 + '/parameters'
#     response = requests.get(base)
#     response = response.text
#     raise Exception('No "parameters" file', response)




stockObj = Stock('XOM', token='sk_7877f23aca6b44e1be3eb1cad70c8860')
quote = stockObj.get_quote()
ticker = 'XOM'

api = alpaca.Alpaca()

def numshares(ticker):
    buyingpower = api.checkbuyingpower()
    equity_at_risk =  350 #risk_factor*balance
    quote = stockObj.get_quote()
    close = quote['iexRealtimePrice'][ticker]
    cents_at_risk = .02*close
    
    numshares = round(equity_at_risk/cents_at_risk)
    if numshares*close > buyingpower:
        numshares = round(buyingpower/close) - 5 # subtract 5 shares to ensure enough equity...

    return numshares

print(numshares(ticker))

def long(tradeID, pct_change):

    tradeType = 'long'
    tradeInfo = tradeInfoCreator(tradeType, tradeID)
    quote = stockObj.get_quote()
    entered_price = quote['iexRealtimePrice']
    entered_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(quote['iexCloseTime']/1000 + 60*60*hour_offset))
    api = alpaca()
    numshares = tradeInfo[3]
    if numshares <= 0:
        print('Not enough buying power')
        exit()
    if api.checkMarket() == False:
        print('market closed')
        exit()
    # alpaca trading
    
    api.longmarket(ticker, tradeInfo[3])
    time.sleep(2)
    # end

    while True:
        # non-alpaca trading
        quote = stockObj.get_quote()
        current_close = quote['iexRealtimePrice']

        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(quote['iexCloseTime']/1000 + 60*60*hour_offset))

        trade_gain_or_loss = (current_close - entered_price)/entered_price
        close_reason = 'null'
        ## non-alpaca paper trading
        line = [tradeID, ticker, tradeType, pct_change, entered_price,  entered_time, current_close,current_time, trade_gain_or_loss, close_reason]

        ## end

        if (trade_gain_or_loss < -.02) or (trade_gain_or_loss > .02):
            close_reason = 'stop_loss'
            line = [tradeID, ticker, tradeType, pct_change, entered_price, entered_time, current_close, current_time, trade_gain_or_loss, close_reason]

            api.closeposition(tradeInfo)
            time.sleep(2)
            print('killed trade ', tradeID)
            exit()

        if trade_period == 'day' and timecheck(quote) == True:
            close_reason = 'day_end'
            line = [tradeID, ticker, tradeType, pct_change, entered_price, entered_time, current_close, current_time, trade_gain_or_loss, close_reason]

            api.closeposition(tradeInfo)
            time.sleep(2)
            print('killed trade ', tradeID)
            exit()

        time.sleep(60)

def short(tradeID, pct_change):
    # SETUP

    base = "https://oil-trader-api.herokuapp.com/futures/realtime"
    tradeType = 'short'
    tradeInfo = tradeInfoCreator(tradeType, tradeID)
    quote = stockObj.get_quote()
    entered_price = quote['iexRealtimePrice']
    entered_time = quote['iexCloseTime']
    
    numshares = tradeInfo[3]
   
    if numshares <= 0:
        print('Not enough buying power')
        exit()
    # alpaca trading
    api = alpaca()
    if api.checkMarket() == False:
        print('market closed')
        exit()
    api.short(ticker, numshares)

    while True:
        
        quote = stockObj.get_quote()
        current_close = quote['iexRealtimePrice']
        current_time = quote['iexCloseTime']
        
        trade_gain_or_loss = (entered_price-current_close)/entered_price
        close_reason = 'null'
        
        line = [tradeID, ticker, tradeType, pct_change, entered_price, entered_time, current_close, current_time, trade_gain_or_loss, close_reason]        

        ## checks to see if the stop loss was hit
        if (trade_gain_or_loss < -.02) or (trade_gain_or_loss > .02):
            close_reason = 'stop_loss'
            line = [tradeID, ticker, tradeType, pct_change, entered_price, entered_time, current_close, current_time, trade_gain_or_loss, close_reason]
            writetodatafile(line)
            api.closeposition(tradeInfo)
            time.sleep(2)
            print('killed trade ', tradeID)
            exit()
        
        ## checks to see if 
        if trade_period == 'day' and timecheck(quote) == True:
            close_reason = 'day_end'
            line = [tradeID, ticker, tradeType, pct_change, entered_price, entered_time, current_close, current_time, trade_gain_or_loss, close_reason]
            writetodatafile(line)
            api.closeposition(tradeInfo)
            time.sleep(2)
            print('killed trade ', tradeID)
            exit()

        time.sleep(60)

def timecheck(quote):
    current_close = quote['iexRealtimePrice']
    current_time = datetime.fromtimestamp(quote['iexCloseTime']/1000).time()
    end_of_day = dt.time(15,57)

    if current_time > end_of_day:
        return True
    else:
        return False

