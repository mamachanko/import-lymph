import json

from lymph.web.interfaces import WebServiceInterface
from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Response


class Web(WebServiceInterface):

    http_port = 4080
    pool_size = 2
    url_map = Map([
        Rule('/echo', endpoint='echo'),
    ])

    def echo(self, request):
        post_data = json.loads(request.get_data())
        text = post_data['text']
        echoed = self.proxy('Echo').echo(text=text)
        return Response(
            json.dumps({'echoed': echoed}),
            content_type='application/json'
        )

