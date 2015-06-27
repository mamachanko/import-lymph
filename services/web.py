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
        echoed = self.proxy('Echo').echo(text=text)
        print 'http echo:', text
        return Response(
            json.dumps({'text': echoed}), content_type='application/json'
        )

