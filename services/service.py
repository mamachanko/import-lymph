# service.py
import lymph 


class Service(lymph.Interface):

    def apply_config(self, config):
        super(Service, self).apply_config(config)
        self.cache_client = config.get_instance('cache_client')

    def on_start(self):
        super(Service, self).on_start()
        print('started with client: %s' % self.cache_client)

    def on_stop(self):
        print('stopping...')
        super(Service, self).on_stop()
