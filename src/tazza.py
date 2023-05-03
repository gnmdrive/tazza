#!/usr/bin/env python3

import sys


def help_message():
    print(' ---------------------------------------------------')
    print('| Tazza is a Programming Language written in Python |')
    print('| Command:                                          |')
    print('|     build      Compile code                       |')
    print('|     run        Compile and execute code           |')
    print('| Options:                                          |')
    print('|     --getc     Get C transpiled code              |')
    print(' ---------------------------------------------------')


def main():
    if len(sys.argv) == 1:
        help_message()


if __name__ == '__main__':
    main()
