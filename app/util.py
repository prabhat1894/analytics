'''
   Contains utility methods to deal with various situations
'''
__author__ = 'Ankur Srivastava'

from flask import (
        redirect,
        session,
        url_for
)
from functools import wraps
import config
import sqlite3
from app.models import Users


def getConnection():
    '''Returns a new sqlite connection to the database'''
    return sqlite3.connect(config.DATABASE)


def validate(username, password):
    '''Validates username and password
    Returns False if user name or password doesn't match'''
    user = Users.query.filter_by(username=username).filter_by(password=password).first()
    if user is None:
        return False

    return True

def authenticate(username, password):
    '''Validates username and password
    Returns False if user name or password doesn't match'''
    cursor = getConnection().cursor()
    try:
        cursor.execute('''SELECT * FROM users
                    WHERE username = ?
                    AND password = ?''',(username, password))

        if not cursor.fetchone():
            return False

        return True
   
    except sqlite3.Error:
        cursor.close()
        return False

def isLoggedIn():
    '''Checks if user is logged in.
    Session is set once for successfull login.'''


   # Check for logged_in key in session object
    if not 'logged_in' in session:
        return False

    return True

def redirectTo(url):
    '''returns redirect object to the specified URL identified by views.py'''

    return redirect(url_for(url))

def loginRequired(function):
    '''Function decorator that checks if user is logged in
    If not redirect to login page else return the function itself'''
    @wraps(function)
    def wrapper(*args, **kwargs):
        # Check and redirect to appropriate page
        if not isLoggedIn():
            return redirectTo('login')

        return function(*args, **kwargs)

    return wrapper

def count(row):
    '''Just a simple function to return the first element in list'''
    for r in row:
        return r[0]

