from fastapi.testclient import TestClient

from .main import app, NewFlyerRequest, NewFlyerDetails

client = TestClient(app)

#def test_read_main():
#    response = client.get("/")
#    assert response.status_code == 200
#    assert response.json() == {"msg": "Hello World"}

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
   
    # Stable diffusion is not set, so the service is unavailable.
    assert response.status_code == 503
    
