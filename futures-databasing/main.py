
from sqlalchemy.orm import sessionmaker

from datetime import datetime, timedelta, timezone
import datetime as dt
import os 

import db
import models
import oil_api as oil

ENV = 'dev'
DB = db.DB(ENV)
DB_ENGINE = DB.engine

Session = sessionmaker(bind=DB_ENGINE)
session = Session()

def now(return_type='string', time_add=None):
    time = datetime.now(timezone.utc)
    if time_add is not None:
            time = time + time_add

    if return_type == 'datetime':
        return time
    else:
        time = time.strftime("%Y-%m-%dT%H:%M:%S.%f")
        time = time[0:-4]
    
    return time


def main(event=None, context=None):
    try:
        oilobj = oil.OilApi()
        data = oilobj.get_latest()
        futures_data = models.FuturesData(
            created_at_utc = now(),
            json_payload = data
        )
        session.add(futures_data)
        session.commit()
    except:
        print('failure')
