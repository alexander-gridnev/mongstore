import config

from copy import copy


class DBClient(object):
    def __init__(self, db):
        self.__db = db

    def safe(self, kwargs):
        _kwargs = copy(kwargs)
        _kwargs['w'] = config.MONGO_DB_WRITE_CONCERN
        _kwargs['j'] = config.MONGO_DB_JOURNAL
        _kwargs['wtimeout'] = config.MONGO_DB_TIMEOUT
        _kwargs['fsync'] = config.MONGO_FSYNC

        return _kwargs

    def insert(self, *args, **kwargs):
        return self.__db.insert(*args, **self.safe(kwargs))

    def update(self, *args, **kwargs):
        return self.__db.update(*args, **self.safe(kwargs))

    def __getattr__(self, attrib):
        return getattr(self.__db, attrib)
