"""API"""

from __future__ import annotations


import requests


def get_uuid(name: str) -> str | None:
    try:
        api_data = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{name}',
                            headers={'User-Agent': 'Mozilla/5.0'}).json()
        if api_data['id']:
            return api_data['id']
        if api_data['errorMessage']:
            return None
    except (requests.exceptions.ConnectionError, requests.exceptions.RequestException, KeyError):
        print('Something happened with the connection. Maybe their server is down?')
        return None


def get_api_data(key: str, uuid: str) -> dict | None:
    try:
        api_data = requests.get(f'https://api.hypixel.net/player?key={key}&uuid={uuid}',
                            headers={'User-Agent': 'Mozilla/5.0'}).json()
        if not api_data['success']:
            print(api_data['cause'])
            return None
        return api_data
    except (requests.exceptions.ConnectionError, requests.exceptions.RequestException, KeyError):
        print('Something happened with the connection. Maybe their server is down?')
        return None
