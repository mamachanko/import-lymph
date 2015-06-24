import lymph


class Echo(lymph.Interface):

    @lymph.rpc()
    def echo(self, text):
        print 'echoing:', text
        self.emit('echo', {'text': text})
        return text
