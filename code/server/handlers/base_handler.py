from tornado.web import RequestHandler
from db_client.client import catch_db_errors


class BaseHandler(RequestHandler):

    @property
    def db(self):
        return self.settings['db']

    @property
    def catch_db_errors(self):
        return catch_db_errors()

    def paginate(self, cursor):
        offset = int(self.get_query_argument('offset', 0))
        size = int(self.get_query_argument('size', 10))
        cursor.limit(size).skip(offset)
        return cursor.to_list(length=size)
