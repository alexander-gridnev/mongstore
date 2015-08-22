import http

from tornado.testing import gen_test
from tests.base_test_case import BaseTestCase


class SchemaHandlerTests(BaseTestCase):
    test_schema = {
        'type': 'object',
        'properties': {
            'test': {'type': 'string'},
            'some': {'type': 'number'}
        }
    }

    @gen_test
    def test_get(self):
        result, _ = yield self.fetch(self.get_url('/_schemas'))
        self.assertEqual(result, {'schemas': {}})

    @gen_test
    def test_post(self):
        result, response = yield self.fetch(
            self.get_url('/_schemas/test'),
            'POST',
            body=self.test_schema)

        self.assertEqual(response.code, http.client.CREATED)
        self.assertEqual(result, self.test_schema)

        result, _ = yield self.fetch(self.get_url('/_schemas'))
        print(result)
        self.assertEqual(result, {'schemas': dict(test=self.test_schema)})

    @gen_test
    def test_list(self):
        for i in range(10):
            result, response = yield self.fetch(
                self.get_url('/_schemas/test%s' % i),
                'POST',
                body=self.test_schema)

            self.assertEqual(response.code, http.client.CREATED)
            self.assertEqual(result, self.test_schema)

        result, _ = yield self.fetch(self.get_url('/_schemas'))
        self.assertEqual(result, {
            'schemas': {'test%s' % i: self.test_schema for i in range(10)}
        })

    @gen_test
    def test_delete(self):
        result, response = yield self.fetch(
            self.get_url('/_schemas/test'),
            'DELETE')

        self.assertEqual(response.code, http.client.NOT_FOUND)
        self.assertEqual(result, None)

        result, response = yield self.fetch(
            self.get_url('/_schemas/test'),
            'POST',
            body=self.test_schema)

        result, response = yield self.fetch(
            self.get_url('/_schemas/test'),
            'DELETE')

        self.assertEqual(response.code, http.client.OK)
        self.assertEqual(result, None)
