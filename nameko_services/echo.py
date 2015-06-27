from nameko.rpc import rpc


class EchoService(object):
    name = 'echo_service'

    @rpc
    def echo(self, text):
        return text

    @rpc
    def upper(self, text):
        return text.upper()
