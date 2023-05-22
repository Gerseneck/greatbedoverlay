import requests


def get_uuid(name: str):
    try:
        data = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{name}', headers={'User-Agent': 'Mozilla/5.0'})
        if data.json()['id']:
            return data.json()['id']
        if data.json()['errorMessage']:
            return None
    except (requests.exceptions.ConnectionError, requests.exceptions.RequestException, KeyError):
        return None


def get_stats(key: str, uuid: str):
    try:
        return requests.get(f'https://api.hypixel.net/player?key={key}&uuid={uuid}', headers={'User-Agent': 'Mozilla/5.0'}).json()
    except (requests.exceptions.ConnectionError, requests.exceptions.RequestException, KeyError):
        return None


def _get_finals(data: dict) -> tuple[int, int]:
    core_finals = ['eight_one_final_kills_bedwars', 'eight_two_final_kills_bedwars', 'four_three_final_kills_bedwars', 'four_four_final_kills_bedwars']
    core_deaths = ['eight_one_final_deaths_bedwars', 'eight_two_final_deaths_bedwars', 'four_three_final_deaths_bedwars',
                    'four_four_final_deaths_bedwars']
    finals = 0
    deaths = 0
    for i in [data['player']['stats']['Bedwars'][i] for i in data['player']['stats']['Bedwars'] if i in core_finals]:
        finals += i
    for i in [data['player']['stats']['Bedwars'][i] for i in data['player']['stats']['Bedwars'] if i in core_deaths]:
        deaths += i
    return finals, deaths


def _get_beds(data: dict) -> tuple[int, int]:
    return data['player']['stats']['Bedwars']['beds_broken_bedwars'], data['player']['stats']['Bedwars']['beds_lost_bedwars']


def _get_win_loose(data: dict) -> tuple[int, int]:
    return data['player']['stats']['Bedwars']['wins_bedwars'], data['player']['stats']['Bedwars']['losses_bedwars']


def _get_level(data: dict):
    exp = data['player']['networkExp']
    return exp


def _get_rank(data: dict):
    if data['player']['rank']:
        return data['player']['rank']
    if data['player']['monthlyPackageRank']:
        return data['player']['monthlyPackageRank']
    if data['player']['newPackageRank']:
        return data['player']['newPackageRank']
    if data['player']['packageRank']:
        return data['player']['packageRank']


def get_info(data: dict):
    if not data:
        return 'Unable to obtain bedwars data'
    bw_level = data['player']['achievements']['bedwars_level']
    level = _get_level(data)
    rank = _get_rank(data)
    finals, deaths = _get_finals(data)
    beds_broken, beds_lost = _get_beds(data)
    wins, losses = _get_win_loose(data)
    return {'rank': rank, 'level': level, 'bedwars_level': bw_level, 'finals': finals, 'FKDR': round(finals/deaths, 2), 'beds_broken': beds_broken, 'wins': wins, 'WLR': round(wins/losses, 2), 'winstreak': data['player']['stats']['Bedwars']['winstreak']}


def print_data(data: dict):
    no_data_players = {}
    for player in data:
        if player == 'Nicked. Unable to obtain bedwars data.' or player == 'Unable to obtain bedwars data':
            no_data_players[player] = data[player]
            del data[player]
            continue
    data = dict(sorted(data.items(), key=lambda item: item[1]['bedwars_level'], reverse=True))
    for player in data:
        level = data[player]['level']
        rank = data[player]['rank']
        print(f'[{rank}] {player}: {data[player]}')
    for player in no_data_players:
        print(f'{player}: {no_data_players[player]}')
