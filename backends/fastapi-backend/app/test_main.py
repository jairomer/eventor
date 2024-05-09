from fastapi.testclient import TestClient
from fastapi import status
from PIL import Image
import io

from app.core.settings.app_settings import get_settings

from .main import app
from app.models.new_flyer import NewFlyerRequest, NewFlyerDetails, NewFlyerResponse

headers = {
    "X-API-Key": get_settings().API_MASTER_KEY.get_secret_value()
}

client = TestClient(app)

def test_generate_flyer():
    """
    Happy path for the generation of a flyer batch from a request and their successive recovery.
    """
    if not get_settings().TEST_END_TO_END: 
        return 
    details = NewFlyerDetails(
        title="Silent Meditation Course",
        subtitle="no speech",
        date="2024-05-07",
        timeframe="From 19:00 to 21:30",
        place="Sala Dana",
        metro="Tirso de Molina",
    )
    request = NewFlyerRequest(
            prompt="People meditating in silence",
            size=(512, 512),
            details=details,
            batch_size=5)

    response = client.post("/flyer", content=request.model_dump_json(), headers=headers)
   
    assert response.status_code == status.HTTP_200_OK

    content = NewFlyerResponse.model_validate_json(response.content)

    assert content.form == request
    assert len(content.flyers_uris) == 5
    
    # Now get the images.
    for uri in content.flyers_uris:
        uri_response = client.get(uri, headers=headers)
        assert uri_response.status_code == status.HTTP_200_OK
        #img = Image.open(io.BytesIO(uri_response.content))
        #img.save("./tests/{}.jpeg".format(uri))

def test_api_auth():
    """
    This should fail because we are not including the API key in the request headers.
    """
    response = client.post("/flyer")
    assert response.status_code == status.HTTP_403_FORBIDDEN
