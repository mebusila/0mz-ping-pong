import random
import socket

import redis


class Discoverable:

    def __init__(self):
        self._r = redis.StrictRedis(host='redis', port=6379, db=0)

    def discover(self, service):
        _ask = self._r.get('%s_ask' % service)
        _tell = self._r.get('%s_tell' % service)

        return _ask, _tell

    def register(self, service):
        _address = socket.gethostbyname(socket.gethostname())
        _ask = 'tcp://%s:%s' % (_address, random.randint(7000, 8000))
        _tell = 'tcp://%s:%s' % (_address, random.randint(5000, 6000))

        self._r.set('%s_ask' % service, _ask)
        self._r.set('%s_tell' % service, _tell)

        return _ask, _tell
