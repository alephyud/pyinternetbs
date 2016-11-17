import requests
from urllib.parse import quote

class ApiWrapper():
    def __init__ (self, key = None, password = None):
        self.KEY = key or 'testapi'
        self.PASSWORD = password or 'testpass'
        self.URL = 'https://api.internet.bs/'
        # assume we use test credential if none were provided
        if not key or not password:
            print('Wrapper uses test credentials')
            self.URL = 'https://testapi.internet.bs'
    
    def __perform_get_request (self, endpoint, params=dict()):
        credentials = {
            'ApiKey' : self.KEY,
            'Password' : self.PASSWORD
        }

        full_params = {
            'ResponseFormat' : 'JSON'
        }
        
        full_params.update(credentials)
        full_params.update(params)

        endpoint = self.URL + endpoint
        response = requests.get(endpoint , params = full_params)

        return response

    def domain_check(self, domain, raw=True):
        endpoint = '/Domain/Check'
        
        params = {
            'Domain' : domain,
        }

        response = self.__perform_get_request(endpoint, params)

        if response.status_code == 200:
            parsed_response = response.json()
            if raw:
                return parsed_response
            else:
                return parsed_response.get('status') == 'AVAILABLE'             
    