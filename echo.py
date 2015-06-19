import lymph


class Echo(lymph.Interface):

    @lymph.rpc()
    def echo(self, text):
        self.emit('echo', {'text': text})
        return text
