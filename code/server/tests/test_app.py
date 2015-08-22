import http
import time
import signal

import subprocess
from tests.base_test_case import BaseTestCase
from tornado.testing import gen_test


class AppTests(BaseTestCase):

    @gen_test(timeout=10)
    def test_app_start(self):
        port = 5555
        success = {'state': 'connected'}

        p = subprocess.Popen(
            ['.store/bin/python', 'code/server/app.py'],
            env={'STORE_PORT': str(port)}
        )

        try:

            obj, res = None, None

            while p.poll() is None:
                try:
                    obj, res = yield self.fetch('http://localhost:%s' % port)
                except:
                    continue

                if res.code == http.client.OK and obj == success:
                    break

                time.sleep(1)

            self.assertEqual(obj, success)
            self.assertEqual(res.code, http.client.OK)

        finally:
            if p.poll() is None:
                p.send_signal(signal.SIGINT)
                p.wait()
