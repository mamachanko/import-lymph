import lymph


class Listen(lymph.Interface):

    @lymph.event('greeted')
    def on_greeted(self, event):
        print('Somebody greeted %s' % event['name'])
