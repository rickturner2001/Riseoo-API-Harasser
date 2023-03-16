import requests
from enum import Enum, auto
from typing import Optional
from models import RiseooSponsorValidationResponse
import json
from pydantic import ValidationError
from logger import LOGGER


class RequestType(Enum):
    POST = auto()
    GET = auto()


class ApiHarasser:
    def __init__(self, endpoint: str, request_type: RequestType = RequestType.GET, data: Optional[dict] = None, headers: Optional[dict] = None):
        self.endpoint = endpoint
        self.request_type = request_type
        self.headers = headers
        self.data = data

    def do_request(self, endpoint_extension: Optional[str] = None) -> Optional[RiseooSponsorValidationResponse]:
        API_ENDPOINT = self.endpoint + \
            ("" if endpoint_extension is None else endpoint_extension)
        try:
            if self.request_type == RequestType.GET:
                response = requests.get(
                    API_ENDPOINT, headers=self.headers, allow_redirects=False)
            else:
                response = requests.post(
                    API_ENDPOINT, headers=self.headers, data=self.data, allow_redirects=False)

            if not (response and response.ok):
                LOGGER.error(
                    f"Unsuccessful request. Status code: {response.status_code}")
                return

        except requests.ConnectTimeout:
            LOGGER.error(
                "Server did not respond within the timeout period specified in the request.")
            return
        except requests.ConnectionError:
            LOGGER.error(
                "Connection to the server is refused or if there is a DNS resolution failure.")
            return

        try:
            response_json = response.json()
            return RiseooSponsorValidationResponse(**response_json)
        except json.JSONDecodeError:
            LOGGER.error(
                f"Response is not json serializable: {response.status_code}\n-{response.text}")

        except ValidationError:
            LOGGER.error(
                f"Response is not serializable (RiseooSponsorValidationResponse): {response.status_code}\n-{response.text}")
