import json

from tornado.testing import AsyncHTTPTestCase
from tornado.testing import gen_test
from tornado.gen import coroutine

from app import init
from common import utils


class RootHandlerTests(AsyncHTTPTestCase):
    def get_app(self):
        return init()

    @coroutine
    def fetch(self, url):
        response = yield self.http_client.fetch(url)
        data = json.loads(utils.to_str(response.body))
        return data, response

    @gen_test
    def test_root(self):
        result, _ = yield self.fetch(self.get_url('/'))
        self.assertEqual(result, {'state': 'connected'})
