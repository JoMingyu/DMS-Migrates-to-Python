from flask import request
from flask_restful import Resource
import uuid as _uuid

from support.crypto import *

from database.mongodb import student_acc


class NewUUID(Resource):
    """
    새로운 UUID 생성(POST available)
    """
    def post(self):
        number = request.form.get('number', type=int)
        name = request.form.get('name')
        uuid = str(_uuid.uuid4())

        student_acc.insert({
            'id': None,
            'pw': None,
            'sid': None,
            'uuid': sha.encrypt(uuid),
            'number': aes.encrypt(number),
            'name': aes.encrypt(name)
        })

        return uuid, 201


class Migration(Resource):
    """
    신입생들이 들어오는 매 해마다 학번 마이그레이션'담당
    1. 데이터베이스에서 3학년 삭제
    2. legacy uuid 엑셀에서 1~2학년 학생들의 데이터를 가져옴(tuple in list)
    3. 신규 학생 데이터 엑셀에서 2~3학년 학생들의 데이터를 가져옴(tuple in list)
    4. 이름이 매칭되는 신규 학번을 가져옴
    5. uuid에 조건을 걸고 legacy 학번을 신규 학번으로 교체

    * 동명이인 문제 해결
    (1) 학번을 교체하기 위해서
    (2) 이름을 매칭하는 것이기 때문에
    이름을 임시로 수정하는 방법으로 해결 가능

    ex) 10101 김지수, 10102 김지수가 20101 김지수, 20201 김지수로 올라갔을 때
    10101 김지수와 20101 김지수가 같은 사람이라고 가정하면 임시로 양쪽 다 ' 김지수1' 이라는 이름을 지어 주고
    10102 김지수와 20201 김지수가 같은 사람이므로 임시로 양쪽 다 ' 김지수2'라는 이름을 지어 주면
    코드로서 동명이인 문제를 해결할 수 있다
    """
    _legacy_uuid_excel = 'legacy_uuid'

    def post(self):
        def remove_3rd():
            data = list(student_acc.find())
            for d in data:
                if aes.decrypt(d['number']) > 30000:
                    student_acc.remove({'number': d['number']})

        def read_legacy_data():
            data = list()
            # Some logic..
            return data

        def read_new_data():
            data = list()
            # some logic..
            return data

        def change_student_data(uuid, number_for_change):
            data = dict(student_acc.find_one({'uuid': sha.encrypt(uuid)}))
            data.update({
                'number': aes.encrypt(number_for_change)
            })

            student_acc.update({'uuid': sha.encrypt(uuid)}, data)

        remove_3rd()
        legacy_data = read_legacy_data()
        new_data = read_new_data()

        for legacy_idx, legacy in enumerate(legacy_data):
            legacy_number, legacy_name, uuid = legacy
            assert legacy_number == int

            for new_idx, new in enumerate(new_data):
                new_number, new_name = new
                assert new_number == int

                if legacy_name == new_name and legacy_number / 10000 + 1 == new_number / 10000:
                    change_student_data(uuid, new_number)

                    del legacy_data[legacy_idx]
                    del new_data[new_idx]

        return '', 201
