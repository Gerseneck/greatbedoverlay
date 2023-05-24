import pathlib as pl
import time

import util
from constants import C
from api import get_uuid, get_stats


def tail(file):
    file.seek(0, 2)
    while True:
        lines = file.readline()
        if not lines:
            time.sleep(0.1)
            continue
        yield lines


def set_data(name: str, key: str, match_data: dict):
    if name in match_data:
        return
    uuid = get_uuid(name)
    if uuid:
        stat = get_stats(key, uuid)
        try:
            match_data[name] = util.get_info(stat)
        except RuntimeError:
            match_data[name] = 'New'
    else:
        match_data[name] = 'Nicked. Unable to obtain Bedwars data.'


def main():

    print('\033[H\033[2J')
    print('GreatOverlay')

    # TODO Setup config file for client, API key
    log = pl.Path('~/.lunarclient/offline/multiver/logs/latest.log').expanduser().open('r')
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
                name = line.replace(', ', ' ').split()[5:]
                for n in name:
                    set_data(n, key, match_data)
                util.print_data(match_name, match_data)
            if 'has joined' in line:
                name = line.split()[4]
                set_data(name, key, match_data)
                util.print_data(match_name, match_data)
                if int(line.split()[7][1]) > len(match_data):
                    print(f'{C.yellow}Less players detected! Run /who to update all players{C.end}')
            if 'has quit' in line:
                name = line.split()[4]
                if name in match_data:
                    match_data.pop(name)
                util.print_data(match_name, match_data)


if __name__ == '__main__':
    main()
