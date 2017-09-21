from flask import request, session, Response
from flask_restful import Resource
import uuid as _uuid

from support.user.user_manager import get_uuid_from_request
from support.crypto import *

from database.mongodb import student_acc


# 학생 계정의 구성 : uuid, 학번, 이름, id, 비밀번호, sid
class Signup(Resource):
    """
    uuid 기반 학생 회원가입(POST available)
    """
    def post(self):
        uuid = sha.encrypt(request.form.get('uuid'))
        _id = aes.encrypt(request.form.get('id'))
        pw = sha.encrypt(request.form.get('pw'))

        if not student_acc.find_one({'uuid': uuid}):
            # 1. uuid가 존재하지 않음
            return '', 204
        elif student_acc.find_one({'uuid': uuid})['id'] is not None:
            # 2. 이미 회원가입 완료된 uuid
            return '', 204
        elif student_acc.find_one({'id': _id}):
            # 3. 이미 가입되어 있는 id
            return 'c', 204

        data = student_acc.find_one({'uuid': uuid})
        data.update({
            'id': _id,
            'pw': pw
        })
        student_acc.update({'uuid': uuid}, data)

        return '', 201


class SignIn(Resource):
    """
    학생 로그인(POST available)
    """
    def post(self):
        _id = aes.encrypt(request.form.get('id'))
        pw = sha.encrypt(request.form.get('pw'))
        keep_login = request.form.get('keep_login', False, bool)

        if student_acc.find_one({'id': _id, 'pw': pw}):
            # 로그인 성공
            resp = Response('', 201)
            sid = str(_uuid.uuid4())

            if keep_login:
                # 로그인 유지 - 쿠키
                resp.set_cookie('UserSession', sid)
            else:
                # 로그인 비유지 - 세션
                session['UserSession'] = sid

            data = student_acc.find_one({'id': _id})
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
    로그아웃(POST available)
    """
    def post(self):
        uuid = get_uuid_from_request(request, session)
        if uuid:
            data = student_acc.find_one({'uuid': uuid})
            data.update({
                'sid': None
            })
            student_acc.update({'uuid': uuid}, data)

            resp = Response('', 201)
            if 'UserSession' in request.cookies:
                resp.set_cookie('UserSession', '', expires=0)
            elif 'UserSession' in session:
                session.pop('UserSession')

            return resp
        else:
            return '', 204
