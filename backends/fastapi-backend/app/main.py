import io
import logging

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse

from app.services.flyer_generator.flyer import FlyerData
from app.services.flyer_generator.flyer_maker import make_flyer_from_image
from app.services.flyer_generator.stable_diffusion import get_images
from app.models.new_flyer import NewFlyerRequest, NewFlyerResponse
from app.models.flyer_storage import get_storage
from app.core.settings.app_settings import get_settings

app = FastAPI()

def generate_flyer_data_from_details(request: NewFlyerRequest) -> FlyerData:
    return FlyerData(
        title = request.details.title,
        subtitle = request.details.subtitle,
        date = request.details.date,
        timeframe = request.details.timeframe,
        place = request.details.place,
        metro = request.details.metro)

@app.get("/flyer/{uri}")
async def get_flyer(uri: str):
    storage = get_storage()
    flyer = storage.get(uri)
    if flyer:
        flyer.seek(0)
        return StreamingResponse(flyer, media_type="image/jpeg")
    raise HTTPException(status_code=404, detail="Flyer URI not found")

@app.post("/flyer")
async def generate_flyer(new_flyer_request: NewFlyerRequest):
    storage = get_storage()
    # Get images
    images = get_images(
        url=get_settings().STABLE_DIFUSSION_INSTANCE,
        prompt=new_flyer_request.prompt,
        img_size=new_flyer_request.size,
        batch_size=new_flyer_request.batch_size)

    if not images:
        logging.error("Error generating the images.")
        raise HTTPException(status_code=503, detail="Service Unavailable")

    # Modify images
    flyers = []
    flyer_data = generate_flyer_data_from_details(new_flyer_request)
    for image in images:
        flyer = make_flyer_from_image(flyer_data, image, get_settings().METRO_PATH)
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
