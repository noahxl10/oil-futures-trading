import alpaca_trade_api as tradeapi
import time



class Alpaca:
    def __init__(self):
        self.api = tradeapi.REST(
                        api_key,
                        api_secret,
                        'https://paper-api.alpaca.markets')
        self.account = self.api.get_account()

    def longmarket(self, ticker, shares):
        print('Going long!')
        ticker = ticker.upper()
        try:
            self.api.submit_order(symbol = ticker, qty = shares, 
                side = 'buy', type = 'market', time_in_force = 'gtc')
            print('Order confirmed.') 
            time.sleep(3)
            if int(self.position(ticker).qty) > 0:
                print(f'Long position open for {ticker}')
        except Exception as e:
            # LOG HERE
            
            print(str(e))
            print('Long market order failed.')

    def short(self, ticker, shares):
        print('Going short!')
        try: 
            self.api.submit_order(symbol = ticker, qty = shares, side = 'sell', type = 'market', time_in_force = 'gtc')
            time.sleep(4)
            print('Order confirmed.')
            
            if int(self.position(ticker).qty) < 0:
                print(f'Short position open for {ticker}')
        except Exception as e:
            
            print(str(e))
            print('Short order failed.')

    def checkbal(self):
        cur_bal = float(self.account.equity)
        #balance_change = float(account.equity) - float(account.last_equity)
        return cur_bal #, balance_change

    def checkMarket(self):
        clock = self.api.get_clock()
        return clock.is_open

    def checkbuyingpower(self):
        cur_bp = float(self.account.buying_power)
        return cur_bp

    def position(self, ticker):
        try:
            pos = self.api.get_position(ticker)
            print(f'Number of shares: {pos.qty}\n Market Value: {pos.market_value}\nProfit/Loss: {pos.change_today}' ) 
            return pos
        except Exception as e:
            print(str(e))
            print('No position found.')


    def closeposition(self, tradeInfo):
        ticker = tradeInfo[1]
        typetoclose = tradeInfo[2]
        numshares = tradeInfo[3]
        
        print('Closing position...')
        if typetoclose == 'short':
            self.api.submit_order(symbol = ticker, qty = -int(numshares), 
                side = 'buy', type = 'market', time_in_force = 'gtc')
            time.sleep(3)
            try: 
                if self.position() == 0:
                    print("Position didn't close")
            except Exception as e:
                
            
                print(f'Short position in {ticker} closed.')
                
        if typetoclose == 'long':
            self.api.submit_order(symbol = ticker, qty = int(numshares), 
                side = 'sell', type = 'market', time_in_force = 'gtc')
            
            time.sleep(3)
            try:
                if self.position() == 0:
                    print("Position didn't close")
                    
            except Exception as e:
                print(f'Long position in {ticker} closed.')

