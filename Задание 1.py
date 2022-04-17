#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import pathlib
import colorama #type: ignore
from colorama import Fore, Back, Style


def tree(directory: pathlib.Path) -> None:
    print(Fore.RED + f'|-- {directory}')
    for path in sorted(directory.glob('*')):
        depth: int = len(path.relative_to(directory).parts)
        spacer: str = '\t' * depth
        print(Fore.YELLOW + f'{spacer}|-- \033 {path.name}')
        for new_path in sorted(directory.joinpath(path).glob('*')):
            depth2: int = len(new_path.relative_to(directory.joinpath(path)).parts)
            spacer2: str = '\t\t' * depth2
            print(Fore.BLUE + f'{spacer2}|-- \033 {new_path.name}')



def main(command_line=None):
    colorama.init()
    way: pathlib.Path = pathlib.Path.cwd()
    file_parser: argparse.ArgumentParser = argparse.ArgumentParser(add_help=False)
    parser: argparse.ArgumentParser = argparse.ArgumentParser("flights")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0")
    subparsers: argparse.ArgumentParser = parser.add_subparsers(dest="command")
    mv: argparse.ArgumentParser = subparsers.add_parser(
        "cd",
        parents=[file_parser])
    mv.add_argument(
        'filename',
        action="store")
    mv: argparse.ArgumentParser = subparsers.add_parser(
        "back",
        parents=[file_parser])
    mv.add_argument(
        'filename',
        action="store")
    args: argparse.ArgumentParser = parser.parse_args(command_line)
    if args.command == 'cd':
        way: pathlib.Path = way/args.filename
        tree(way)
    elif args.command == 'back':
        if '\\' in args.filename:
            lst: list = args.filename.split('\\')
            for i in lst:
                way: pathlib.Path = way.parent
        else:
            way: pathlib.Path = way.parent
        tree(way)
    elif args.command == None:
        tree(way)


if __name__ == "__main__":
    main()