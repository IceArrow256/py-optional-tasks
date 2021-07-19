import sys

from optional_tasks.colors import Colors
from optional_tasks.tasks import Tasks
from optional_tasks.exceptions import NameAlreadyExistError
from optional_tasks.args import Args


def main():
    args = Args()
    t = Tasks(args.is_short_header)
    if args.current_action == 'add':
        try:
            t.add(args.description, args.priority, args.tags)
        except NameAlreadyExistError as e:
            print(F'{Colors.FAIL}{e}{Colors.ENDC}', file=sys.stderr)
            exit()
    elif args.current_action == 'edit':
        try:
            t.edit(args.id, args.description, args.priority, args.tags)
        except NameAlreadyExistError as e:
            print(F'{Colors.FAIL}{e}{Colors.ENDC}', file=sys.stderr)
            exit()
    elif args.current_action == 'complete':
        t.complete(args.id)
    elif args.current_action == 'remove':
        t.remove(args.id)
    elif args.current_action == 'list':
        t.print(args.group, args.sort)


if __name__ == '__main__':
    main()
