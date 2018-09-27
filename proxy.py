import logging

import zmq

from discoverable import Discoverable


class Proxy(Discoverable):

    def __init__(self, service):
        super(Proxy, self).__init__()

        self.service = service
        self.name = '%s%s' % (self.__class__.__name__, service)
        self.logger = logging.getLogger(self.name)

        _ask, _tell = self.discover(self.service)
        self._init_connections(_ask, _tell)

    def _init_connections(self, ask, tell):
        try:
            self._context = zmq.Context()
            self._ask = self._context.socket(zmq.REQ)
            self._ask.setsockopt(zmq.LINGER, 0)
            self._ask.connect(ask)

            self._tell = self._context.socket(zmq.PUSH)
            self._tell.setsockopt(zmq.LINGER, 0)
            self._tell.connect(tell)
        except Exception as ex:
            self.logger.error(ex)

    def ask(self, event):
        self.logger.debug(event)
        try:
            self._ask.send_pyobj(event)
            return self._ask.recv_pyobj()
        except Exception as ex:
            self.logger.error(ex)
        return None

    def tell(self, event):
        self.logger.debug(event)
        try:
            self._tell.send_pyobj(event)
        except Exception as ex:
            self.logger.error(ex)

    def close(self):
        try:
            self._ask.close()
            self._tell.close()
            self._context.term()
        except Exception as ex:
            self.logger.error(ex)
