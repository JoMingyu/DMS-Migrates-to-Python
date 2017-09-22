from flask import request, session, abort
from flask_restful import Resource

from support.user.user_manager import get_uuid_from_request

from database.mongodb import afterschool, afterschool_item
from pymongo.collection import ObjectId


class Afterschool(Resource):
    """
    방과후 아이템(POST available)
    """
    def get(self):
        data = list(afterschool_item.find())
        for idx, d in enumerate(data):
            data[idx]['_id'] = str(d['_id'])

        return data


class AfterschoolApply(Resource):
    def post(self):
        uuid = get_uuid_from_request(request, session)
        if not uuid:
            return '', 204

        afterschool.remove({'uuid': uuid})
        ids = request.json
        for _id in ids:
            if not afterschool_item.find_one({'_id': ObjectId(_id)}):
                # 존재하지 않는 방과후 아이템인 경우
                continue

            afterschool.insert({
                'uuid': uuid,
                'value': _id
            })

        return '', 201

    def get(self):
        uuid = get_uuid_from_request(request, session)
        if not uuid:
            return '', 204

        data = list(afterschool.find({'uuid': uuid}))
        for idx, d in enumerate(data):
            data[idx]['_id'] = str(d['_id'])

        return data
