''' Handles the core parts of the bot '''

from datetime import datetime, timedelta
import webbrowser
from requests_oauthlib import OAuth2Session
from database import db
from beam import authentication

#######################
# Beam Authentication #
#######################

def token_handling(data, account):
    ''' Handles saving the OAuth tokens to the database '''
    dte = datetime.now() + timedelta(seconds=data['expires_in'])
    tmp = ("access_token='{a}', ".format(a=data['access_token']) +
           "refresh_token='{r}', ".format(r=data['refresh_token']) +
           "token_expire='{e}'".format(e=dte))
    db.set_db('accounts', tmp, account)

def oauth_handling(account):
    ''' Sets up the beam OAuth in the config file '''
    client_id = db.get_db('settings', 'client_id')[1]
    scope = db.get_db('settings', 'scope')[1]
    redirect_uri = db.get_db('api_url', 'redirect_url')[1]
    oauth_url = db.get_db('api_url', 'oauth_endpoint')[1]

    # creates an object for authentication.OAuth
    beamoauth = authentication.OAuth(client_id, redirect_uri)

    # Checks the database if there is a valid OAuth Token
    if db.get_db('accounts', account)[3] is None:

        #Sets up the OAuth URL to generate Shortcode
        oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
        authorization_url, state = oauth.authorization_url(oauth_url)

        # Opens a new tab in browser for permission agreement and
        # short code retrieval
        webbrowser.open_new(authorization_url)

        # Gets User to input the shortcode
        code = input('Please input your Shortcode : ')
        tmp = beamoauth.check(code)
        while tmp['error']:
            print(tmp['reason'])
            code = input('Please input your Shortcode : ')
            tmp = beamoauth.check(code)
        # If there is no OAuth token then start the proccess
        # of generating one.
        token_handling(tmp, account)
    else:
        # if an OAuth access token is saved to the database then this
        # gets the Time now and the expiry imformation of the OAuth token
        dtn = datetime.now()
        dte = datetime.strptime(db.get_db('accounts', account)[5], '%Y-%m-%d %H:%M:%S.%f')

        # Check to see if the OAtuh access token has expired
        if dtn > dte:
            # OAtuh access token has expired then perform a token refresh
            print('Token expired for {acc} account, token refreshing...'.format(acc=account))
            tmp = beamoauth.check(db.get_db('accounts', account)[4])
            token_handling(tmp, account)

def initialize():
    ''' Checks if the OAuth tokens are expired '''
    client_id = db.get_db('settings', 'client_id')[1]

    beamoauth = authentication.OAuth(client_id, None)

    data = ['main', 'bot']
    for account in data:
        # Check account access token
        oauth_handling(account)

        # checks user information
        tmp = db.get_db('accounts', account)
        if tmp[1] is None or tmp[2] is None or tmp[6] is None:
            tmp = beamoauth.get_userinfo(tmp[3])
            db.set_db_userinfo(account, tmp)
