**Oil Futures Trader V3**


Architecture:
- Google Cloud Functions triggers futures_reader.py
- futures_reader.py triggers cloud run of oil_trader.py 
- Use RDBMS to store data 
    - In this, we store all data from futures_reader.py
        - Event logs, data pulled, trigger/no trigger etc. 
    - Store all data from oil_trader.py