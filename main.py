
from __future__ import annotations

import pathlib as pl
import sys
import time

import util
from constants import C
from api import get_uuid, get_api_data


def tail(file):
    file.seek(0, 2)
    while True:
        lines = file.readline()
        if not lines:
            time.sleep(0.1)
            continue
        yield lines


def set_data(player_name: str, key: str, match_data: dict):
    if player_name in match_data:
        return
    uuid = get_uuid(player_name)
    if uuid:
        api_data = get_api_data(key, uuid)
        if api_data['player'] is not None:
            match_data[player_name] = util.get_info(api_data)
        else:
            match_data[player_name] = f'{C.bdarkred}Nicked. Unable to obtain bedwars data.{C.end}'
    else:
        match_data[player_name] = f'{C.bdarkred}Nicked. Unable to obtain bedwars data.{C.end}'


def main():

    print('\033[H\033[2J')
    print('GreatBedOverlay')

    # TODO Setup config file for client, API key
    log = pl.Path('~/.lunarclient/offline/multiver/logs/latest.log').expanduser().open('r')

    if len(sys.argv) == 2:
        print('Using the API key passed from args')
        key = sys.argv[1]
    else:
        key = input('Please enter an API key: ')

    if not key:
        print('You do not have an api key. Join Hypixel and execute `/api new` for a key.')
        return

    match_data = {}
    match_name = ''

    while True:
        log_lines = tail(log)
        for line in log_lines:
            if '[CHAT]' not in line:
                continue

            if 'Sending you to' in line:
                match_name = line.strip().split(' ')[7][:-1]
                match_data = {}

            if 'ONLINE:' in line:
                player_names = line.replace(', ', ' ').split()[5:]
                for name in player_names:
                    set_data(name, key, match_data)
                util.print_data(match_name, match_data)
            if 'has joined' in line:
                player_name = line.split()[4]
                set_data(player_name, key, match_data)
                util.print_data(match_name, match_data)
                if int(line.split()[7][1]) > len(match_data):
                    print(f'{C.yellow}Less players detected! Run /who to update all players{C.end}')
            if 'has quit' in line:
                player_name = line.split()[4]
                if player_name in match_data:
                    match_data.pop(player_name)
                util.print_data(match_name, match_data)


if __name__ == '__main__':
    main()
