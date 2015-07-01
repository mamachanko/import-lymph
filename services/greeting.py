import lymph


class Greeting(lymph.Interface):

    @lymph.rpc()
    def greet(self, name):
        print('Saying hi to %s' % name)
        self.emit('greeting', {'name': name})
        return u'Hi, %s!' % name
