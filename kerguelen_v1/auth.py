# -*- coding: utf-8 -*-

import os

from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash

auth = HTTPBasicAuth();

USERNAME = os.environ.get('FLASK_USERNAME')
PASSWORD= os.environ.get('FLASK_PASSWORD')

@auth.verify_password
def check_security(username, password):
    if check_password_hash(USERNAME, username) and check_password_hash(PASSWORD, password):
        return True
    return False