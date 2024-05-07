from typing import Optional, Tuple, List
import io

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .services.flyer_generator.flyer_maker import make_flyer_from_image
from .services.flyer_generator.stable_diffusion import get_images
from .services.flyer_generator.flyer import FlyerData

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
    generated_from: NewFlyerRequest
    flyers: List[bytes]

@app.post("/flyer")
async def generate_flyer(new_flyer_request: NewFlyerRequest):
    STABLE_DIFUSSION_INSTANCE = ""
    METRO_PATH = None
    # Get images
    images = get_images(
        url=STABLE_DIFUSSION_INSTANCE,
        prompt=new_flyer_request.prompt,
        img_size=new_flyer_request.size,
        batch_size=new_flyer_request.batch_size)

    if not images:
        print("Error generating the images.")
        raise HTTPException(status_code=503, detail="Service Unavailable")

    # Modify images
    flyers = []
    flyer_data = new_flyer_request.generate_flyer_data_from_details()
    for image in images:
        flyer = make_flyer_from_image(flyer_data, image, METRO_PATH)
        flyer_bytes = io.BytesIO()
        flyer.save(flyer_bytes, format="JPEG")
        flyers.append(flyer_bytes)

    return NewFlyerResponse(
            generated_from=new_flyer_request,
            flyers=flyers)
