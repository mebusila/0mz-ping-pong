import time


class Event:

    def __init__(self):
        self.time = time.time()
        self.name = self.__class__.__name__

    def __str__(self):
        return str(self.__dict__)


class SubscribeEvent(Event):

    def __init__(self, service, topics):
        self.service = service
        self.topics = topics
        super(SubscribeEvent, self).__init__()


class StopEvent(Event):

    def __init__(self):
        super(StopEvent, self).__init__()


class PingEvent(Event):

    def __init__(self):
        super(PingEvent, self).__init__()


class PongEvent(Event):

    def __init__(self):
        super(PongEvent, self).__init__()
