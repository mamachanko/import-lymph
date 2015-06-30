from kazoo.client import KazooClient


zk = KazooClient('zk:2181')
zk.start()
zk.delete('/lymph', recursive=True)
zk.stop()
