from lymph.web.interfaces import WebServiceInterface
from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Response


class Web(WebServiceInterface):

    url_map = Map([
        Rule('/greet', endpoint='greet'),
    ])

    def greet(self, request):
        """
        handles:
            /greet?name=<name>
        """
        name = request.args['name']
        print('About to greet %s' % name)
        greeting = self.proxy('Greeting').greet(name=name)
        return Response(greeting)
