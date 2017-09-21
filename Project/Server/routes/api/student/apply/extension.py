from flask import request, session
from flask_restful import Resource

from support.user.user_manager import get_uuid_from_request

from database.mongodb import extension


class Extension(Resource):
    """
    연장신청(POST, GET, DELETE available)
    """
    def post(self):
        uuid = get_uuid_from_request(request, session)
        if not uuid:
            return '', 204

        _class = request.form.get('class')
        value = request.form.get('value', 1, int)

        extension.remove({'uuid': uuid})
        extension.insert({
            'uuid': uuid,
            'class': _class,
            'value': value
        })

        return '', 201

    def get(self):
        uuid = get_uuid_from_request(request, session)
        if not uuid:
            return '', 204

        return extension.find_one({'uuid': uuid}, {'_id': False}), 200

    def delete(self):
        uuid = get_uuid_from_request(request, session)
        if not uuid:
            return '', 204

        extension.remove({'uuid': uuid})

        return '', 200
