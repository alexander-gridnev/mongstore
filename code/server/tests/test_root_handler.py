import http

from tornado.testing import gen_test
from tests.base_test_case import BaseTestCase


class RootHandlerTests(BaseTestCase):

    @gen_test
    def test_root(self):
        result, _ = yield self.fetch(self.get_url('/'))
        self.assertEqual(result, {'state': 'connected'})

    @gen_test(timeout=60)
    def test_bad_db_connection(self):
        self.mongod.stop()
        try:
            result, response = yield self.fetch(self.get_url('/'))
            self.assertEqual(result, None)
            self.assertEqual(response.code, http.client.SERVICE_UNAVAILABLE)
        finally:
            self.mongod.start()
