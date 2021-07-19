import argparse
from os import register_at_fork
from sys import argv


class Args:
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='To-do list for optional tasks.')
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            '-a', '--add', type=str, help='add task with description', metavar='DESC')
        group.add_argument('-e', '--edit', type=int,
                           help='edit task with id', metavar='ID')
        group.add_argument('-r', '--remove', type=int,
                           help='remove task with id', metavar='ID')
        group.add_argument('-c', '--complete', type=int,
                           help='complete task with id', metavar='ID')
        parser.add_argument('-d', '--description',
                            type=str, help='set description', metavar='DESC')
        parser.add_argument('-t', '--tags', nargs='+',
                            help='set tags', metavar='TAG')
        parser.add_argument('-p', '--priority', type=int,
                            choices=range(1, 10), help='set priority')
        parser.add_argument(
            '-g', '--group', default='none', choices=['none', 'priority', 'tags', 'count', 'date'], help='set group by')
        parser.add_argument('-s', '--sort', default='id', choices=[
            'id', 'description', 'priority', 'count', 'date', 'score', 'tcount', 'tscore'], help='set sort by')
        # parser.add_argument('-c', '--complete', type=int,
        # help='complete task with id')
        parser.add_argument('--short', action='store_true',
                            help='short headers')
        self._args = parser.parse_args()

    @property
    def is_short_header(self):
        return self._args.short

    @property
    def current_action(self):
        if (self._args.add):
            return 'add'
        elif (self._args.edit):
            return 'edit'
        elif (self._args.remove):
            return 'remove'
        elif (self._args.complete):
            return 'complete'
        else:
            return 'list'

    @property
    def description(self):
        if self.current_action == 'add':
            return self._args.add
        else:
            return self._args.description

    @property
    def tags(self):
        print(self._args.tags)
        if self._args.tags:
            return set(self._args.tags)
        else:
            return None

    @property
    def priority(self):
        return self._args.priority or 1

    @property
    def id(self):
        if self.current_action == 'edit':
            return self._args.edit
        elif self.current_action == 'remove':
            return self._args.remove
        elif self.current_action == 'complete':
            return self._args.complete
        else:
            return None

    @property
    def group(self):
        return self._args.group

    @property
    def sort(self):
        return self._args.sort
