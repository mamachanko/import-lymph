import lymph


class Echo(lymph.Interface):

    @lymph.rpc()
    def upper(self, text):
        print('echoing: %s' % text)
        self.emit('echo', {'text': text})
        return text.upper()
