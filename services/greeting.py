import lymph


class Greeting(lymph.Interface):

    @lymph.rpc()
    def greet(self, name):
        """ Returns a greeting for a provided name.
        """
        print('Saying hi to %s' % name)
        self.emit('greeted', {'name': name})
        return u'Hi, %s!' % name
