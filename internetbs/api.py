import requests
from urllib.parse import quote

class ApiWrapper():
    """
        A simple wrapper for domain registrant internetbs.net
    """
    def __init__ (self, key = None, password = None):
        """
            Instantiates a wrapper object. If no key or password are provided, test credentials are used.
        """
        self.KEY = key or 'testapi'
        self.PASSWORD = password or 'testpass'
        self.URL = 'https://api.internet.bs/'
        # assume we use test credential if none were provided
        if not key or not password:
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

        #or k,v in full_params.items():
        #    full_params[k] = quote(v)

        endpoint = self.URL + endpoint
        response = requests.get(endpoint , params = full_params)

        return response

    
    
    def domain_check(self, domain, raw=False):
        """
            The command is intended to check whether a domain is available for registration or not. The command is not generating any cost.
        """
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
    
    def domain_create(self, domain, contact_info, raw=True, **kwargs):
        """
            The command is intended to register a new domain
        """
        endpoint = '/Domain/Create'

        params = {
            'Domain' : domain
        }

        params.update(contact_info)
        params.update(kwargs)

        response = self.__perform_get_request(endpoint, params)

        if response.status_code == 200:
            parsed_response = response.json()
            if raw:
                return parsed_response
            else:
                return parsed_response['product'][0]['status'] == 'SUCCESS'