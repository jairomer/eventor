from pydantic import BaseModel
from typing import Optional, Tuple, List

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

class NewFlyerResponse(BaseModel):
    form: NewFlyerRequest
    flyers_uris: List[str]
