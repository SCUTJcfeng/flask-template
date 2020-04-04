
from flask import Blueprint

from app.util.restful import Api
from app.util.restful import Resource
from app.task import system_notice_task
from app.util.response import response_ok
from app.util.time import current_timestamp


bp = Blueprint('test', __name__)
url_prefix = '/test'
api = Api(bp)


class TestTimeResource(Resource):

    @staticmethod
    def get():
        return response_ok(current_timestamp())


class TestCeleryResource(Resource):

    @staticmethod
    def get():
        system_notice_task.delay('test celery task')
        return response_ok()


api.add_resource(TestTimeResource, '/now')
api.add_resource(TestCeleryResource, '/celery')
