''' handles all the database data flow '''

import sqlite3

CONN = sqlite3.connect('database/db.db')

def get_db(table, data):
    ''' Gets the requested information from the database '''
    database = CONN.cursor()
    database.execute("SELECT * FROM {table} WHERE id = '{data}'".format(
        table=table, data=data))
    return database.fetchone()

def set_db(table, data, row):
    ''' Changes values in the database and commits changes '''
    database = CONN.cursor()
    database.execute("UPDATE {table} SET {data} WHERE id='{row}'".format(
        table=table, data=data, row=row))
    CONN.commit()

def set_db_userinfo(account, data):
    ''' Saves the account information to the database '''
    data = ("username='{n}', ".format(n=data['username']) +
            "user_id='{uid}', ".format(uid=data['channel']['id']) +
            "channel_id='{cid}'".format(cid=data['channel']['userId']))
    set_db('accounts', data, account)
