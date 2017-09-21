from flask import request, session
from flask_restful import Resource

from support.user.user_manager import get_admin_id_from_request
from support.crypto import *

from database.mongodb import student_acc


class InitializeStudent(Resource):
    """
    학생 계정을 재가입 가능하도록 초기화(POST available)
    """
    def post(self):
        if not get_admin_id_from_request(request, session):
            return '', 403

        number = aes.encrypt(request.form.get('number', type=int))

        data = student_acc.find_one({'number': number})
        data.update({
            'id': None,
            'pw': None,
            'sid': None
        })
        student_acc.update({'number': number}, data)

        return '', 201
