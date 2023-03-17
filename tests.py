import unittest
from models import RiseooSponsorValidationResponse, RiseoAccountRegistration
from pydantic import ValidationError
import json
from riseo_harasser import ApiHarasser


class TestRiseooModels(unittest.TestCase):

    # Models
    def test_riseoo_sponsor_validation_request_model_success(self):
        data = '{"isSuccess":true,"messageCode":0,"message":null,"data":{"side":1,"sponsorUsername":"priyanka2","sponsorID":94299},"additionalMessage":null}'
        riseo_data = RiseooSponsorValidationResponse(**json.loads(data))
        self.assertTrue(riseo_data.isSuccess)

    def test_riseoo_sponsor_validation_request_model_fail(self):
        data = '{"isSuccess":false,"messageCode":0,"message":"Referral user not found","data":null,"additionalMessage":null}'
        riseo_data = RiseooSponsorValidationResponse(**json.loads(data))
        self.assertFalse(riseo_data.isSuccess)

    def test_riseoo_sponsor_validation_request_model_error(self):
        with self.assertRaises(ValidationError):
            data = '{"isSuccess":false,"messageCode":"Hey","message":"Referral user not found","data":null,"additionalMessage":null}'
            RiseooSponsorValidationResponse(**json.loads(data))

    def test_riseoo_account_record_success(self):
        model = RiseoAccountRegistration(**{"sponsorUsername": "aaron", "side": 1, "username": "TempUser", "password": "Temp123$", "fullName": "Tempuser at User", "emailAddress": "tempuser@gmail.com",
                                         "contactNumber": "1-3129406294", "countryID": 219, "ipAddress": "95.138.2.197", "title": "Mr.", "panID": "", "bankAccountHolderName": "", "bankAccountNumber": "", "bankAccountIFSC": "", "bankAccountType": 0})
        self.assertTrue(model.username is not None)

    def test_riseoo_account_record_fail(self):
        with self.assertRaises(ValidationError):
            RiseoAccountRegistration(**json.loads("""{"sponsorUsername": "aaron", "side": 1, "username": null, "password":"Temp123$", "fullName": "Tempuser at User", "emailAddress": "tempuser@gmail.com",
                                                 "contactNumber": "1-3129406294", "countryID": null, "ipAddress": "95.138.2.197", "title": "Mr.", "panID": "", "bankAccountHolderName": "", "bankAccountNumber": "", "bankAccountIFSC": "", "bankAccountType": 0}"""))

    # API

    def test_riseoo_validation_request_success(self):
        harasser = ApiHarasser(
            "https://api.riseoo.com/Registration/ValidateSponsor/")
        data = harasser.do_request("test")
        self.assertTrue(isinstance(data, RiseooSponsorValidationResponse))

    def test_riseoo_validation_request_fail(self):
        harasser = ApiHarasser(
            "https://api.riseoo.com/Registration/randomEndpoint/")
        data = harasser.do_request(endpoint_extension="Hey123")
        self.assertTrue(data is None)


if __name__ == "__main__":
    unittest.main()
