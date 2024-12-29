import base64
#### PACKAGES ####
import requests
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

from datetime import datetime, timedelta, timezone
import datetime as dt

import os 
import time
# import logging

#### LOCAL IMPORTS ####
import db
import models

ENV = 'dev'
DB = db.DB(ENV)
DB_ENGINE = DB.engine
DB.setup()

## DB SESSION ##
Session = sessionmaker(bind=DB_ENGINE)
session = Session()

## DATETIME FORMAT ##

def now(return_type='string', time_add=None):
    # example usage: time_check(now(return_type='datetime', time_add = timedelta(hours=11, minutes=46)))
    time = datetime.now(timezone.utc)

    if time_add is not None:
            time = time + time_add

    if return_type == 'datetime':
        return time
    else:
        time = time.strftime("%Y-%m-%d %H:%M:%S.%f")
        time = time[0:-4]
    
    return time
    


# this function checks to see if it is a good time to check another set of data from
# crude oil. It only checks periodically becaause checking every minute will miss the big % moves!
# since big % moves don't happen in a minute. It also checks from previous close to new open.
def time_check(currentTime):
    currentTime = currentTime.time()

    times_start = [
                    datetime(2022, 1, 1, 14, 30, 0), 
                    datetime(2022, 1, 1, 14, 59, 0), 
                    datetime(2022, 1, 1, 15, 59, 0),
                    datetime(2022, 1, 1, 16, 59, 0), 
                    datetime(2022, 1, 1, 17, 59, 0),
                    datetime(2022, 1, 1, 18, 59, 0), 
                    datetime(2022, 1, 1, 19, 59, 0),
                    datetime(2022, 1, 1, 20, 59, 0)
                    ]

    for i in range(len(times_start)):
        endtime = times_start[i] + timedelta(minutes=2)
        endtime2 = times_start[7] + timedelta(minutes=2)

        if (times_start[i].time() <=currentTime <= endtime.time()) == True:            
                
            if (endtime2.time() <= currentTime <= times_start[7]) == True:
                # if current time is between last close and market open, don't place a trade
                fillVar = 0
            else:
                return True

        else:
            pass
    return False
## test for time_check
# print(time_check(now(return_type='datetime', time_add = timedelta(hours=11, minutes=46))))



## Should have two functions: one for trading, one for analyzing the movement.
def signal_sender():

    # create close_data list that keeps a list of all data we gather
    close_data = []
    time_data = []

    # request data from API to itnitialize array with current data, otherwise the loop won't have anything to compare to 
    # try:
    hour_offset = -17  #default -17
    date = now(return_type='string', time_add = timedelta(hours=hour_offset, minutes=0))
    date = date[0:-6]
    with DB_ENGINE.connect() as connection:
        results = connection.execute(text(f"""
            select 
                * 
            from futures_data_raw_v2 
            where to_char(created_at_utc, 'YYYY-MM-DD HH24:MI:SS') ilike '%{date}%' 
        """))
        for result in results:        
            if result["json_payload"]['status'] == 'success':
                close_data.append(result['json_payload']['data']['price'])
                time_data.append(result['json_payload']['data']['created_at'])
            else:
                futures_decisions = models.FuturesDecisions(
                    created_at_utc = now(),
                    trade_trigger = 0,
                    trade_type = 'NONE',
                    decision_dttm = now(),
                    decision_payload = {'close_data': [],
                                        'time_data': [],
                                        'status': result["json_payload"]['status']}
                )
                session.add(futures_decisions)
                session.commit()
                exit()


    query = session.query(models.FuturesData).order_by(models.FuturesData.created_at_utc.desc()).first()
    current_close = query.json_payload['data']['price']
    current_time = query.json_payload['data']['created_at'] 
    # Append close and time data to respective lists
    close_data.append(current_close)
    time_data.append(current_time)

    move_trigger = float(os.environ.get('MOVE_TRIGGER')) # .5%

    try:

        last_close = close_data[0]
        cur_close = close_data[1] 

        pct_change = cur_close/last_close - 1

        if abs(pct_change) > move_trigger:
            if pct_change > 0:
                # GO LONG, 
                trade_trigger = 1
                trade_type = 'LONG'
                print(f'pct_change: {pct_change}')

            if pct_change < 0:
                # GO SHORT
                trade_trigger = 1
                trade_type = 'SHORT'
                print(f'pct_change: {pct_change}')
        else:
                trade_trigger = 0
                trade_type = 'NONE'

        futures_decisions = models.FuturesDecisions(
            created_at_utc = now(),
            trade_trigger = trade_trigger,
            trade_type = trade_type,
            decision_dttm = now(),
            decision_payload = {'close_data': close_data,
                                'time_data': time_data,
                                'status': 'success'}
        )
        session.add(futures_decisions)
        session.commit()

    except Exception as e:
        print(e)

def main(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    signal_sender()
