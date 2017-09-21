from flask import request, session
from flask_restful import Resource

from support.user.user_manager import get_uuid_from_request

from database.mongodb import stay


class Stay(Resource):
    """
    잔류신청
    """
    def post(self):
        uid = get_uuid_from_request(request, session)
        if not uid:
            return '', 204

        value = request.form.get('value', 4, int)

        stay.remove({'uid': uid})
        stay.insert({
            'uid': uid,
            'value': value
        })

        return '', 201

    def get(self):
        uid = get_uuid_from_request(request, session)
        if not uid:
            return '', 204

        return stay.find_one({'uid': uid}, {'_id': False}), 200

    def delete(self):
        uid = get_uuid_from_request(request, session)
        if not uid:
            return '', 204

        stay.remove({'uid': uid})

        return '', 200
