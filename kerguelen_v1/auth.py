# -*- coding: utf-8 -*-

from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash

auth = HTTPBasicAuth();

USERNAME = 'pbkdf2:sha256:150000$bx2lNwuv$f9d9d721408e61b754af049428defda606cac876f6404c9f47fa963d4560c7bd'
PASSWORD = 'pbkdf2:sha256:150000$kpjKcRG2$683bc1759a12a48e15dcce40ee2e6da7352ddf49e89f5cf08c3b71faccaee8d1'

@auth.verify_password
def check_security(username, password):
    if check_password_hash(USERNAME, username) and check_password_hash(PASSWORD, password):
        return True
    return False