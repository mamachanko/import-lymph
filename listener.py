import lymph


class Listener(lymph.Interface):

    @lymph.event('echo')
    def on_echo(self, event):
        print 'echoed text {}'.format(event['text'])
