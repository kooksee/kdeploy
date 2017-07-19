# -*- coding: utf-8 -*-

base_log_key_words = [
    'created',
    'filename',
    'funcName',
    'levelname',
    'lineno',
    'module',
    'msg',
    'name',
    'asctime',
    'host_ip'
]


class Env(object):
    dev = "dev"
    local = "local"
    production = "pro"
    uat = "uat"


LOGO = """
                     ▄▄▄▄▄
            ▀▀▀██████▄▄▄       _______________
          ▄▄▄▄▄  █████████▄  /                 \\
         ▀▀▀▀█████▌ ▀▐▄ ▀▐█ | Gotta go fast!   |
       ▀▀█████▄▄ ▀██████▄██ | _________________/
       ▀▄▄▄▄▄  ▀▀█▄▀█════█▀ |/
            ▀▀▀▄  ▀▀███ ▀       ▄▄
         ▄███▀▀██▄████████▄ ▄▀▀▀▀▀▀█▌    _____________________________
       ██▀▄▄▄██▀▄███▀ ▀▀████      ▄██   █                             \\\\
    ▄▀▀▀▄██▄▀▀▌████▒▒▒▒▒▒███     ▌▄▄▀▀▀▀█_____________________________//
    ▌    ▐▀████▐███▒▒▒▒▒▐██▌
    ▀▄▄▄▄▀   ▀▀████▒▒▒▒▄██▀
              ▀▀█████████▀
            ▄▄██▀██████▀█
          ▄██▀     ▀▀▀  █
         ▄█             ▐▌
     ▄▄▄▄█▌              ▀█▄▄▄▄▀▀▄
    ▌     ▐                ▀▀▄▄▄▀
     ▀▀▄▄▀     ██
 \  ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀ ▀
 \- ▌          ▀▀▀▀▀▀▀▀▀▀▀▀▀▀              ▀ ▀
  - ▌        (o)        (o)       (o)          ▀
 /- ▌            Go Go Go !               ▀ ▀              Service:{0}
 /  ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀ ▀                   Version 0.1
               ██
"""
