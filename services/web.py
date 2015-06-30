import json

from lymph.web.interfaces import WebServiceInterface
from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Response


class Web(WebServiceInterface):

    url_map = Map([
        Rule('/echo', endpoint='echo'),
    ])

    def echo(self, request):
        text = json.loads(request.get_data())['text']
        print('http echoing: %s' % text)
        echoed = self.proxy('Echo').upper(text=text)
        return Response(
            json.dumps({'text': echoed}), content_type='application/json'
        )

