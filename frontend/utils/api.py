import requests

BASE_URL = "http://127.0.0.1:8000"


def get(endpoint, token=None):
    headers = {}

    if token:
        headers["Authorization"] = f"Bearer {token}"

    return requests.get(BASE_URL + endpoint, headers=headers)


def post(endpoint, data=None, token=None):
    headers = {}

    if token:
        headers["Authorization"] = f"Bearer {token}"

    return requests.post(BASE_URL + endpoint, json=data, headers=headers)


def put(endpoint, data=None, token=None):
    headers = {}

    if token:
        headers["Authorization"] = f"Bearer {token}"

    return requests.put(BASE_URL + endpoint, json=data, headers=headers)


def delete(endpoint, token=None):
    headers = {}

    if token:
        headers["Authorization"] = f"Bearer {token}"

    return requests.delete(BASE_URL + endpoint, headers=headers)