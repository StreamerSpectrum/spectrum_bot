''' handles all the database data flow '''

import sqlite3
CONN = sqlite3.connect('Data/Database/db.sqlite3')


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


def set_db_userdata(account, data):
    ''' Saves the account information to the database '''
    for ids in data:
        set_db('account_' + account, "data='" + data[ids].__str__() + "'", ids)
