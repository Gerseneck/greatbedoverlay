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


def main():

    print('\033[H\033[2J')
    print('GreatOverlay')

    log = pl.Path('~/.lunarclient/offline/multiver/logs/latest.log').expanduser().open('r')
    key = 'f8a22fc3-6849-44ec-9da8-77d3f419b440'

    if not key:
        print('You do not have an api key. Join Hypixel and send `/api new` for a key.')
        return 

    match_data = {}
    match_name = ''

    while True:
        log_lines = tail(log)
        for line in log_lines:
            if '[CHAT]' not in line:
                continue
            if 'has joined' in line:
                name = line.split(' ')[4]
                uuid = util.get_uuid(name)
                if uuid:
                    stat = util.get_stats(key, uuid)
                    match_data[name] = util.get_info(stat)
                else:
                    match_data[name] = 'Nicked. Unable to obtain bedwars data.'
                print('\033[H\033[2J')
                print(f'Game {match_name}:')
                print()
                util.print_data(match_data)
            if 'Sending you to' in line:
                match_name = line.split(' ')[7][:-1]
                match_data = {}


if __name__ == '__main__':
    main()
