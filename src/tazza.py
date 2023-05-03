#!/usr/bin/env python3

import sys, os
from dataclasses import dataclass
from enum import Enum, auto

def help_message():
    print(' ---------------------------------------------------')
    print('| Tazza is a Programming Language written in Python |')
    print('| Command:                                          |')
    print('|     build       Compile code                      |')
    print('|     run         Compile and execute code          |')
    print('| Options:                                          |')
    print('|     --getc      Get C transpiled code             |')
    print(' ---------------------------------------------------')
    exit(0)

def cmd_error_message(message: str, code=1):
    print(f'[ERROR]: {message}')
    exit(code)

def compilation_error(message: str, row: int, col: int, path: str, code=1):
    print(f'[ERROR] {path}:{row}:{col}: {message}')
    exit(code)

@dataclass(slots=True, kw_only=True)
class CmdDetail:
    file_path: str = ''
    execute: bool = False
    action: bool = False
    getc: bool = False

TAZZA_EXTENSION = '.tazza'

class TokenType(Enum):
    UNKNOWN = auto()

@dataclass(slots=True, kw_only=True)
class Token:
    ttype: TokenType = TokenType.UNKNOWN
    txt: str
    row: int
    col: int

def find_end(predicate, begin: int, line: str) -> int:
    end = begin + 1
    while predicate(line[end]):
        end += 1
    return end + 1 if line[begin] == '"' else end

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
                detail.action = True
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
    if not detail.action:
        cmd_error_message(f'action not provided')

    print(detail)

    with open(detail.file_path, 'r') as f:
        SYMBOLS = '=;:(){}[]+-*/'
        source: list[str] = f.read().splitlines()
        list_of_tokens: list[Token] = []
        for row, line in enumerate(source):
            # for each line in source
            col, line_length = 0, len(line)
            while col < line_length:
                # each iteration append a token
                token_begin, token_end = col, None
                if line[col].isalpha():
                    token_end = find_end(lambda c: c.isalpha(), token_begin, line) # keyword or identifier 
                elif line[col] == '"':
                    token_end = find_end(lambda c: c != '"', token_begin, line) # string literal 
                elif line[col].isnumeric():
                    token_end = find_end(lambda c: c.isnumeric(), token_begin, line) # constant
                elif line[col].isspace():
                    col += 1
                    continue # try next col
                else:
                    # symbol
                    if line[col] == '/' and line[col + 1] == '/':
                        break # no more token on this line
                    if line[col] not in SYMBOLS:
                        compilation_error(f'`{line[col]}` not recognized', row, col, detail.file_path)
                    token_end = token_begin + 1
                
                col = token_end
                list_of_tokens.append(Token(txt=line[token_begin:token_end], row=row, col=token_begin))

    __import__('pprint').pprint(list_of_tokens)


if __name__ == '__main__':
    main()
