import pathlib as pl
import time

import util


def tail(file):
    file.seek(0, 2)
    while True:
        lines = file.readline()
        if not lines:
            time.sleep(0.1)
            continue
        yield lines


def set_data(name: str, key: str, match_data: dict):
    uuid = util.get_uuid(name)
    if uuid:
        stat = util.get_stats(key, uuid)
        if not stat:
            print('Invalid API key. Join Hypixel and execute `/api new` for a new key.')
            return
        match_data[name] = util.get_info(stat)
    else:
        match_data[name] = 'Nicked. Unable to obtain Bedwars data.'


def main():

    print('\033[H\033[2J')
    print('GreatOverlay')

    log = pl.Path('~/.lunarclient/offline/multiver/logs/latest.log').expanduser().open('r')
    key = input('Please enter an API key: ')
    print(key)

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
                print('Queue detected! If nothing shows up, type /who')
            if 'ONLINE:' in line:
                name = line.replace(', ', ' ').split()[5:]
                for n in name:
                    set_data(n, key, match_data)
                print('\033[H\033[2J')
                print(f'Game {match_name}:\n')
                util.print_data(match_data)
            if 'has joined' in line:
                name = line.split()[4]
                set_data(name, key, match_data)
                print('\033[H\033[2J')
                print(f'Game {match_name}:\n')
                util.print_data(match_data)
            if 'has quit' in line:
                name = line.split()[4]
                match_data.pop(name)
                print('\033[H\033[2J')
                print(f'Game {match_name}:\n')
                util.print_data(match_data)


if __name__ == '__main__':
    main()
