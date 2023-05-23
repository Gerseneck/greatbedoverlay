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


RANK = {
    'NORMAL': '',
    'VIP': f'{C.green}[VIP]{C.end}',
    'VIP_PLUS': f'{C.green}[VIP{C.yellow}+{C.green}]{C.end}',
    'MVP': f'{C.cyan}[MVP]{C.end}',
    'MVP_PLUS': f'{C.cyan}[MVP{C.red}+{C.cyan}]{C.end}',
    'SUPERSTAR': f'{C.darkyellow}[MVP{C.red}++{C.darkyellow}]{C.end}',
    'YOUTUBER': f'{C.red}[{C.white}YouTuber{C.red}]{C.end}',
    'HELPER': f'{C.darkblue}[Helper]{C.end}',
    'MODERATOR': f'{C.darkgreen}[Mod]{C.end}',
    'ADMIN': f'{C.darkred}[Admin]{C.end}',
}
