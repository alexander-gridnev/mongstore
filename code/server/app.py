import motor
import config
import logging

from db_client.client import DBClient
from handlers.root_handler import RootHandler
from handlers.schema_handler import SchemaHandler

from tornado.ioloop import IOLoop
from tornado.web import Application


logging.basicConfig(
    format='%(levelname)-8s [%(asctime)s][%(name)s] %(message)s',
    level=logging.WARNING
)


def init():
    client = motor.MotorClient(config.MONGO_URL())
    db = client[config.MONGO_DB_NAME]
    db_wrapper = DBClient(db)

    application = Application([
        (r'/', RootHandler),
        (r'/_schemas', SchemaHandler),
        (r'/_schemas/(.*)', SchemaHandler)
    ], _db=db, db=db_wrapper)

    return application


def start_app():
    init().listen(config.APP_PORT)
    io = IOLoop.instance()
    io.start()


if __name__ == '__main__':
    start_app()
