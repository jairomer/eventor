from typing import Optional, Tuple, List, Final
import io
import logging
import threading 

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from starlette.types import HTTPExceptionHandler

from .services.flyer_generator.flyer_maker import make_flyer_from_image
from .services.flyer_generator.stable_diffusion import get_images
from .services.flyer_generator.flyer import Flyer, FlyerData

app = FastAPI()

class NewFlyerDetails(BaseModel):
    title: str
    subtitle: str
    date: str
    timeframe: str
    place: str
    metro: Optional[str] = None

class NewFlyerRequest(BaseModel):
    prompt: str
    size: Tuple[int, int]
    batch_size: int
    details: NewFlyerDetails

    def generate_flyer_data_from_details(self) -> FlyerData:
        return FlyerData(
            title = self.details.title,
            subtitle = self.details.subtitle,
            date = self.details.date,
            timeframe = self.details.timeframe,
            place = self.details.place,
            metro = self.details.metro)

class NewFlyerResponse(BaseModel):
    form: NewFlyerRequest
    flyers_uris: List[str]


class FlyerStorage:
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

storage = FlyerStorage()

@app.get("/flyer/{uri}")
async def get_flyer(uri: str):
    global storage
    flyer = storage.get(uri)
    if flyer:
        flyer.seek(0)
        return StreamingResponse(flyer, media_type="image/jpeg")
    raise HTTPException(status_code=404, detail="Flyer URI not found")

@app.post("/flyer")
async def generate_flyer(new_flyer_request: NewFlyerRequest):
    STABLE_DIFUSSION_INSTANCE = ""
    METRO_PATH = None
    global storage
    # Get images
    images = get_images(
        url=STABLE_DIFUSSION_INSTANCE,
        prompt=new_flyer_request.prompt,
        img_size=new_flyer_request.size,
        batch_size=new_flyer_request.batch_size)

    if not images:
        logging.error("Error generating the images.")
        raise HTTPException(status_code=503, detail="Service Unavailable")

    # Modify images
    flyers = []
    flyer_data = new_flyer_request.generate_flyer_data_from_details()
    for image in images:
        flyer = make_flyer_from_image(flyer_data, image, METRO_PATH)
        flyer = flyer.convert("RGB")
        flyer_bytes = io.BytesIO()
        flyer.save(flyer_bytes, "JPEG", quality=95)
        h = storage.store(flyer_bytes)
        if not h:
            raise HTTPException(status_code=503, detail="Service Overload")
        flyers.append("/flyer/{}".format(h))

    return NewFlyerResponse(
            form=new_flyer_request,
            flyers_uris=flyers)
