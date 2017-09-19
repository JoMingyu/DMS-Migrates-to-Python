from flask import request, session, Response
from flask_restful import Resource
import uuid

from support.user.user_manager import get_admin_id_from_request
from support.crypto import *

from database.mongodb import admin_acc


class AddAccount(Resource):
    def post(self):
        if not get_admin_id_from_request(request, session):
            return '', 403

        _id = aes.encrypt(request.form.get('id'))
        pw = sha.encrypt(request.form.get('pw'))
        owner = aes.encrypt(request.form.get('owner', '주인 없음', str))

        if admin_acc.find_one({'id': _id}):
            return '', 204
        else:
            admin_acc.insert({
                'id': _id,
                'pw': pw,
                'owner': owner
            })

            return '', 201


class SignIn(Resource):
    def post(self):
        _id = aes.encrypt(request.form.get('id'))
        pw = sha.encrypt(request.form.get('pw'))
        keep_login = request.form.get('keep_login', False, bool)

        if admin_acc.find_one({'id': _id, 'pw': pw}):
            resp = Response('', 201)
            sid = str(uuid.uuid4())
            if keep_login:
                resp.set_cookie('AdminSession', sid)
            else:
                session['AdminSession'] = sid

            return resp
        else:
            return '', 204


class Logout(Resource):
    def post(self):
        if get_admin_id_from_request(request, session):
            resp = Response('', 201)
            if 'AdminSession' in request.cookies:
                resp.set_cookie('AdminSession', '', expires=0)
            elif 'AdminSession' in session:
                session.pop('AdminSession')

            return resp
        else:
            return '', 204
