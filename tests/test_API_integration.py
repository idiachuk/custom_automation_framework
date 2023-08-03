import time
import requests
import json
from time import gmtime, strftime
import pytest
import concurrent.futures

today = strftime("%Y-%m-%d", gmtime())
baseUrl = "https://reqres.in"
path = "/api/users/"
params = {
        "page": 1,
        "per_page": 12
    }


def test_get_users_list():
    # - Get a list of users:
    response = requests.get(url=baseUrl + path, params=params)
    # Validate that the response code is `200`
    assert response.status_code == 200

    odd_users_list = []
    for user in response.json()['data']:
        if int(user['id']) % 2 != 0:
            odd_users_list.append(user['email'])
    # Print all users with odd ID numbers
    print(f'TEST1: list of odd users: {odd_users_list}')


def test_create_new_user():
    payload = {
        "name": "Igor",
        "job": "QA Automation Engineer"
    }
    # Create a new user
    response = requests.post(url=baseUrl + path, data=json.dumps(payload))
    # Validate that the response code is `201`
    assert response.status_code == 201
    # Validate that the creation date is today
    user_creation_day = response.json()['createdAt'].split('T')[0]
    assert user_creation_day == today


def test_user_update():
    payload = {
        "name": "Igor",
        "job": "QA Automation Engineer",
        "updatedAt": "2023-08-01T16:56:48.203Z"
    }
    user_id = "2"
    headers = {"Content-Type": "application/json"}
    # Update a user
    response = requests.patch(url=baseUrl + path + user_id, data=json.dumps(payload), headers=headers)
    # Validate that the response code is `200`
    assert response.status_code == 200

    # Validate that the response body matches the request body where applicable. Do a recursive comparison if possible.
    def dicts_comparison(dict1, dict2):
        different_keys = []
        for key in dict1:
            if dict1[key] != dict2[key]:
                different_keys.append(key)
        if len(different_keys) == 0:
            return "TEST3: Dicts are equal"
        else:
            return f"TEST3: Keys that differ: {different_keys}"

    print(dicts_comparison(payload, response.json()))


# Write a parameterized validation with the values `0` and `3`
@pytest.mark.parametrize("delay_sec, expected_response_time", [(0, 1), (3, 1)])
def test_response_time(delay_sec, expected_response_time):
    start_time = time.time()
    # Get a list of users passing a delay query parameter with the provided value for the validation
    time.sleep(delay_sec)
    # - Get a list of users:
    response = requests.get(url=baseUrl + path, params=params)
    execution_time = time.time() - start_time
    # Validate that the response time is no longer than `1` second
    assert execution_time < expected_response_time


def test_asynch_requests():
    user_ids_range = range(1, 11)

    def get_user(user_id):
        response = requests.get(url=baseUrl + path + str(user_id))
        # - Validate, asynchronously as well, that all response codes are `200s`
        # NOTE: to make sure that requests are asynch, pls uncomment the next string:
        # print(response.json())
        assert response.status_code == 200

    # - Use whatever asynchronous technique you prefer to get `10` single users
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(get_user, user_ids_range)
    for i in results:
        pass

