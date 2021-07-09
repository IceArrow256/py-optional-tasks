import sys
import argparse

from optional_tasks.colors import Colors
from optional_tasks.tasks import Tasks
from optional_tasks.exceptions import NameAlreadyExistError


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
                        'id', 'name', 'difficulty', 'count', 'date', 'score'], help='set sort by')
    parser.add_argument('-c', '--complete', type=int,
                        help='complete task with id')
    args = parser.parse_args()

    t = Tasks()
    if args.add and args.edit == None and args.complete == None:
        if args.name:
            name = ' '.join(args.name)
            try:
                t.add(name, args.difficulty, args.tags)
            except NameAlreadyExistError as e:
                print(F'{Colors.FAIL}{e}{Colors.ENDC}', file=sys.stderr)
                exit()
    elif args.edit and not args.add and args.complete == None:
        if args.name:
            name = ' '.join(args.name)
        else:
            name = None
        try:
            t.edit(args.edit, name, args.difficulty, args.tags)
        except NameAlreadyExistError as e:
            print(F'{Colors.FAIL}{e}{Colors.ENDC}', file=sys.stderr)
            exit()
    elif args.complete != None and args.edit == None and not args.add:
        t.complete(args.complete)
    elif args.complete != None and args.add != None and args.edit != None:
        print(F'{Colors.FAIL}Invalid argument combination{Colors.ENDC}',
              file=sys.stderr)
        exit()
    else:
        t.print(args.group, args.sort)


if __name__ == '__main__':
    main()
