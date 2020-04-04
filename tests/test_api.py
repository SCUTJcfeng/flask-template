
from app import create_app

app = create_app()


class TestApi:
    """
    simple test class
    """
    def test_api(self):
        with app.test_client() as client:
            self._test_test_now(client)
            self._test_test_celery(client)

    def _validate_response(self, r):
        assert r.status_code == 200
        assert r.json['code'] == 0
        assert r.json['msg'] == 'OK'

    def _test_test_now(self, client):
        r = client.get('/v1/test/now')
        self._validate_response(r)

    def _test_test_celery(self, client):
        r = client.get('/v1/test/celery')
        self._validate_response(r)
