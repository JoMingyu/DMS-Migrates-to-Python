from flask import request, session, abort
from flask_restful import Resource

from support.user.user_manager import get_admin_id_from_request

from database.mongodb import afterschool_item


class AfterschoolItem(Resource):
    """
    방과후 아이템(POST, GET available)
    """
    def post(self):
        if not get_admin_id_from_request(request, session):
            abort(403)

        afterschool_item.remove()

        afterschool_data = request.json
        for afterschool in afterschool_data:
            title, on_monday, on_tuesday, on_saturday = afterschool.values()
            afterschool_item.insert({
                'title': title,
                'on_monday': on_monday,
                'on_tuesday': on_tuesday,
                'on_saturday': on_saturday
            })

        return '', 201

    def get(self):
        if not get_admin_id_from_request(request, session):
            abort(403)

        data = list(afterschool_item.find())
        for idx, d in enumerate(data):
            data[idx]['_id'] = str(d['_id'])

        return data
