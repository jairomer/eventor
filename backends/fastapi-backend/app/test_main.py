from fastapi.testclient import TestClient

from .main import app
from app.models.new_flyer import NewFlyerRequest, NewFlyerDetails, NewFlyerResponse

client = TestClient(app)

def test_generate_flyer():
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

    response = client.post("/flyer", content=request.model_dump_json())
   
    assert response.status_code == 200

    content = NewFlyerResponse.model_validate_json(response.content)

    assert content.form == request
    assert len(content.flyers_uris) == 5
    

    
