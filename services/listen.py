import lymph


class Listen(lymph.Interface):

    @lymph.event('greeted')
    def on_greeting(self, event):
        print('Somebody greeted  %s' % event['name'])
