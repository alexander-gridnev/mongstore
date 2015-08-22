import config
import http

from tornado.web import HTTPError
from pymongo.errors import ConnectionFailure

from contextlib import contextmanager


@contextmanager
def catch_db_errors():
    try:
        yield
    except ConnectionFailure:
        raise HTTPError(http.client.SERVICE_UNAVAILABLE)


class DBClient(object):

    def __init__(self, db):
        self.__db = db
        self.__db.write_concern = {
            'w': config.MONGO_DB_WRITE_CONCERN,
            'j': config.MONGO_DB_JOURNAL,
            'wtimeout': config.MONGO_DB_TIMEOUT,
            'fsync': config.MONGO_FSYNC
        }

    def __getattr__(self, attrib):
        return getattr(self.__db, attrib)
