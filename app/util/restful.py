
import flask_restful


class Api(flask_restful.Api):
    def error_router(self, original_handler, e):
        return original_handler(e)


class Resource(flask_restful.Resource):
    """全局权限验证"""


__all__ = (
    'Api',
    'Resource',
)
