import json
import pytest
import requests

baseUrl = "https://api.frs1.ott.kaltura.com"
headers = {"Content-Type": "application/json"}


class KalturaUser:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def from_request(cls, request_object):
        request_dict = json.loads(request_object)
        username = request_dict['user']['username']
        password = request_dict['password']
        return cls(username, password)


@pytest.fixture(scope='function')
def register(request):
    payload = request.param
    path = "/api_v3/service/ottuser/action/register"
    response = requests.post(url=baseUrl + path, data=json.dumps(payload), headers=headers)
    return response


@pytest.fixture
def create_user(register):
    user = KalturaUser.from_request(register.request.body)
    return user





