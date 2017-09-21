from flask import request, session
from flask_restful import Resource

from support.user.user_manager import get_uid_from_request

from database.mongodb import extension


class Extension(Resource):
    """
    연장신청
    """
    def post(self):
        uid = get_uid_from_request(request, session)
        if not uid:
            return '', 204

        _class = request.form.get('class')
        value = request.form.get('value', 1, int)

        extension.remove({'uid': uid})
        extension.insert({
            'uid': uid,
            'class': _class,
            'value': value
        })

        return '', 201

    def get(self):
        uid = get_uid_from_request(request, session)
        if not uid:
            return '', 204

        return dict(extension.find_one({'uid': uid}, {'_id': False})), 200

    def delete(self):
        uid = get_uid_from_request(request, session)
        if not uid:
            return '', 204

        extension.remove({'uid': uid})

        return '', 200
