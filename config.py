import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = os.urandom(32)
#SECRET_KEY = "vddf2jjwm3" 

DATABASE =  os.path.join(basedir,"regression.sqlite")

USERNAME = "admin"
PASSWORD = "admin"

SESSION_TIMEOUT = 180