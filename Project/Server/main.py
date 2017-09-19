# -*- coding: utf8 -*-
# DMS Web : SPA, Client-side rendering, JQuery AJAX
from flask import Flask, request
from flask_restful import Api

from routes.api.admin.account import account
# from routes.api.admin.apply_xlsx import *
# from routes.api.admin.post import *
#
# from routes.api.developer.dms import *
# from routes.api.developer.initializer import *
#
# from routes.api.student.account import *
# from routes.api.student.apply import *
# from routes.api.student.dms import *
# from routes.api.student.post import *
# from routes.api.student.school_data import *

app = Flask(__name__)
api = Api(app)

logger = None


@app.before_first_request
def before_first_request():
    from logging.handlers import RotatingFileHandler
    import logging

    def make_handler():
        handler = RotatingFileHandler('server_log.log', maxBytes=1048576, backupCount=5)
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        return handler

    def make_logger():
        app.logger.addHandler(make_handler())
        app.logger.setLevel(logging.INFO)

        return app.logger

    global logger
    logger = make_logger()
    logger.info('------ Logger started ------')


@app.before_request
def before_request():
    logger.info(f'Requested from {request.host} [ {request.method} {request.url} ]')
    logger.info(f'Request data : {request.form}')


@app.after_request
def after_request(response):
    logger.info(f'Response status : {response.status}')

    return response


@app.teardown_appcontext
def teardown_appcontext(exception):
    logger.info('--- Teardown appcontext')


def add_resources():
    api.add_resource(account.AddAccount, '/admin/add-account')


if __name__ == '__main__':
    add_resources()
    app.run()
