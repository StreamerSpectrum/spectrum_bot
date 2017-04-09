''' Handles the core parts of the bot '''

from datetime import datetime, timedelta
from BeamAuth import OAuth
from BotCore import db
import config

def _beamauthdata(account, data):
    if data['error']:
        # if any errors then pass information to error handler
        beamautherror(data)
    else:
        # if no errors then pass information to save to db
        beamauthtokens(account, data)

def beamautherror(data):
    ''' Handles all the errors that is generated by the beam OAuth '''
    if data['reason'] is not None:
        # display any errors that arises
        print(data['reason'])

def beamauthtokens(account, data):
    ''' Handles the access token information and saves to database '''
    if 'expires_in' in data:
        # setting a temp viariable to the data passed to function
        tmp = data

        # adds the 'expires_in' to the current date and time
        dte = datetime.now() + timedelta(seconds=data['expires_in'])

        # updates the access token expiry to date and time format
        tmp['expires_in'] = dte.__str__()

    # saves access token information to db
    db.set_db_userdata(account, data)

def beamauth(account, conf=config):
    ''' Handles all the data for Beam OAuth'''
    # creates and object for the beam oauth class
    bauth = OAuth.OAuth(conf)

    # Checks the database if there is a valid OAuth Token
    if db.get_db('account_' + account, 'access_token')[1] is None:
        # generate shortcode and get access token if shortcode is correct
        beam_data = bauth.generate(None)

        # pass on informaion to check if any errors
        _beamauthdata(account, beam_data)

        # gets the user id, username and channel id from beam
        beam_data_b = bauth.generate_userinfo(beam_data['access_token'])
        # pass on informaion to check if any errors
        _beamauthdata(account, beam_data_b)

    else:
        # if an OAuth access token is saved to the database then this
        # gets the Time now and the expiry imformation of the OAuth token
        datetimemnow = datetime.now()
        datetimeexpire = datetime.strptime(db.get_db('account_' + account, 'expires_in')[1],
                                           '%Y-%m-%d %H:%M:%S.%f')

        # Check to see if the OAtuh access token has expired
        if datetimemnow > datetimeexpire:
            # OAtuh access token has expired then perform a token refresh
            print('Token expired for {acc} account, token refreshing...'.format(acc=account))

            # refesh access token information
            beam_data = bauth.generate(db.get_db('account_' + account, 'refresh_token')[1])

            # pass on informaion to check if any errors
            _beamauthdata(account, beam_data)
