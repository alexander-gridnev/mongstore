from tornado.gen import coroutine
from tornado.web import RequestHandler


class RootHandler(RequestHandler):
    @coroutine
    def get(self):
        db = self.settings['db']
        state = dict(state='connected')
        result = yield db.status.update(state, state, upsert=True)
        print(result)
        if result['err'] is None and result['ok'] == 1:
            self.write(state)
        else:
            self.write(dict(state='bad_connect'))
