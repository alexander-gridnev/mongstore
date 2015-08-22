import pytest
import subprocess
import tempfile
import shutil
import os
import config
import time
import pymongo


@pytest.fixture(scope='session')
def mongod(request):
    subprocess.call(['pkill', '-f', 'mongod*tmp'])
    server = MongoServer()
    server.start()

    def stop():
        server.stop()
        server.clean()

    request.addfinalizer(stop)

    from tests.base_test_case import BaseTestCase
    BaseTestCase.mongod = server
    return server


@pytest.fixture(scope='session')
def exclusive_tests(request):
    subprocess.call(['pkill', '-f', 'code/server/app.py'])


class MongoServer(object):

    def __init__(self):
        self.tmp_path = tempfile.mkdtemp()
        self.db_path = os.path.join(self.tmp_path, 'db')
        os.mkdir(self.db_path)

    def start(self):
        self.server = subprocess.Popen(
            ['mongod', '--dbpath', self.db_path, '--port',
             str(config.MONGO_PORT), '--smallfiles']
        )
        self.wait_alive()

    def stop(self):
        self.server.terminate()
        self.server.wait()

    def clean(self):
        shutil.rmtree(self.tmp_path)

    def drop_db(self):
        client = pymongo.MongoClient(config.MONGO_URL())
        client.drop_database(config.MONGO_DB_NAME)

    def wait_alive(self):
        while True:
            try:
                client = pymongo.MongoClient(config.MONGO_URL())
                result = client.admin.command('ping')
                if result['ok']:
                    break
            except:
                pass

            time.sleep(0.1)
