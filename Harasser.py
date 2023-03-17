import requests
from enum import Enum, auto
from typing import Optional
from models import RiseooSponsorValidationResponse
import json
from pydantic import ValidationError
import logging

logging.basicConfig(filename="assets/logger.log",
                             format='%(levelname)s:%(message)s', level=logging.INFO)


class RequestType(Enum):
    POST = auto()
    GET = auto()


class ApiHarasser:
    def __init__(self, endpoint: str, request_type: RequestType = RequestType.GET, headers: Optional[dict] = None, ):
        self.endpoint = endpoint
        self.request_type = request_type
        self.headers = headers

    def do_request(self, endpoint_extension: Optional[str] = None, data: Optional[dict] = None, is_json: bool = False) -> Optional[requests.Response]:
        API_ENDPOINT = self.endpoint + \
            ("" if endpoint_extension is None else endpoint_extension)
        try:
            if self.request_type == RequestType.GET:
                response = requests.get(
                    API_ENDPOINT, headers=self.headers, allow_redirects=False)
            else:

                if is_json:
                    response = requests.post(
                        API_ENDPOINT, headers=self.headers, json=json.loads(data), allow_redirects=False, )

                else:
                    response = requests.post(
                        API_ENDPOINT, headers=self.headers, data=data, allow_redirects=False, )

            if not (response and response.ok):
                logging.error(
                    f"Unsuccessful request. Status code: {response.status_code}")
                return

        except requests.ConnectTimeout:
            logging.error(
                "Server did not respond within the timeout period specified in the request.")
            return
        except requests.ConnectionError:
            logging.error(
                "Connection to the server is refused or if there is a DNS resolution failure.")
            return

        return response
