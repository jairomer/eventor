import io
import logging

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import StreamingResponse
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_503_SERVICE_UNAVAILABLE

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

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
async def get_api_key(api_key: str=Depends(api_key_header)):
    if not api_key:
        raise HTTPException (
                status_code=status.HTTP_403_FORBIDDEN,
                detail="API Key missing in request headers")
    if not get_settings().is_api_key(api_key):
        raise HTTPException (
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid API key")

    return api_key

@app.get("/flyer/{uri}")
async def get_flyer(uri: str, _: str = Depends(get_api_key)):
    storage = get_storage()
    flyer = storage.get(uri)
    if flyer:
        flyer.seek(0)
        return StreamingResponse(flyer, media_type="image/jpeg")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flyer URI not found")

@app.post("/flyer")
async def generate_flyer(new_flyer_request: NewFlyerRequest, _: str = Depends(get_api_key)):
    storage = get_storage()
    if new_flyer_request.batch_size > get_settings().MAX_BATCH_SIZE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Batch size exceeded")

    # Get images
    images = get_images(
        url=get_settings().STABLE_DIFFUSION_INSTANCE,
        prompt=new_flyer_request.prompt,
        img_size=new_flyer_request.size,
        batch_size=new_flyer_request.batch_size)

    if not images:
        logging.error("Error generating the images.")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service Unavailable")

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
            raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail="Service Overload")
        flyers.append("/flyer/{}".format(h))

    return NewFlyerResponse(
            form=new_flyer_request,
            flyers_uris=flyers)
