from lymph.testing import (LymphServiceTestCase, EventMockTestCase,
                           WebServiceTestCase, RpcMockTestCase)
from mock import call

from greeting import Greeting
from web import Web


class GreetingTest(LymphServiceTestCase, EventMockTestCase):
    service_class = Greeting
    service_name = u'Greeting'

    def test_says_hi(self):
        self.assertEqual(
            self.client.proxy(u'Greeting').greet(name=u'John'),
            u'Hi, John!'
        )
        self.assert_events_emitted(call(u'greeting', {u'name': u'John'}))


class WebTest(WebServiceTestCase, RpcMockTestCase):
    service_class = Web
    service_name = 'Web'

    def test_post(self):
        self.update_rpc_mock('Greeting.greet', 'Hi, John!')
        response = self.client.post('/greet?name=John')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'Hi, John!')
