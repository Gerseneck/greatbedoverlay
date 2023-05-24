"""API"""

from __future__ import annotations


import requests


def get_uuid(name: str) -> str | None:
    try:
        data = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{name}',
                            headers={'User-Agent': 'Mozilla/5.0'}).json()
        if data['id']:
            return data['id']
        if data['errorMessage']:
            return None
    except (requests.exceptions.ConnectionError, requests.exceptions.RequestException, KeyError):
        print('Something happened with the connection. Maybe their server is down?')
        return None


def get_stats(key: str, uuid: str) -> dict | None:
    try:
        data = requests.get(f'https://api.hypixel.net/player?key={key}&uuid={uuid}',
                            headers={'User-Agent': 'Mozilla/5.0'}).json()
        if not data['success']:
            return None
        return data
    except (requests.exceptions.ConnectionError, requests.exceptions.RequestException, KeyError):
        print('Something happened with the connection. Maybe their server is down?')
        return None
