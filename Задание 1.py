#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import json
import pathlib
import colorama
from colorama import Fore


def selecting(line: str, flights: list, nom: str) -> None:
    """Выбор рейсов по типу самолёта"""
    count: int = 0
    print(Fore.RED + f'{line}')
    print(
        '| {:^4} | {:^20} | {:^15} | {:^16} |'.format(
            "№",
            "Место прибытия",
            "Номер самолёта",
            "Тип"))
    print(line)
    for i, num in enumerate(flights, 1):
        if nom == num.get('value', ''):
            count += 1
            print(Fore.BLUE +
                '| {:<4} | {:<20} | {:<15} | {:<16} |'.format(
                    count,
                    num.get('stay', ''),
                    num.get('number', ''),
                    num.get('value', 0)))
    print(Fore.RED + f'{line}')


def table(line: str, flights: list) -> None:
    """Вывод скиска рейсов"""
    print(Fore.RED + f'{line}')
    print(
        '| {:^4} | {:^20} | {:^15} | {:^16} |'.format(
            "№",
            "Место прибытия",
            "Номер самолёта",
            "Тип"))
    print(line)
    for i, num in enumerate(flights, 1):
        print(Fore.BLUE +
            '| {:<4} | {:<20} | {:<15} | {:<16} |'.format(
                i,
                num.get('stay', ''),
                num.get('number', ''),
                num.get('value', 0)
            )
        )
    print(Fore.RED + f'{line}')


def adding(flights: list, stay: str, number: str, value: str) -> list:
    flights.append(
        {
            'stay': stay,
            'number': number,
            'value': value
        }
    )
    return flights


def saving(file_name: str, flights: list) -> None:
    with open(file_name, "w", encoding="utf-8") as file_out:
        json.dump(flights, file_out, ensure_ascii=False, indent=4)
    work_dir: pathlib.Path = pathlib.Path.cwd()/file_name
    work_dir.replace(pathlib.Path.home()/file_name)


def opening(file_name: pathlib.Path) -> None:
    with open(file_name, "r", encoding="utf-8") as f_in:
        return json.load(f_in)


def main(command_line=None):
    colorama.init()
    file_parser: argparse.ArgumentParser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename",
        action="store",)
    parser: argparse.ArgumentParser = argparse.ArgumentParser("flights")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0")
    subparsers: argparse.ArgumentParser = parser.add_subparsers(dest="command")
    add: argparse.ArgumentParser = subparsers.add_parser(
        "add",
        parents=[file_parser])
    add.add_argument(
        "-s",
        "--stay",
        action="store",
        required=True,)
    add.add_argument(
        "-v",
        "--value",
        action="store",
        required=True,)
    add.add_argument(
        "-n",
        "--number",
        action="store",
        required=True,)
    _: argparse.ArgumentParser = subparsers.add_parser(
        "display",
        parents=[file_parser],)
    select: argparse.ArgumentParser = subparsers.add_parser(
        "select",
        parents=[file_parser],)
    select.add_argument(
        "-t",
        "--type",
        action="store",
        required=True,)
    args: argparse.ArgumentParser = parser.parse_args(command_line)
    is_dirty: bool = False
    name: pathlib.Path = args.filename
    home: pathlib.Path = pathlib.Path.home()/name

    if home.exists():
        flights: list = opening(home)
    else:
        flights: list = []

    line: str = '+-{}-+-{}-+-{}-+-{}-+'.format(
        '-' * 4,
        '-' * 20,
        '-' * 15,
        '-' * 16)

    if args.command == "add":
        flights: list = adding(flights, args.stay, args.number, args.value)
        is_dirty = True
    elif args.command == 'display':
        table(line, flights)
    elif args.command == "select":
        selecting(line, flights, args.type)
    if is_dirty:
        saving(args.filename, flights)


if __name__ == '__main__':
    main()