from lymph.web.interfaces import WebServiceInterface
from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Response


class Web(WebServiceInterface):

    url_map = Map([
        Rule('/greet', endpoint='greet'),
    ])

    def greet(self, request):
        name = request.args['name']
        print('About to greet %s' % name)
        return Response(
            self.proxy('Greeting').greet(name=name)
        )
