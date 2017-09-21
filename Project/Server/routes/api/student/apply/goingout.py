from flask import request, session
from flask_restful import Resource

from support.user.user_manager import get_uuid_from_request

from database.mongodb import goingout


class Goingout(Resource):
    """
    외출신청
    """
    def post(self):
        uid = get_uuid_from_request(request, session)
        if not uid:
            return '', 204

        sat = request.form.get('sat', False, bool)
        sun = request.form.get('sun', False, bool)

        goingout.remove({'uid': uid})
        goingout.insert({
            'uid': uid,
            'sat': sat,
            'sun': sun
        })

        return '', 201

    def get(self):
        uid = get_uuid_from_request(request, session)
        if not uid:
            return '', 204

        return goingout.find_one({'uid': uid}, {'_id': False}), 200

    def delete(self):
        uid = get_uuid_from_request(request, session)
        if not uid:
            return '', 204

        goingout.remove({'uid': uid})

        return '', 200
