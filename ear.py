import lymph


class Ear(lymph.Interface):

    @lymph.event('echo')
    def on_echo(self, event):
        print 'consumed echo:', event['text']
