from flask import request, session, Response, abort
from flask_restful import Resource
import uuid

from support.user.user_manager import get_admin_id_from_request
from support.crypto import *

from database.mongodb import admin_acc


class AddAccount(Resource):
    """
    새로운 관리자 계정 추가
    """
    def post(self):
        if not get_admin_id_from_request(request, session):
            abort(403)

        _id = aes.encrypt(request.form.get('id'))
        pw = sha.encrypt(request.form.get('pw'))
        owner = aes.encrypt(request.form.get('owner', '주인 없음', str))

        if admin_acc.find_one({'id': _id}):
            # 이미 가입되어 있는 ID
            return '', 204
        else:
            admin_acc.insert({
                'id': _id,
                'pw': pw,
                'owner': owner,
                'sid': None
            })

            return '', 201


class SignIn(Resource):
    """
    관리자 계정 로그인
    """
    def post(self):
        _id = aes.encrypt(request.form.get('id'))
        pw = sha.encrypt(request.form.get('pw'))
        keep_login = request.form.get('keep_login', False, bool)

        if admin_acc.find_one({'id': _id, 'pw': pw}):
            # 로그인 성공
            resp = Response('', 201)
            sid = str(uuid.uuid4())

            if keep_login:
                # 로그인 유지 - 쿠키
                resp.set_cookie('AdminSession', sid)
            else:
                # 로그인 비유지 - 세션
                session['AdminSession'] = sid

            data = dict(admin_acc.find_one({'id': _id}))
            data.update({
                'sid': sid
            })
            admin_acc.update({'id': _id}, data)
            # SID 업데이트

            return resp
        else:
            return '', 204


class Logout(Resource):
    """
    로그아웃
    """
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
