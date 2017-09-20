from flask import request, session, abort
from flask_restful import Resource

from support.user.user_manager import get_admin_id_from_request

from database.mongodb import notice
from pymongo.collection import ObjectId


class Notice(Resource):
    def post(self):
        if not get_admin_id_from_request(request, session):
            abort(403)

        title = request.form.get('title')
        content = request.form.get('content')
        writer = request.form.get('writer', '사감부')

        notice.insert({
            'title': title,
            'content': content,
            'writer': writer
        })

        return '', 201

    def delete(self):
        if not get_admin_id_from_request(request, session):
            abort(403)

        _id = request.form.get('_id')

        notice.remove({
            '_id': ObjectId(_id)
        })

        return '', 200

    def get(self):
        # list
        data = list(notice.find())
        for idx in range(len(data)):
            data[idx]['_id'] = str(data[idx]['_id'])

        return data, 200

    def patch(self):
        if not get_admin_id_from_request(request, session):
            abort(403)

        _id = request.form.get('_id')
        title = request.form.get('title')
        content = request.form.get('content')
        writer = request.form.get('writer', '사감부')

        notice.update({'_id': ObjectId(_id)}, {
            'title': title,
            'content': content,
            'writer': writer
        })

        return '', 200
