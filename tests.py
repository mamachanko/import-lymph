from lymph.testing import (LymphServiceTestCase, EventMockTestCase,
                           WebServiceTestCase, RpcMockTestCase)
from mock import call

from echo import Echo
from web import Web


class EchoTest(LymphServiceTestCase, EventMockTestCase):
    service_class = Echo
    service_name = 'Echo'

    def test_echoes(self):
        self.assertEqual(
            self.client.proxy(u'Echo').upper(text=u'hi'),
            u'HI'
        )
        self.assert_events_emitted(call('echo', {'text': 'hi'}))


class WebTest(WebServiceTestCase, RpcMockTestCase):
    service_class = Web
    service_name = 'Web'

    def test_post(self):
        self.update_rpc_mock('Echo.echo', 'HI!')
        response = self.client.post('/echo', data='{"text": "hi"}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, '{"text": "HI!"}')
