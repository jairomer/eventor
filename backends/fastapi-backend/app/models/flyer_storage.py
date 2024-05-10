import threading 
import io
import logging
from typing import Final
from functools import lru_cache

from app.core.settings.app_settings import AppSettings, get_settings

class FlyerStorage:
    """
    This is a simple in-memory key/value cache to hold images until they are delivered to a client.

    Attention:
        This works if you have a single instance of the service, but if several replicas are created,
        it is important that the request is directed to the right replica, which can complicate operations,
        so this is not the best solution for horizontally scalable deployments.

        However, this is not yet a problem we need to solve. If it becomes one, then the next step
        would be to use something like Redis or Memcached instead of a dictionary.
    """
    __flyers = dict()
    __lock = threading.Lock()
    MAX_IN_MEMORY: Final
    
    def __init__(self, settings: AppSettings):
        self.MAX_IN_MEMORY = settings.MAX_IN_MEMORY

    def store(self, flyer: io.BytesIO) -> str | None:
        with self.__lock:
            h = str(hash(flyer))
            self.__flyers[h] = flyer
            if len(self.__flyers) > self.MAX_IN_MEMORY:
                logging.error("Too many images in memory")
                return None
            return h

    def get(self, h) -> io.BytesIO | None:
        with self.__lock:
            flyer = self.__flyers.get(h) 
            if flyer:
                self.__flyers.pop(h)
            return flyer

    def __len__(self):
        return len(self.__flyers)

@lru_cache
def get_storage() -> FlyerStorage: 
    return FlyerStorage(get_settings())

