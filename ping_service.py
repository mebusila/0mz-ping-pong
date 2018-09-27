import logging
import time

from events import PingEvent, PongEvent
from service import Service

logging.basicConfig(format='%(levelname) -7s %(asctime)s %(name) -20s'
                           ' %(funcName) -10s %(lineno) -5d: %(message)s',
                    level=logging.DEBUG)


class PingService(Service):

    def __init__(self):
        super(PingService, self).__init__()
        self._register_event(PongEvent, self.on_pong_event)

    def on_pong_event(self, event):
        self.logger.debug(event)
        time.sleep(1)
        return PingEvent()


if __name__ == '__main__':
    PingService().run()
