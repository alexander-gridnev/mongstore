from tornado.gen import coroutine
from handlers.base_handler import BaseHandler


class RootHandler(BaseHandler):

    @coroutine
    def get(self):
        state = dict(state='connected')

        with self.catch_db_errors:
            result = yield self.db.status.update(state, state, upsert=True)

        if result['err'] is None and result['ok'] == 1:
            self.write(state)
        else:
            # TODO: add test for some internal errors in db
            self.write(dict(state='errors', reponse=result))
