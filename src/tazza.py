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
    print(f'[ERROR]: {path}:{row+1}:{col+1}: {message}')
    exit(code)

@dataclass(slots=True, kw_only=True)
class CmdDetail:
    file_path: str = ''
    execute: bool = False
    command: bool = False
    getc: bool = False

TAZZA_EXTENSION = '.tazza'

class TokenType(Enum):
    UNKNOWN = auto()
    STRING_LITERAL = auto()
    CONST_NUMBER = auto()
    IDENTIFIER = auto()

@dataclass(slots=True, kw_only=True)
class Token:
    ttype: TokenType = TokenType.UNKNOWN
    txt: str
    row: int
    col: int

def find_end(predicate, begin: int, line: str) -> int:
    end = begin + 1
    while predicate(line, end):
        end += 1
    return end + 1 if line[begin] == '"' else end # return "****"

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
                detail.command = True
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

    if not detail.command:
        cmd_error_message(f'command not provided')
    if not detail.file_path:
        cmd_error_message(f'file not provided')

    print(detail)

    with open(detail.file_path, 'r') as f:
        SYMBOLS = '=;:(){}[]+-*/'
        source: list[str] = f.read().splitlines(keepends=True)
        list_of_tokens: list[Token] = []
        for row, line in enumerate(source):
            # for each line in source
            col, line_length = 0, len(line)
            while col < line_length:
                token_type = TokenType.UNKNOWN
                # each iteration append a token
                token_begin, token_end = col, None
                if line[col].isalpha():
                    token_end = find_end(lambda l, c: l[c].isalpha(), token_begin, line) # keyword or identifier 
                    # token_type = get_token_from_alpha()
                elif line[col] == '"':
                    token_end = find_end(lambda l, c: l[c] != '"' or l[c-1] == '\\', token_begin, line) # string literal 
                    token_type = TokenType.STRING_LITERAL
                elif line[col].isnumeric():
                    token_end = find_end(lambda l, c: l[c].isnumeric(), token_begin, line) # constant
                    token_type = TokenType.CONST_NUMBER
                elif line[col].isspace():
                    col += 1
                    continue # next col
                else:
                    # symbol
                    if line[col] == '/' and line[col + 1] in ['n', '/']:
                        break # no more token on this line
                    token_end = token_begin + 1
                    # if line[col] not in SYMBOLS:
                    #     compilation_error(f'`{line[col]}` not recognized', row, col, detail.file_path)
                    # token_type = get_token_from_symbol(line, token_begin, token_end)

                
                col = token_end
                list_of_tokens.append(Token(ttype=token_type, txt=line[token_begin:token_end], row=row, col=token_begin))

    __import__('pprint').pprint(list_of_tokens)

if __name__ == '__main__':
    main()
