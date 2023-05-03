#!/usr/bin/env python3

import sys, os
from dataclasses import dataclass

def help_message():
    print(' ---------------------------------------------------')
    print('| Tazza is a Programming Language written in Python |')
    print('| Command:                                          |')
    print('|     build      Compile code                       |')
    print('|     run        Compile and execute code           |')
    print('| Options:                                          |')
    print('|     --getc     Get C transpiled code              |')
    print(' ---------------------------------------------------')
    exit(0)

def cmd_error_message(message: str, code=1):
    print(f'[ERROR]: {message}')
    exit(code)

@dataclass(slots=True, kw_only=True)
class CmdDetail:
    file_path: str = ''
    execute: bool = False
    getc: bool = False

TAZZA_EXTENSION = '.tazza'

def main():
    argv = sys.argv
    i, argv_len = 1, len(argv)
    if argv_len == i:
        help_message()

    detail = CmdDetail()
    while i < argv_len:
        arg = argv[i]
        match arg:
            case '--getc':
                detail.getc = True
            case 'build' | 'run':
                if arg == 'run':
                    detail.execute = True
            case _:
                file_name = arg
                _, ext = os.path.splitext(file_name)
                if ext != TAZZA_EXTENSION:
                    cmd_error_message(f'{arg} not recognized')
                if not os.path.exists(file_name):
                    cmd_error_message(f'`{file_name}` not found')
                detail.file_path = file_name
        i += 1

    if not detail.file_path:
        cmd_error_message(f'file not provided')

    print(detail)


if __name__ == '__main__':
    main()
