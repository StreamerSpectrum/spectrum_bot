'''
    File : beamauth.py
    Author : CAPGames

    Description : Checks code supplied if is an access token or shortcode.
                  If the code is a shortcode then it will generate an access and refresh token.
                  If the code is an access token then it will perform a token refresh.
'''

import requests

OATH_TOKEN_URL = 'https://beam.pro/api/v1/oauth/token'
USERS_CURRENT_URL = 'https://beam.pro/api/v1/users/current'
class OAuth():
    ''' Handles the generatation of a new OAuth access token  '''

    def __init__(self, client_id, redirect_uri):
        self.client_id = client_id
        self.redirect_uri = redirect_uri

    def generate_dict(self, data):
        ''' generates a responce as a dict depending on the data '''

        # If the data is False
        if not data:
            # retrun a False validity
            return {'error': True,
                    'reason': 'The code entered is the incorrect length'}
        elif  'error' in data:
            if 'error_description' in data:
                return {'error': True,
                        'reason': data['error_description']}
            else:
                return {'error': True,
                        'reason': 'There was an issue with authorization'}
        else:
            # return a True validity along with the token data
            return {'error': False,
                    'access_token': data['access_token'],
                    'refresh_token': data['refresh_token'],
                    'expires_in': data['expires_in'],
                    'token_type': data['token_type']}

    def token_refresh(self, code):
        ''' refreshes the access and refresh tokens '''
        # Create Data for request
        data = dict(client_id=self.client_id, refresh_token=code,
                    grant_type='refresh_token')
        #crete Header for request
        header = {'Media-Type': 'application/json'}
        # Send request and return the responce
        tmp = requests.post(url=OATH_TOKEN_URL, data=data, headers=header).json()
        return self.generate_dict(tmp)

    def get_access(self, code):
        """retrieves access and fresh tokens from beam api"""
        # Creates the data used to send to the the beam API to access
        # the access and refresh token information
        data = dict(client_id=self.client_id, code=code,
                    redirect_uri=self.redirect_uri, grant_type='authorization_code')

        # Generates the header for the request
        header = {'Media-Type': 'application/json'}

        # gets the the Access and Refresh tokens and returns them
        # to be processed
        tmp = requests.post(url=OATH_TOKEN_URL, data=data, headers=header).json()
        return self.generate_dict(tmp)

    def get_userinfo(self, code):
        ''' gets and returns the user information from beam '''

        # Create Data for request
        data = dict(client_id=self.client_id)
        # Creates the header for the request
        header = {'Media-Type': 'application/json',
                  'Authorization': 'Bearer ' + code}
        # Get the request and return the responce
        return requests.get(url=USERS_CURRENT_URL, data=data, headers=header).json()

    def check(self, code):
        ''' Checks the code and determines if to refressh or get a new access token '''

        # If the code is a shortcode
        if len(code) == 16:
            # Get access token using the short code
            return self.get_access(code)

        # If the code is a refresh token
        elif len(code) == 64:
            # performs a token refresh and retrun the data
            return self.token_refresh(code)
        else:
            # return an error
            return self.generate_dict(False)
    