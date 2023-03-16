from typing import Optional
from pydantic import BaseModel


class RiseooSponsorValidationData(BaseModel):
    side: str
    sponsorUsername: str
    sponsorID: str


class RiseooSponsorValidationResponse(BaseModel):
    isSuccess: bool
    messageCode: int
    message: Optional[str]
    data: Optional[RiseooSponsorValidationData]
    additionalMessage: Optional[str]
