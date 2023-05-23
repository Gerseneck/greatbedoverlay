"""Constants"""


class C:
    bwhite = '\033[1;97m'
    no = '\033[9;91m'
    #
    white = '\033[0;97m'
    yellow = '\033[0;93m'
    green = '\033[0;92m'
    blue = '\033[0;94m'
    cyan = '\033[0;96m'
    red = '\033[0;91m'
    magenta = '\033[0;95m'
    black = '\033[0;90m'
    darkwhite = '\033[0;37m'
    darkyellow = '\033[0;33m'
    darkgreen = '\033[0;32m'
    darkblue = '\033[0;34m'
    darkcyan = '\033[0;36m'
    darkred = '\033[0;31m'
    darkmagenta = '\033[0;35m'
    darkblack = '\033[0;30m'
    end = '\033[0;0m'


CLEAR = '\033[H\033[2J'


RANK = {
    'NORMAL': '',
    'VIP': f'{C.green}[VIP] ',
    'VIP_PLUS': f'{C.green}[VIP{C.yellow}+{C.green}] ',
    'MVP': f'{C.cyan}[MVP] ',
    'MVP_PLUS': f'{C.cyan}[MVP{C.red}+{C.cyan}] ',
    'SUPERSTAR': f'{C.darkyellow}[MVP{C.red}++{C.darkyellow}] ',
    'YOUTUBER': f'{C.red}[{C.white}YOUTUBE{C.red}] ',
    'MOJANG': f'{C.darkyellow}[MOJANG] ',
    'EVENTS': f'{C.darkyellow}[EVENTS] ',
    'MCP': f'{C.red}[MCP] ',
    'MODERATOR': f'{C.darkgreen}[GM] ',
    'ADMIN': f'{C.darkred}[ADMIN] ',
    'OWNER': f'{C.darkred}[OWNER] '
}
