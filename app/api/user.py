
from flask import Blueprint

from app.util.restful import Api
from app.util.restful import Resource
from app.util.response import response_ok
from app.model import User


bp = Blueprint('user', __name__)
url_prefix = '/user'
api = Api(bp)


class UserResource(Resource):

    @staticmethod
    def get():
        query = User.query.order_by(User.id)
        name_list = [r.username for r in query]
        return response_ok(name_list)

    @staticmethod
    def post():
        return response_ok()


api.add_resource(UserResource, '/name')
