import concurrent.futures
from pathlib import Path
from functions import read_data_from_file, write_to_file
from Harasser import ApiHarasser, RequestType
import sys
import json
from pydantic import ValidationError
from models import RiseooSponsorValidationResponse
import logging
from config import FILES_DIR

logging.basicConfig(filename="assets/logger.log",
                             format='%(levelname)s:%(message)s', level=logging.INFO)


USERNAMES = read_data_from_file(str(FILES_DIR / "usernames.txt"))

requests_counter = 0

harasser = ApiHarasser(
    "https://api.riseoo.com/Registration/ValidateSponsor/", RequestType.GET)


def do_harass(username: str) -> None:
    global requests_counter
    requests_counter += 1
    try:
        response = harasser.do_request(username)
        parsed_data = (RiseooSponsorValidationResponse(**response.json()))
        if (parsed_data and parsed_data.isSuccess):
            print("Successful request with username: ",
                  parsed_data.data.sponsorUsername)
            write_to_file(FILES_DIR / "valid_sponsors.txt",
                          parsed_data.data.sponsorUsername)
            logging.info(f"new sponsor: {parsed_data.data.sponsorUsername}")

        else:
            print(
                f"{username} is not a sponsor... {requests_counter}/{len(USERNAMES)}")
    except json.JSONDecodeError:
        logging.error(
            f"Response is not json serializable: {response.status_code}\n-{response.text}")

    except ValidationError:
        logging.error(
            f"Response is not serializable (RiseooSponsorValidationResponse): {response.status_code}\n-{response.text}")


def main() -> None:
    workers = 50
    if len(sys.argv) > 1:
        if sys.argv[1].isnumeric():
            workers = int(sys.argv[1])

    print(f"== Initialized with {workers} workers ==\n")
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(do_harass, username)
                   for username in USERNAMES]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as exc:
                logging.error(f"Job failed: {exc}")


if __name__ == "__main__":
    main()
