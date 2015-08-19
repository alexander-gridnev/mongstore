import motor
import config

from db_client.client import DBClient
from handlers.root_handler import RootHandler

from tornado.ioloop import IOLoop
from tornado.web import Application


def init():
    client = motor.MotorClient(config.MONGO_URL)
    db = client[config.MONGO_DB_NAME]
    db_wrapper = DBClient(db)

    application = Application([
        (r'/', RootHandler)
    ], _db=db, db=db_wrapper)

    return application


if __name__ == 'main':
    init().listen(config.APP_PORT)
    io = IOLoop.instance()
    io.start()
