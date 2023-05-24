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
    return round(math.sqrt(data['player'].get('networkExp', 0)*0.0008 + 12.25) - 2.5, 2)


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


def longest_name(data: dict, nicked_players: dict) -> str:
    name = []
    for player_name in data:
        name.append(player_raw_display_name(player_name, data, nicked=False))
    for player_name in nicked_players:
        name.append(player_raw_display_name(player_name, data, nicked=True))
    long = max(name, key=len)
    return long


def player_raw_display_name(name: str, data: dict, nicked: bool) -> str:
    if nicked:
        return f'<nicked> {name}'
    return f'{constants.RAW_RANK[data[name].network_rank]}{name}'


def level_color(level: int) -> str:
    if level >= 600:
        return C.bdarkred  # NOTE: your terminal may require customization to bold the dark colors
    elif level >= 500:
        return C.bdarkcyan
    elif level >= 400:
        return C.bdarkgreen
    elif level >= 300:
        return C.bcyan
    elif level >= 200:
        return C.darkyellow
    elif level >= 100:
        return C.bwhite
    else:
        return C.black


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
    skill_score = 5 * wilson_ratio(math.floor(index), final_deaths) + (index/160)**0.65 - 5

    return Player(bedwars_level=bedwars_level, network_level=network_level, network_rank=network_rank,
                  final_kills=final_kills, final_deaths=final_deaths, bed_breaks=bed_breaks, bed_losses=bed_losses,
                  games_won=games_won, games_lost=games_lost, current_winstreak=current_winstreak, raw_fkdr=raw_fkdr,
                  raw_wlr=raw_wlr, adjusted_fkdr=adjusted_fkdr, adjusted_wlr=adjusted_wlr, skill_score=skill_score)


def print_data(game_id: str, data: dict):
    print(CLEAR)
    print(f'Game {game_id}:\n')

    nicked_players = {}
    for player_name in list(data):
        if data[player_name] == '[Player nicked - no data]':
            nicked_players[player_name] = data[player_name]
            del data[player_name]

    spaces = len(longest_name(data, nicked_players))

    data = dict(sorted(data.items(), key=lambda item: item[1].skill_score, reverse=True))
    title = (f'{"NAME":<{spaces}} |  NETWORK LEVEL  | BW LEVEL | SKILL SCORE'
             + f' ||| FINAL KILLS | RAW FKDR | ADJ FKDR | BEDS BROKEN |  WINS  | RAW WLR | ADJ WLR | WINSTREAK |')
    print('=' * len(title))
    print(title)
    print('=' * len(title))

    for player_name in data:
        player_spaces = spaces - len(constants.RAW_RANK[data[player_name].network_rank])
        print(f'{data[player_name].network_rank}{player_name:<{player_spaces}}{C.end}'
              f' | {data[player_name].network_level:^15}'
              f' | {level_color(data[player_name].bedwars_level)}{data[player_name].bedwars_level:^8}{C.end}'
              f' | {C.bwhite}{data[player_name].skill_score:^11.1f}{C.end}'
              f' ||| {data[player_name].final_kills:^11}'
              f' | {C.black}{data[player_name].raw_fkdr:^8.2f}{C.end}'
              f' | {data[player_name].adjusted_fkdr:^8.2f}'
              f' | {data[player_name].bed_breaks:^11}'
              f' | {data[player_name].games_won:^6}'
              f' | {C.black}{data[player_name].raw_wlr:^7.2f}{C.end}'
              f' | {data[player_name].adjusted_wlr:^7.2f}'
              f' | {data[player_name].current_winstreak:^9}'
              f' |')
    for player_name in nicked_players:
        display_name = player_raw_display_name(player_name, data, nicked=True)
        print(f'{display_name:<{spaces}} | {nicked_players[player_name]:^135} |')
    print('=' * len(title))
