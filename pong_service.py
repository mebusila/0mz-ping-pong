import logging
import time

from events import PongEvent, PingEvent
from service import Service

logging.basicConfig(format='%(levelname) -7s %(asctime)s %(name) -20s'
                           ' %(funcName) -10s %(lineno) -5d: %(message)s',
                    level=logging.DEBUG)


class PongService(Service):

    def __init__(self):
        super(PongService, self).__init__()
        self._register_event(PingEvent, self.on_ping_event)

    def on_ping_event(self, event):
        self.logger.debug(event)
        time.sleep(1)
        return PongEvent()


if __name__ == '__main__':
    PongService().run()
