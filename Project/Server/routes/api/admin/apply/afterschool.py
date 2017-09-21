from flask import request, Session, abort
from flask_restful import Resource

from support.user.user_manager import get_admin_id_from_request

from database.mongodb import afterschool_item


class AfterschoolItem(Resource):
    pass
