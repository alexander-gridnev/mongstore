import json
import pytest

from tornado.testing import AsyncHTTPTestCase
from tornado.gen import coroutine
from tornado.httpclient import HTTPError, HTTPRequest

from app import init
from common import utils


@pytest.mark.usefixtures('exclusive_tests', 'mongod')
class BaseTestCase(AsyncHTTPTestCase):

    def get_app(self):
        return init()

    def prepare_body(self, body):
        if body is None:
            return

        return json.dumps(body)

    def setUp(self):
        self.mongod.drop_db()
        super(BaseTestCase, self).setUp()

    def tearDown(self):
        super(BaseTestCase, self).tearDown()

    @coroutine
    def fetch(self, url, method='GET', body=None, headers=None):
        request = HTTPRequest(
            url,
            method=method,
            headers=headers,
            body=self.prepare_body(body)
        )

        try:
            response = yield self.http_client.fetch(request)
        except HTTPError as e:
            return None, e.response

        if response.body:
            data = json.loads(utils.to_str(response.body))
        else:
            data = None

        return data, response
