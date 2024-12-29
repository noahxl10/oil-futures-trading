
import requests
import os 

class OilApi:
    """
    Example data: 
        {
            'status': 'success', 
            'data': {
                    'price': 94.79, 
                    'formatted': '$94.79', 
                    'currency': 'USD', 
                    'code': 'BRENT_CRUDE_USD', 
                    'created_at': '2022-11-09T05:16:03.538Z', 
                    'type': 'spot_price'
                    }
        }
    """
    def __init__(self):
        API_KEY = os.environ.get('API_KEY')
        self.headers = {
            'Authorization': f'Token {API_KEY}',
            'Content-Type': 'application/json'
            }

    def get_latest(self):
        self.endpoint = 'https://api.oilpriceapi.com/v1/prices/latest'
        response = requests.get(url = self.endpoint, headers = self.headers)
        data = response.json()
        return data

    def get_custom(self, start: int, end: int):
        self.endpoint = 'https://api.oilpriceapi.com/v1/prices?by_period[from]=${start}&by_period[to]=${end}'
        response = requests.get(url = self.endpoint, headers = self.headers)
        data = response.json()
        return data

    def get_past_day(self):
        self.endpoint = 'https://api.oilpriceapi.com/v1/prices/past_day'
        response = requests.get(url = self.endpoint, headers = self.headers)
        data = response.json()
        return data
    def get_past_week(self):
        self.endpoint = 'https://api.oilpriceapi.com/v1/prices/past_week'
        response = requests.get(url = self.endpoint, headers = self.headers)
        data = response.json()
        return data
    
    def get_past_month(self):
        self.endpoint = 'https://api.oilpriceapi.com/v1/prices/past_month'
        response = requests.get(url = self.endpoint, headers = self.headers)
        data = response.json()
        return data

    def get_past_year(self):
        self.endpoint = 'https://api.oilpriceapi.com/v1/prices/past_year'
        response = requests.get(url = self.endpoint, headers = self.headers)
        data = response.json()
        return data

    def get_all_time(self):
        self.endpoint = 'https://api.oilpriceapi.com/v1/prices'
        response = requests.get(url = self.endpoint, headers = self.headers)
        data = response.json()
        return data
