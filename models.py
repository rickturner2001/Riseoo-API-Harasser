from typing import Optional
from typing import Optional
from pydantic import BaseModel, fields


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


class RiseoAccountRegistration(BaseModel):
    sponsorUsername: str
    side: int = 1
    username: str
    password: str
    fullName: str
    emailAddress: str
    contactNumber: str
    countryId: int = 219
    ipAddress: str
    title: str = 'Mr.'
    bankAccountHolderName: str = ""
    bankAccountNumber: str = ""
    bankAccountIFSC: str = ""
    bankAccountType: int = 0
