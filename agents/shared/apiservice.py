

import requests
from requests.auth import HTTPBasicAuth

class ApiService1():
    """

    This class is shared request service

    """
    def _api_call( self,method,url,**kwargs):
        response = requests.request(method,url, **kwargs)
        print(response)
        return response
    def _basic_auth( self,email,token):
        auth = HTTPBasicAuth(email,token)
        print(auth)
        return auth