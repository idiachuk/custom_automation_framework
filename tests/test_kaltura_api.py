import allure
from time import strftime, localtime
from conftest import *


payload_positive = {
    "apiVersion": "6.0.0",
    "partnerId": 3197,
    "user": {
        "objectType": "KalturaOTTUser",
        "username": f"QATest_{randname(8)}",
        "firstName": f"ott_user_{randname(8)}",
        "lastName": f"{randnumber(12)}",
        "email": f"QATest_{randnumber(12)}@mailinator.com",
        "address": "ott_user_lWkiwzTJJGYI fake address",
        "city": "ott_user_lWkiwzTJJGYI fake city",
        "countryId": 5,
        "externalId": f"{randnumber(12)}"
    },
    "password": "password_SlLVWDLl"
}

payload_negative = {
    "apiVersion": "6.0.0",
    "partnerId": 3197,
    "user": {
        "objectType": "KalturaOTTUser",
        "username": "QATest_qZNxDEXC",
        "firstName": "ott_user_pMbaSNXc",
        "lastName": "424740711529",
        "email": "QATest_266494261893@mailinator.com",
        "address": "ott_user_lWkiwzTJJGYI fake address",
        "city": "ott_user_lWkiwzTJJGYI fake city",
        "countryId": 5,
        "externalId": "097625450181"
    },
    "password": "password_SlLVWDLl"
}


def print_headers_and_bodies(response):
    print(f"\nREQUEST BODY: \n{response.request.body}")
    allure.attach(response.request.body, name="REQUEST BODY", attachment_type=allure.attachment_type.JSON)
    print(f"\nREQUEST HEADERS: \n{response.request.headers}")
    allure.attach(str(response.request.headers), name="REQUEST HEADERS", attachment_type=allure.attachment_type.JSON)
    print(f"\nRESPONSE BODY: \n{response.json()}")
    allure.attach(str(response.json()), name="RESPONSE BODY", attachment_type=allure.attachment_type.JSON)
    print(f"\nRESPONSE HEADERS: \n{response.headers}")
    allure.attach(str(response.headers), name="RESPONSE HEADERS", attachment_type=allure.attachment_type.JSON)


@allure.title("Register a new user")
@pytest.mark.parametrize('register', [payload_positive, payload_negative], indirect=True)
def test_post_register(register):
    # - Register a new user:
    print("\nREGISTRATION TEST")
    response = register

    # Validate that the response code is `200`
    assert response.status_code == 200

    # Print bodies and headers and attach them to allure report:
    print_headers_and_bodies(response)

    # Assertion of existence of any response header - checking if X-Kaltura-Session is TRUE:
    assert response.headers['X-Kaltura-Session']

    if 'X-Kaltura-Error-Msg' in response.headers:
        error_code = response.json()['result']['error']['code']
        error_message = response.json()['result']['error']['message']
        error_text = f"ERROR CODE: {error_code} and ERROR MESSAGE: {error_message}"
        allure.attach(str(error_text), name="ERROR TEXT", attachment_type=allure.attachment_type.JSON)
        pytest.fail(error_text)
    else:
        # Assert if ID exists:
        assert response.json()["result"]["id"]
        # Assert if ID is string:
        assert isinstance(response.json()["result"]["id"], str)
        # Assert if countryId exists:
        assert response.json()["result"]["countryId"]
        # Assert if countryId is int:
        assert isinstance(response.json()["result"]["countryId"], int)


@allure.title("Login with a new user")
@pytest.mark.parametrize('register', [payload_positive], indirect=True)
def test_post_login(register, create_user):
    user = create_user
    # - Login with a new user:
    path = "/api_v3/service/ottuser/action/login"
    payload = {
        "apiVersion": "6.0.0",
        "partnerId": 3197,
        "username": f"{user.username}",
        "password": f"{user.password}",
        "extraParams": {}
    }
    response = requests.post(url=baseUrl + path, data=json.dumps(payload), headers=headers)
    print("\nLOGIN TEST")

    # Print bodies and headers and attach them to allure report:
    print_headers_and_bodies(response)

    # Assertion if “lastLoginDate” exist
    assert response.json()['result']['user']['lastLoginDate']

    # Present it (lastLoginDate) as valid Date value (any format)
    last_login_date = response.json()['result']['user']['lastLoginDate']
    date_string = strftime('%Y-%m-%d %H:%M:%S', localtime(last_login_date))
    print(f'lastLoginDate:  {date_string}')
    allure.attach(str(date_string), name="lastLoginDate", attachment_type=allure.attachment_type.JSON)
