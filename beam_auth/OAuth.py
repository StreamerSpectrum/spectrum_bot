''' Beam Authentication '''

import webbrowser
import requests
from requests_oauthlib import OAuth2Session


class OAuth():
    ''' Handles the generatation of a new OAuth access token  '''

    def __init__(self, config):
        self.config = config

    def _buildurl(self, path):
        return self.config.BEAM_URI + path

    def generate(self, code):
        ''' Generates access token information '''
        if code is None:
            return self.generate_new()
        elif len(code) == 64:
            return self.generate_refresh(code)
        else:
            self.generate_output(False)

    def generate_new(self):
        ''' Generates shortcode and gets access token from Beam '''
        #Sets up the OAuth URL to generate Shortcode
        oauth = OAuth2Session(self.config.CLIENT_ID, redirect_uri=self.config.REDIRECT_URI,
                              scope=self.config.SCOPE)
        # Forms an authorization URL
        authorization_url, state = oauth.authorization_url(self.config.OAUTH_URI)

        # Opens a new tab in browser for permission agreement and
        # short code retrieval
        webbrowser.open_new(authorization_url)

        # Gets User to input the shortcode
        code = input('Please enter your Shortcode : ')
        while len(code) < 16 or len(code) > 16:
            print('SHORTCODE ERROR: The shortcode entered is not the correct length\n'
                  '                 please check and re-enter')
            code = input('Please enter your Shortcode : ')

        # Creates the data used to send to the the beam API to access
        # the access and refresh token information
        data = dict(client_id=self.config.CLIENT_ID, code=code,
                    redirect_uri=self.config.REDIRECT_URI,
                    grant_type='authorization_code')

        # Generates the header for the request
        header = {'Media-Type': 'application/json'}

        # gets the the Access and Refresh tokens and returns them
        # to be processed
        responce = requests.post(url=self._buildurl(self.config.AUTHTOKEN_URI),
                                 data=data, headers=header).json()
        return self.generate_output(responce)

    def generate_refresh(self, code):
        ''' refreshes the access and refresh tokens '''
        # Create Data for request
        data = dict(client_id=self.config.CLIENT_ID, refresh_token=code,
                    grant_type='refresh_token')
        #crete Header for request
        header = {'Media-Type': 'application/json'}
        # Send request and return the responce
        responce = requests.post(url=self._buildurl(self.config.AUTHTOKEN_URI),
                                 data=data, headers=header).json()
        return self.generate_output(responce)

    def generate_userinfo(self, code):
        ''' gets and returns the user information from beam '''

        # Create Data for request
        data = dict(client_id=self.config.CLIENT_ID)
        # Creates the header for the request
        header = {'Media-Type': 'application/json',
                  'Authorization': 'Bearer ' + code}
        # Get the request and return the responce
        tmp = requests.get(url=self._buildurl(self.config.USERSCURRENT_URI), data=data,
                           headers=header).json()
        # gets the data needed from the infrormation obtained from beam
        responce = {'error': False,
                    'user_id': tmp['channel']['userId'],
                    'username': tmp['username'],
                    'channel_id': tmp['channel']['id']}
        return responce

    def generate_output(self, data):
        ''' generates a responce as a dict depending on the data '''

        # If the data is False
        if not data:
            # returns error if data is corrupt or incorrect
            return {'error': True,
                    'reason': ('DATA ERROR: Authentication data is incorrect, '
                               'please recheck your data')}
        # if 'error' key exists
        elif 'error' in data:
            # returns error information if cannot authenticate
            if 'error_description' in data:
                return {'error': True,
                        'reason': 'API ERROR: ' + data['error_description']}
            else:
                return {'error': True,
                        'reason': ('There has been an error caused during authentication, '
                                   'code is no longer valid')}
        else:
            # returns token data in dictionary type
            return {'error': False,
                    'access_token': data['access_token'],
                    'refresh_token': data['refresh_token'],
                    'expires_in': data['expires_in'],
                    'token_type': data['token_type']}
