''' Handles the core parts of the bot '''

from datetime import datetime, timedelta
from beam_auth import OAuth
from bot_core import db
import config

CONFIG = config


def beamauth(account):
    ''' Handles all the data for Beam OAuth'''
    # creates and object for the beam oauth class
    beam_auth = OAuth.OAuth(CONFIG)

    # Checks the database if there is a valid OAuth Token
    if db.get_db('account_' + account, 'access_token')[1] is None:
        # generate shortcode and get access token if shortcode is correct
        beam_data = beam_auth.generate(None)
        # pass on informaion to check if any errors
        beamauth_data(account, beam_data)

        # gets the user id, username and channel id from beam
        beam_data = beam_auth.generate_userinfo(beam_data['access_token'])
        # pass on informaion to check if any errors
        beamauth_data(account, beam_data)

    else:
        # if an OAuth access token is saved to the database then this
        # gets the Time now and the expiry imformation of the OAuth token
        datetimemnow = datetime.now()
        datetimeexpire = datetime.strptime(db.get_db('account_' + account,
                                                     'expires_in')[1],
                                           '%Y-%m-%d %H:%M:%S.%f')

        # Check to see if the OAtuh access token has expired
        if datetimemnow > datetimeexpire:
            # OAtuh access token has expired then perform a token refresh
            print('Token expired for {acc} account,'
                  'token refreshing...'.format(acc=account))

            # refesh access token information
            beam_data = beam_auth.generate(db.get_db('account_' + account,
                                                     'refresh_token')[1])

            # pass on informaion to check if any errors
            beamauth_data(account, beam_data)


def beamauth_data(account, data):
    ''' decides what to do with the data that is recieved '''
    if data['error']:
        # if any errors then pass information to error handler
        beamauth_error(data)
    else:
        # if no errors then pass information to save to db
        beamauth_tokens(account, data)


def beamauth_error(data):
    ''' Handles all the errors that is generated by the beam OAuth '''
    if data['reason'] is not None:
        # display any errors that arises
        print(data['reason'])


def beamauth_tokens(account, data):
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


def initialize():
    ''' Checks account information in db and provides instruction for user '''
    print('Starting SpectrumBot...\n')
    data = ['main', 'bot']
    # Runs a loop for each account
    for account in data:
        # if there is not main account info then provide user instruction
        if account == 'main' and db.get_db('account_bot',
                                           'access_token')[1] is None:
            print('    Please login to your main Beam account')
            input('    Then press ENTER to continue...')
        # if there is not bot account info then provide user instruction
        elif account == 'bot' and db.get_db('account_bot',
                                            'access_token')[1] is None:
            print('    Please log out of your main Beam account'
                  'and log into your Beam bot account')
            input('    Then press ENTER to continue...')
        # run account check
        beamauth(account)
