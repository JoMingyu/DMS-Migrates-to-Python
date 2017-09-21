from flask import request, session
from flask_restful import Resource

from support.user.user_manager import get_uuid_from_request

from database.mongodb import stay


class Stay(Resource):
    """
    잔류신청
    """
    def post(self):
        uuid = get_uuid_from_request(request, session)
        if not uuid:
            return '', 204

        value = request.form.get('value', 4, int)

        stay.remove({'uuid': uuid})
        stay.insert({
            'uuid': uuid,
            'value': value
        })

        return '', 201

    def get(self):
        uuid = get_uuid_from_request(request, session)
        if not uuid:
            return '', 204

        return stay.find_one({'uuid': uuid}, {'_id': False}), 200

    def delete(self):
        uuid = get_uuid_from_request(request, session)
        if not uuid:
            return '', 204

        stay.remove({'uuid': uuid})

        return '', 200
