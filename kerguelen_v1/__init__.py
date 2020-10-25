# -*- coding: utf-8 -*-

import os
import logging, logging.handlers

from flask import Flask
from flask import redirect, url_for
from flask.logging import default_handler

def create_app(test_config = None):

    app = Flask(
        __name__,
        instance_relative_config = True
    )
    app.app_context()

    if test_config is None:
        app.logger.removeHandler(default_handler)
        logger = logging.getLogger('werkzeug')
        handler = logging.handlers.RotatingFileHandler(
            os.path.join(os.path.abspath(os.environ.get('FLASK_APP')), 'access.log'), maxBytes=1000000, backupCount=5
        )
        logger.addHandler(handler)
        app.config.from_object('kerguelen.config.DefaultConfig')
    else:
        app.config.from_mapping(test_config)

    from .kerguelen import kerguelen
    app.register_blueprint(kerguelen)

    @app.route('/')
    def index():
        return redirect(url_for('.kerguelen.camera'))

    return app