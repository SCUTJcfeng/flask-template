
from flask import jsonify
from app.const.code import RESPONSE_OK
from app.const.code import RESPONSE_ERROR
from app.const.code import MESSAGES


def response_ok(data=None, msg=''):
    data = data if data else {}
    msg = msg if msg else MESSAGES[RESPONSE_OK]
    return _response(code=RESPONSE_OK, data=data, msg=msg)


def response_error(code=RESPONSE_ERROR, data=None, msg=''):
    data = data if data else {}
    msg = msg if msg else MESSAGES.get(code)
    return _response(code=code, data=data, msg=msg)


def _response(**kwargs):
    return jsonify(dict(**kwargs))


__all__ = (
    'response_ok',
    'response_error',
)
