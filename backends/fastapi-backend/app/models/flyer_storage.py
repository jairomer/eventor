import threading 
from typing import Final
import io
import logging

class FlyerStorage:
    """
    This is a simple in-memory database to hold temporal images to be delivered to a client.
    """
    __flyers = dict()
    __lock = threading.Lock()
    MAX_IN_MEMORY: Final = 3000

    def store(self, flyer: io.BytesIO) -> str | None:
        with self.__lock:
            h = str(hash(flyer))
            self.__flyers[h] = flyer
            if len(self.__flyers) > FlyerStorage.MAX_IN_MEMORY:
                logging.error("Too many images in memory")
                return None
            return h

    def get(self, h) -> io.BytesIO | None:
        with self.__lock:
            flyer = self.__flyers.get(h) 
            if flyer:
                self.__flyers.pop(h)
            return flyer

