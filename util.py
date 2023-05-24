from dataclasses import dataclass
import math

import constants
from constants import C, CLEAR


CORE_MODES_FKILLS = ['eight_one_final_kills_bedwars', 'eight_two_final_kills_bedwars',
                     'four_three_final_kills_bedwars', 'four_four_final_kills_bedwars']
CORE_MODES_FDEATHS = ['eight_one_final_deaths_bedwars', 'eight_two_final_deaths_bedwars',
                      'four_three_final_deaths_bedwars', 'four_four_final_deaths_bedwars']


@dataclass
class Player:
    bedwars_level: int
    network_level: float
    network_rank: str
    final_kills: int
    final_deaths: int
    bed_breaks: int
    bed_losses: int
    games_won: int
    games_lost: int
    current_winstreak: int

    raw_fkdr: float
    raw_wlr: float
    adjusted_fkdr: float
    adjusted_wlr: float
    skill_score: float


def get_network_level(data: dict):
    network_level = 0
    if ['networkExp'] in data['player']:
        network_level = round(math.sqrt(data['player']['networkExp']*0.0008 + 12.25) - 2.5, 2)
    return network_level


def get_rank(data: dict):
    rank = 'NORMAL'
    if 'rank' in data['player']:
        rank = data['player']['rank']
    elif 'monthlyPackageRank' in data['player'] and data['player']['monthlyPackageRank'] != 'NONE':
        rank = data['player']['monthlyPackageRank']
    elif 'newPackageRank' in data['player']:
        rank = data['player']['newPackageRank']
    elif 'packageRank' in data['player']:
        rank = data['player']['packageRank']
    return constants.RANK[rank]


def wilson(positive: int, negative: int) -> float:
    n = positive + negative
    if n == 0:
        return 0.0
    p_hat = positive / n
    Z = 2.326  # z_alpha/2, alpha=0.01, 99% right-tailed confidence interval
    radicand = (p_hat*(1-p_hat) + Z*Z/(4*n)) / n
    top = p_hat + (Z*Z)/(2*n) - Z*math.sqrt(radicand)
    bottom = 1 + Z*Z/n
    p = top / bottom
    return p


def wilson_ratio(positive: int, negative: int) -> float:
    p = wilson(positive, negative)
    # Returns something similar to an FKDR/WLR instead of a probability 0..1
    return p / (1-p)


def longest_name(data: dict) -> str:
    name = []
    for i in data:
        name.append(f'{constants.RAW_RANK[data[i].network_rank]}{i}')
    long = max(name, key=len)
    return long


def get_info(data: dict) -> Player:
    network_level = get_network_level(data)
    network_rank = get_rank(data)

    if 'Bedwars' not in data['player']['stats']:
        return Player(bedwars_level=1, network_level=network_level, network_rank=network_rank,
                      final_kills=0, final_deaths=0, bed_breaks=0, bed_losses=0,
                      games_won=0, games_lost=0, current_winstreak=0, raw_fkdr=0,
                      raw_wlr=0, adjusted_fkdr=0, adjusted_wlr=0, skill_score=0)

    bedwars_level = data['player']['achievements']['bedwars_level']
    final_kills = sum([data['player']['stats']['Bedwars'].get(key, 0) for key in CORE_MODES_FKILLS])
    final_deaths = sum([data['player']['stats']['Bedwars'].get(key, 0) for key in CORE_MODES_FDEATHS])
    bed_breaks = data['player']['stats']['Bedwars'].get('beds_broken_bedwars', 0)
    bed_losses = data['player']['stats']['Bedwars'].get('beds_lost_bedwars', 0)
    games_won = data['player']['stats']['Bedwars'].get('wins_bedwars', 0)
    games_lost = data['player']['stats']['Bedwars'].get('losses_bedwars', 0)
    current_winstreak = data['player']['stats']['Bedwars'].get('winstreak', 0)

    # Calculations
    raw_fkdr = final_kills / max(final_deaths, 1)
    raw_wlr = games_won / max(games_lost, 1)
    adjusted_fkdr = wilson_ratio(final_kills, final_deaths)
    adjusted_wlr = wilson_ratio(games_won, games_lost)
    # Basically a modified wilson FKDR scaled by 10, with extra points for high numbers of finals/beds
    index = final_kills + 2.5*bed_breaks
    skill_score = 5 * wilson_ratio(math.floor(index), final_deaths) + (index/80)**0.75 - 15

    return Player(bedwars_level=bedwars_level, network_level=network_level, network_rank=network_rank,
                  final_kills=final_kills, final_deaths=final_deaths, bed_breaks=bed_breaks, bed_losses=bed_losses,
                  games_won=games_won, games_lost=games_lost, current_winstreak=current_winstreak, raw_fkdr=raw_fkdr,
                  raw_wlr=raw_wlr, adjusted_fkdr=adjusted_fkdr, adjusted_wlr=adjusted_wlr, skill_score=skill_score)


def print_data(game_id: str, data: dict):
    print(CLEAR)
    print(f'Game {game_id}:\n')

    nicked_players = {}
    for player in list(data):
        if data[player] == 'Nicked. Unable to obtain Bedwars data.':
            nicked_players[player] = data[player]
            data.pop(player)

    spaces = len(longest_name(data))
    data = dict(sorted(data.items(), key=lambda item: item[1].skill_score, reverse=True))
    title = f'{"NAME":<{spaces}} |    LEVEL    | BW LEVEL | SKILL SCORE | FINAL KILLS | RAW FKDR | ADJ FKDR | BEDS BROKEN |  WINS  | RAW WLR | ADJ WLR | WINSTREAK |'
    print('=' * len(title))
    print(title)
    print('=' * len(title))

    for player in data:
        player_spaces = spaces - len(constants.RAW_RANK[data[player].network_rank])
        print(f'{data[player].network_rank}{player:<{player_spaces}}{C.end} | {data[player].network_level:^11} | '
              f'{data[player].bedwars_level:^8} | {C.bwhite}{data[player].skill_score:^11.2f}{C.end} | {data[player].final_kills:^11} | '
              f'{data[player].raw_fkdr:^8.2f} | {data[player].adjusted_fkdr:^8.2f} | {data[player].bed_breaks:^11} | '
              f'{data[player].games_won:^6} | {data[player].raw_wlr:^7.2f} | {data[player].adjusted_wlr:^7.2f} | '
              f'{data[player].current_winstreak:^9} |')
    for player in nicked_players:
        print(f'{player:<{spaces}} | {nicked_players[player]:^135} |')
    print('=' * len(title))
