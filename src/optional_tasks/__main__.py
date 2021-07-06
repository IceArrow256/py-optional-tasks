import sys
import argparse
import pathlib
import json

import appdirs

import optional_tasks.optional_tasks as optional_tasks
import optional_tasks.tasks as tasks


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def main():
    parser = argparse.ArgumentParser(
        description='To-do list for optional tasks.')
    parser.add_argument('-a', '--add', action='store_true', help='add task',)
    parser.add_argument('-e', '--edit', type=int, help='edit task with id')
    parser.add_argument('-n', '--name', nargs='+', help='name of task')
    parser.add_argument('-t', '--tags', nargs='+', help='add tags to task')
    parser.add_argument('-d', '--difficulty', type=int,
                        choices=range(1, 11), help='set difficulty to task')
    parser.add_argument(
        '-g', '--group', default='none', choices=['none', 'difficulty', 'tags', 'count', 'date'], help='set group by')
    parser.add_argument('-s', '--sort', default='id', choices=[
                        'id', 'name', 'difficulty', 'count', 'date'], help='set sort by')
    parser.add_argument('-c', '--complete', type=int,
                        help='complete task with id')
    args = parser.parse_args()

    t = tasks.Tasks()
    if args.add and args.edit == None and args.complete == None:
        if args.name:
            name = ' '.join(args.name)
            try:
                t.add(name, args.difficulty, args.tags)
            except tasks.NameAlreadyExistError as e:
                print(F'{Colors.FAIL}{e}{Colors.ENDC}', file=sys.stderr)
                exit()
    elif args.edit and not args.add and args.complete == None:
        if args.name:
            name = ' '.join(args.name)
        else:
            name = None
        try:
            t.edit(args.edit, name, args.difficulty, args.tags)
        except tasks.NameAlreadyExistError as e:
            print(F'{Colors.FAIL}{e}{Colors.ENDC}', file=sys.stderr)
            exit()
    elif args.complete != None and args.edit == None and not args.add:
        t.complete(args.complete)
    elif args.complete != None and args.add != None and args.edit != None:
        print(F'{Colors.FAIL}Invalid argument combination{Colors.ENDC}', file=sys.stderr)
        exit()
    else:
        t.print(args.group, args.sort)


if __name__ == '__main__':
    main()
