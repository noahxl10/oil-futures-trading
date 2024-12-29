
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, JSON, DateTime


Base = declarative_base()


class FuturesDecisions(Base):
    __tablename__ = "futures_decisions_raw_v2"

    id = Column(Integer, primary_key=True)
    created_at_utc = Column(DateTime)
    trade_trigger = Column(Integer)
        # Options: (1, 0) 1 = did trigger, 0 = did not trigger
    trade_type = Column(String) 
        # Options: ('LONG', 'SHORT')
    decision_dttm = Column(DateTime)
    decision_payload = Column(JSON)

class FuturesData(Base):
    __tablename__ = "futures_data_raw_v2"

    id = Column(Integer, primary_key=True)
    created_at_utc = Column(DateTime)
    json_payload = Column(JSON)


# class Trades(Base):
#     __tablename__ = 'Trades_raw_v1'

#     id = Column(Integer, primary_key=True)
#     synbol = Column(String)
