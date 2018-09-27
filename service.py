import logging

import zmq

from discoverable import Discoverable
from events import SubscribeEvent, StopEvent
from proxy import Proxy


class Service(Discoverable):

    def __init__(self):
        super(Service, self).__init__()

        self.logger = logging.getLogger(self.__class__.__name__)

        self._is_running = False
        self._events_handlers = {}
        self._subscribers = {}

        self._register_event(StopEvent, self.on_stop_event)
        self._register_event(SubscribeEvent, self.on_subscribe_event)

        _ask, _tell = self.register(self.__class__.__name__)
        self._init_connections(_ask, _tell)

    def _init_connections(self, ask, tell):
        self.logger.debug(ask)
        self.logger.debug(tell)

        try:
            self._context = zmq.Context()

            self._ask = self._context.socket(zmq.REP)
            self._ask.bind(ask)

            self._tell = self._context.instance().socket(zmq.PULL)
            self._tell.bind(tell)

            self._poller = zmq.Poller()
            self._poller.register(self._ask, zmq.POLLIN)
            self._poller.register(self._tell, zmq.POLLIN)
        except Exception as ex:
            self.logger.error(ex)

    def _register_event(self, event, handler):
        self._events_handlers[event] = handler

    def stop(self):
        self._poller.unregister(self._ask)
        self._ask.close()

        self._poller.unregister(self._tell)
        self._tell.close()

        self._context.term()

        for _subscriber in self._subscribers.values():
            _subscriber.get('proxy').close()

    def on_stop_event(self, event):
        self.logger.debug(event)
        self._is_running = False

    def on_subscribe_event(self, event):
        self.logger.debug(event)
        self._subscribers[event.service] = {
            'proxy': Proxy(event.service),
            'topics': event.topics
        }

    def on_event(self, event):
        result = None
        if type(event) in self._events_handlers:
            handler = self._events_handlers[type(event)]
            try:
                result = handler(event)
            except Exception as ex:
                self.logger.error(ex)
        return result

    def ask(self, event):
        self.logger.debug(event)
        return self.on_event(event)

    def tell(self, event):
        self.logger.debug(event)
        result = self.on_event(event)
        if result:
            self.broadcast(result)

    def broadcast(self, event):
        self.logger.debug(event)
        for _subscriber in self._subscribers.values():
            if type(event) in _subscriber.get('topics'):
                _subscriber.get('proxy').tell(event)

    def run(self):
        self._is_running = True
        while self._is_running:
            try:
                __items = dict(self._poller.poll())

                if __items.get(self._ask) == zmq.POLLIN:
                    event = self._ask.recv_pyobj(flags=zmq.NOBLOCK)
                    event = self.ask(event)
                    self._ask.send_pyobj(event)

                if __items.get(self._tell) == zmq.POLLIN:
                    event = self._tell.recv_pyobj(flags=zmq.NOBLOCK)
                    if event:
                        self.tell(event)
            except KeyboardInterrupt:
                self.tell(StopEvent())
        self.stop()
