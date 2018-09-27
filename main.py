import logging
import time

from events import SubscribeEvent, PingEvent, PongEvent, StopEvent
from proxy import Proxy

logging.basicConfig(format='%(levelname) -7s %(asctime)s %(name) -20s'
                           ' %(funcName) -10s %(lineno) -5d: %(message)s',
                    level=logging.DEBUG)

if __name__ == '__main__':
    ping = Proxy('PingService')
    pong = Proxy('PongService')

    ping.ask(SubscribeEvent('PongService', [PingEvent]))
    pong.ask(SubscribeEvent('PingService', [PongEvent]))

    pong.tell(PingEvent())

    time.sleep(15)

    ping.ask(StopEvent())
    pong.ask(StopEvent())
