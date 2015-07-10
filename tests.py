from contextlib import contextmanager
from StringIO import StringIO
import sys

from lymph.testing import (LymphServiceTestCase, EventMockTestCase,
                           WebServiceTestCase, RpcMockTestCase)
from mock import call

from greeting import Greeting
from web import Web
from listen import Listen


@contextmanager
def capture_stdout():
    real_stdout = sys.stdout
    sys.stdout = StringIO()
    try:
        yield sys.stdout
    finally:
        sys.stdout = real_stdout


class GreetingTest(LymphServiceTestCase, EventMockTestCase):
    service_class = Greeting
    service_name = u'Greeting'

    def test_says_hi(self):
        self.assertEqual(
            self.client.proxy(u'Greeting').greet(name=u'John'),
            u'Hi, John!'
        )
        self.assert_events_emitted(call(u'greeted', {u'name': u'John'}))


class ListenServiceTest(LymphServiceTestCase):
    service_class = Listen
    service_name = u'Listen'

    def test_prints(self):
        with capture_stdout() as stdout:
            self.client.emit(u'greeted', {u'name': u'John'})
        output = stdout.getvalue().strip()
        self.assertEqual(output, u'Somebody greeted John')


class WebTest(WebServiceTestCase, RpcMockTestCase):
    service_class = Web
    service_name = 'Web'

    def test_greets(self):
        self.update_rpc_mock('Greeting.greet', 'Hi, John!')
        response = self.client.post('/greet?name=John')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'Hi, John!')
