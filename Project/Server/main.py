# -*- coding: utf8 -*-
# DMS Web : SPA, Client-side rendering, JQuery AJAX
from flask import Flask, request
from flask_restful import Api

from routes.api import *

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


def add_admin_resources():
    from routes.api.admin.account import account, initializer
    from routes.api.admin.apply_xlsx import afterschool_xlsx, extension_xlsx, goingout_xlsx, report_facility_xlsx, stay_xlsx
    from routes.api.admin.post import faq, notice, rule

    api.add_resource(account.AddAccount, '/admin/add-account')
    api.add_resource(account.AdminSignIn, '/admin/signin')
    api.add_resource(account.AdminLogout, '/admin/logout')
    api.add_resource(initializer.InitializeStudent, '/admin/initialize-student')

    api.add_resource(faq.FAQ, '/admin/faq')
    api.add_resource(notice.Notice, '/admin/notice')
    api.add_resource(rule.Rule, '/admin/rule')


def add_developer_resources():
    from routes.api.developer.dms import bug_report
    from routes.api.developer.initializer import account

    api.add_resource(account.NewUUID, '/developer/new-uuid')
    api.add_resource(account.Migration, '/developer/migration')


def add_student_resources():
    from routes.api.student.account import account
    from routes.api.student.apply import afterschool, extension, goingout, stay
    from routes.api.student.post import faq, notice, rule

    api.add_resource(account.Signup, '/signup')
    api.add_resource(account.SignIn, '/signin')
    api.add_resource(account.Logout, '/logout')

    api.add_resource(extension.Extension, '/extension')
    api.add_resource(goingout.Goingout, '/goingout')
    api.add_resource(stay.Stay, '/stay')


if __name__ == '__main__':
    add_admin_resources()
    add_developer_resources()
    add_student_resources()

    app.secret_key = 'qlalfclsrn'
    app.run()
