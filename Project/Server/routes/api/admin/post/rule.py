from flask import request, session, abort
from flask_restful import Resource

from support.user.user_manager import get_admin_id_from_request

from database.mongodb import rule
from pymongo.collection import ObjectId


class Rule(Resource):
    """
    Rule(POST, DELETE, GET, PATCH available)
    """
    def post(self):
        if not get_admin_id_from_request(request, session):
            abort(403)

        title = request.form.get('title')
        content = request.form.get('content')

        rule.insert({
            'title': title,
            'content': content
        })

        return '', 201

    def delete(self):
        if not get_admin_id_from_request(request, session):
            abort(403)

        _id = request.form.get('_id')

        rule.remove({
            '_id': ObjectId(_id)
        })

        return '', 200

    def get(self):
        # list
        data = list(rule.find())
        for idx in range(len(data)):
            data[idx]['_id'] = str(data[idx]['_id'])

        return data, 200

    def patch(self):
        if not get_admin_id_from_request(request, session):
            abort(403)

        _id = request.form.get('_id')
        title = request.form.get('title')
        content = request.form.get('content')

        rule.update({'_id': ObjectId(_id)}, {
            'title': title,
            'content': content
        })

        return '', 200
