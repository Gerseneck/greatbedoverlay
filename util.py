import requests

import constants


def get_uuid(name: str):
    try:
        data = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{name}', headers={'User-Agent': 'Mozilla/5.0'}).json()
        if data['id']:
            return data['id']
        if data['errorMessage']:
            return None
    except (requests.exceptions.ConnectionError, requests.exceptions.RequestException, KeyError):
        return None


def get_stats(key: str, uuid: str):
    try:
        data = requests.get(f'https://api.hypixel.net/player?key={key}&uuid={uuid}', headers={'User-Agent': 'Mozilla/5.0'}).json()
        if not data['success']:
            return None
        return data
    except (requests.exceptions.ConnectionError, requests.exceptions.RequestException, KeyError):
        return None


def _get_winstreak(data: dict):
    winstreak = 0
    if 'winstreak' in data['player']['stats']['Bedwars']:
        winstreak = data['player']['stats']['Bedwars']['winstreak']
    return winstreak


def _get_finals(data: dict):
    core_finals = ['eight_one_final_kills_bedwars', 'eight_two_final_kills_bedwars', 'four_three_final_kills_bedwars', 'four_four_final_kills_bedwars']
    core_deaths = ['eight_one_final_deaths_bedwars', 'eight_two_final_deaths_bedwars', 'four_three_final_deaths_bedwars', 'four_four_final_deaths_bedwars']

    finals = 0
    deaths = 0
    for i in [data['player']['stats']['Bedwars'][i] for i in core_finals if i in data['player']['stats']['Bedwars']]:
        finals += i
    for i in [data['player']['stats']['Bedwars'][i] for i in core_deaths if i in data['player']['stats']['Bedwars']]:
        deaths += i
    return finals, deaths


def _get_beds(data: dict):
    beds = 0
    lost = 0
    if 'beds_broken_bedwars' in data['player']['stats']['Bedwars']:
        beds = data['player']['stats']['Bedwars']['beds_broken_bedwars']
    if 'beds_lost_bedwars' in data['player']['stats']['Bedwars']:
        lost = data['player']['stats']['Bedwars']['beds_lost_bedwars']
    return beds, lost


def _get_win_loose(data: dict):
    wins = 0
    losses = 0
    if 'wins_bedwars' in data['player']['stats']['Bedwars']:
        wins = data['player']['stats']['Bedwars']['wins_bedwars']
    if 'losses_bedwars' in data['player']['stats']['Bedwars']:
        losses = data['player']['stats']['Bedwars']['losses_bedwars']
    return wins, losses


def _get_level(data: dict):
    # exp = data['player']['networkExp']
    exp = 0
    return exp


def _get_rank(data: dict):
    rank = ''
    if 'rank' in data['player']:
        rank = data['player']['rank']
    elif 'monthlyPackageRank' in data['player'] and data['player']['monthlyPackageRank'] != 'NONE':
        rank = data['player']['monthlyPackageRank']
    elif 'newPackageRank' in data['player']:
        rank = data['player']['newPackageRank']
    elif 'packageRank' in data['player']:
        rank = data['player']['packageRank']
    if not rank:
        return 'NONE'
    return constants.RANK[rank]


def get_info(data: dict):
    if not data:
        return 'Unable to obtain Bedwars data'

    bw_level = data['player']['achievements']['bedwars_level']
    level = _get_level(data)
    rank = _get_rank(data)
    finals, deaths = _get_finals(data)
    beds_broken, beds_lost = _get_beds(data)
    wins, losses = _get_win_loose(data)
    winstreak = _get_winstreak(data)
    return {'rank': rank, 'level': level, 'bedwars_level': bw_level, 'finals': finals, 'FKDR': round(finals/deaths, 2), 'beds_broken': beds_broken, 'wins': wins, 'WLR': round(wins/losses, 2), 'winstreak': winstreak}


def print_data(data: dict):
    spaces = len(max(data, key=len)) + 16
    no_data_players = {}
    for player in list(data):
        if data[player] == 'Nicked. Unable to obtain Bedwars data.' or data[player] == 'Unable to obtain Bedwars data':
            no_data_players[player] = data[player]
            data.pop(player)
            continue
    data = dict(sorted(data.items(), key=lambda item: item[1]['bedwars_level'], reverse=True))
    title = f'NAME{" " * (spaces - 4)} | LEVEL | BEDWARS LEVEL | FINAL KILLS |  FKDR  | BEDS BROKEN |  WINS  |  WLR  | WINSTREAK | SCORE |'
    print(title)
    print('=' * len(title))
    for player in data:
        rank = data[player]['rank']
        level = data[player]['level']
        level_bedwars = data[player]['bedwars_level']
        finals = data[player]['finals']
        fkdr = data[player]['FKDR']
        beds = data[player]['beds_broken']
        wins = data[player]['wins']
        wlr = data[player]['WLR']
        winstreak = data[player]['winstreak']

        spaces_name = spaces - len(rank) - 3
        print(f'[{rank}] {player:<{spaces_name}s} | {level:^5} | {level_bedwars:^13} | {finals:^11} | {fkdr:^6} | '
              f'{beds:^11} | {wins:^6} | {wlr:^5} | {winstreak:^9} |  | ')
    for player in no_data_players:
        print(f'{player:<{spaces}s} | {no_data_players[player]:^95} |')
    print('=' * len(title))
