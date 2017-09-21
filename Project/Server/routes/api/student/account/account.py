from flask import request, session, Response
from flask_restful import Resource
import uuid

from support.user.user_manager import get_uid_from_request
from support.crypto import *

from database.mongodb import student_acc


# 학생 계정의 구성 : uuid, 학번, 이름, id, 비밀번호, sid
class Signup(Resource):
    """
    uuid 기반 학생 회원가입
    """
    def post(self):
        _uuid = sha.encrypt(request.form.get('_uuid'))
        _id = aes.encrypt(request.form.get('id'))
        pw = sha.encrypt(request.form.get('pw'))

        if not student_acc.find_one({'uuid': _uuid}):
            # 1. uuid가 존재하지 않음
            return '', 204
        elif student_acc.find_one({'uuid': _uuid})['id'] is not None:
            # 2. 이미 회원가입 완료된 uuid
            return '', 204
        elif student_acc.find_one({'id': _id}):
            # 3. 이미 가입되어 있는 id
            return '', 204

        data = dict(student_acc.find_one({'uuid': _uuid}))
        data.update({
            'id': _id,
            'pw': pw
        })

        return '', 201


class SignIn(Resource):
    """
    학생 로그인
    """
    def post(self):
        _id = aes.encrypt(request.form.get('id'))
        pw = sha.encrypt(request.form.get('pw'))
        keep_login = request.form.get('keep_login', False, bool)

        if student_acc.find_one({'id': _id, 'pw': pw}):
            # 로그인 성공
            resp = Response('', 201)
            sid = str(uuid.uuid4())

            if keep_login:
                # 로그인 유지 - 쿠키
                resp.set_cookie('UserSession', sid)
            else:
                # 로그인 비유지 - 세션
                session['UserSession'] = sid

            data = dict(student_acc.find_one({'id': _id}))
            data.update({
                'sid': sid
            })
            student_acc.update({'id': _id}, data)
            # SID 업데이트

            return resp
        else:
            return '', 204


class Logout(Resource):
    """
    로그아웃
    """
    def post(self):
        uid = get_uid_from_request(request, session)
        if uid:
            data = dict(student_acc.find_one({'uid': uid}))
            data.update({
                'sid': None
            })
            student_acc.update({'uid': uid}, data)

            resp = Response('', 201)
            if 'UserSession' in request.cookies:
                resp.set_cookie('UserSession', '', expires=0)
            elif 'UserSession' in session:
                session.pop('UserSession')

            return resp
        else:
            return '', 204
