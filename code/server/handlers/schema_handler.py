import json
import http

from tornado.gen import coroutine
from handlers.base_handler import BaseHandler
from common.utils import to_str
from tornado.web import HTTPError


class SchemaHandler(BaseHandler):

    @coroutine
    def get(self):
        cursor = self.db.schemas.find()

        with self.catch_db_errors:
            schemas = yield self.paginate(cursor)

        self.write(dict(
            schemas={schema['_id']: schema['schema'] for schema in schemas}
        ))

    @coroutine
    def post(self, name):
        schema = json.loads(to_str(self.request.body))
        schema_obj = dict(
            _id=name,
            schema=schema
        )
        with self.catch_db_errors:
            yield self.db.schemas.insert(schema_obj)

        self.set_status(http.client.CREATED)
        self.write(schema)

    @coroutine
    def delete(self, name):

        with self.catch_db_errors:
            result = yield self.db.schemas.remove({'_id': name})

        if result['n'] == 0:
            raise HTTPError(http.client.NOT_FOUND)
