import requests
import time
import pickle
from datetime import date, datetime, timedelta
import os 
import threading
from iexfinance.stocks import Stock
import subtrader
import logging
import sys


dir_path = os.path.dirname(__file__)


def pipes():

    dir_path = os.path.dirname(__file__)
    tradefile = dir_path + '/tradeIDs'
    try:
        with open(tradefile, 'r') as file:

            lines = file.readlines()
            if lines == []:
                raise Exception

            last_tradeID = lines[-1].split(',')[0]
            tradeID = int(last_tradeID)
 
    except Exception as e:
        tradeID = 0

    while True:

        trade_signal = receival[0]
        pct_change = receival[1]

        if trade_signal == 'long':
            tradeID+=1 
            t1 = threading.Thread(target=subtrader.long, args=((tradeID,pct_change)))
            t1.start()           
        
        if trade_signal == 'short':

            t1 = threading.Thread(target=subtrader.short, args=((tradeID,pct_change)))
            t1.start()

        if trade_signal == 'null':
            print('no trade')


# @sched.scheduled_job('interval', minutes=10000)
def main():

    if len(sys.argv) == 2:
        from trade_finder import signal_sender_test
        pipes_test()
    else:
        from trade_finder import signal_sender
        pipes()

# sched.start()