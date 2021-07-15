from datetime import date
from os import name
import pathlib

import appdirs

from optional_tasks.colors import Colors
from optional_tasks.times import *
from optional_tasks.task import Task
import optional_tasks.exceptions as exceptions
import optional_tasks.files as files


class Tasks:
    def __init__(self, is_short_header):
        appname = "optional_tasks"
        appauthor = "IceArrow256"
        user_data_dir = appdirs.user_data_dir(appname, appauthor)
        self.file = pathlib.Path(user_data_dir) / 'tasks.json'
        self.tasks: list = [Task.from_dict(task)
                            for task in files.load_json(self.file, False)]
        if is_short_header:
            self.headers = {
                'id': 'id',
                'name': 'name',
                'difficulty': 'd',
                'tags': 'tags',
                'count': 'c',
                'score': 's',
                'today count': 'tc',
                'today score': 'ts',
                'last completion date': 'last completion_date'
            }
        else:
            self.headers = {
                'id': 'id',
                'name': 'name',
                'difficulty': 'difficulty',
                'tags': 'tags',
                'count': 'count',
                'score': 'score',
                'today count': 'today count',
                'today score': 'today score',
                'last completion date': 'last completion_date'
            }
        self.lens = self.__count_lengths()

    def add(self, name: str, difficulty: int, tags: set):
        ids = [task.id for task in self.tasks if task.id != None] or [-1]
        names: list = [task.name for task in self.tasks]
        if name not in names:
            self.tasks.append(Task(max(ids) + 1, name, difficulty or 1, tags))
        else:
            raise exceptions.NameAlreadyExistError(
                'Task with this name already exists')

    def edit(self, id: int, name, difficulty: int, tags: set):
        target_task = None
        for task in self.tasks:
            if task.id == id:
                target_task = task
                self.tasks.remove(task)
        names: list = [task.name for task in self.tasks]
        if name not in names and target_task:
            self.tasks.append(Task(target_task.id,
                                   name or target_task.name,
                                   difficulty or target_task.difficulty,
                                   tags or target_task.tags,
                                   target_task.completions))
        else:
            self.tasks.append(target_task)
            raise exceptions.NameAlreadyExistError(
                'Task with this name already exists')

    def complete(self, id):
        for task in self.tasks:
            if task.id == id:
                task.completions.append(get_current_unix_time())

    def __del__(self):
        self.tasks.sort(key=lambda x: x.id, reverse=False)
        for task in self.tasks:
            task.tags = sorted(task.tags)
        files.save_json([task.__dict__ for task in self.tasks], self.file)

    def __sort(self, sort: str):
        if (sort == 'name'):
            self.tasks.sort(key=lambda x: x.name, reverse=False)
        elif (sort == 'difficulty'):
            self.tasks.sort(key=lambda x: x.difficulty, reverse=False)
        elif (sort == 'count'):
            self.tasks.sort(key=lambda x: len(x.completions), reverse=False)
        elif (sort == 'score'):
            self.tasks.sort(key=lambda x: len(x.completions)
                            * x.difficulty, reverse=False)
        elif (sort == 'tcount'):
            self.tasks.sort(key=lambda x: len(
                x.get_today_completions()), reverse=False)
        elif (sort == 'tscore'):
            self.tasks.sort(key=lambda x: len(x.get_today_completions())
                            * x.difficulty, reverse=False)
        elif (sort == 'date'):
            self.tasks.sort(key=lambda x: max(
                x.completions or [0]), reverse=False)
        else:
            # sort by id
            self.tasks.sort(key=lambda x: x.id, reverse=False)

    def __count_lengths(self):
        lens = {}
        if self.tasks:
            lens['id'] = max(max([len(str(task.id))
                             for task in self.tasks]), len(self.headers['id']))
            lens['name'] = max(max([len(task.name)
                               for task in self.tasks]), len(self.headers['name']))
            lens['tags'] = max(max([len(task.get_tags())
                               for task in self.tasks]), len(self.headers['tags']))
            lens['count'] = max(
                max([len(str(len(task.completions))) for task in self.tasks]), len(self.headers['count']))
            lens['score'] = max(
                max([len(str(len(task.completions)*task.difficulty)) for task in self.tasks]), len(self.headers['score']))
            lens['today count'] = max(
                max([len(str(len(task.get_today_completions()))) for task in self.tasks if task]), len(self.headers['today count']))
            lens['today score'] = max(
                max([len(str(len(task.get_today_completions())*task.difficulty)) for task in self.tasks]), len(self.headers['today score']))
        else:
            lens['id'] = 2  # 'id'
            lens['name'] = len(self.headers['name'])  # 'name'
            lens['tags'] = len(self.headers['tags'])  # 'tags'
            lens['count'] = len(self.headers['count'])  # 'count'
            lens['score'] = len(self.headers['score'])  # 'score'
            lens['today count'] = len(self.headers['today count'])  # 'count'
            lens['today score'] = len(self.headers['today score'])  # 'score'
        lens['difficulty'] = max(
            len(self.headers['difficulty']), 2)   # 'difficulty'
        lens['last completion date'] = max(
            len(self.headers['last completion date']), 19)
        return lens

    def __print_header(self):
        output = (f'{Colors.UNDERLINE}{self.headers["id"]:<{self.lens["id"]}}{Colors.ENDC} '
                  f'{Colors.UNDERLINE}{self.headers["name"]:<{self.lens["name"]}}{Colors.ENDC} '
                  f'{Colors.UNDERLINE}{self.headers["difficulty"]:<{self.lens["difficulty"]}}{Colors.ENDC} '
                  f'{Colors.UNDERLINE}{self.headers["tags"]:<{self.lens["tags"]}}{Colors.ENDC} '
                  f'{Colors.UNDERLINE}{self.headers["count"]:<{self.lens["count"]}}{Colors.ENDC} '
                  f'{Colors.UNDERLINE}{self.headers["score"]:<{self.lens["score"]}}{Colors.ENDC} '
                  f'{Colors.UNDERLINE}{self.headers["today count"]:<{self.lens["today count"]}}{Colors.ENDC} '
                  f'{Colors.UNDERLINE}{self.headers["today score"]:<{self.lens["today score"]}}{Colors.ENDC} '
                  f'{Colors.UNDERLINE}{self.headers["last completion date"]:<{self.lens["last completion date"]}}{Colors.ENDC}')
        print(output)

    def __print_row(self, task: Task):
        last_completion_date = max(task.completions or [0])
        output = (f'{task.id:<{self.lens["id"]}} '
                  f'{task.name:<{self.lens["name"]}} '
                  f'{task.difficulty:<{self.lens["difficulty"]}} '
                  f'{task.get_tags():<{self.lens["tags"]}} '
                  f'{len(task.completions):<{self.lens["count"]}} '
                  f'{len(task.completions)*task.difficulty:<{self.lens["score"]}} '
                  f'{len(task.get_today_completions()):<{self.lens["today count"]}} '
                  f'{len(task.get_today_completions())*task.difficulty:<{self.lens["today score"]}} ')
        if last_completion_date == 0:
            output += f'{Colors.FAIL}{"never":<{self.lens["last completion date"]}}{Colors.ENDC}'
        elif last_completion_date > get_unix_day_start_time():
            output += f'{Colors.OKGREEN}{unix_time_to_iso(last_completion_date):<{self.lens["last completion date"]}}{Colors.ENDC}'
        else:
            output += f'{unix_time_to_iso(last_completion_date):<{self.lens["last completion date"]}}'
        print(output)

    def __count_total_score(self):
        today_score = 0
        date_score = {}
        for task in self.tasks:
            for completion in task.completions:
                unix_day_start = get_unix_day_start_time(completion)
                unix_day_end = unix_day_start+SECOND_IN_DAY
                if unix_day_start <= completion < unix_day_end:
                    if unix_day_start not in date_score:
                        date_score[unix_day_start] = 0
                    date_score[unix_day_start] += task.difficulty
        try:
            average_score = sum(date_score.values())/len(date_score.values())
        except ZeroDivisionError as e:
            average_score = 0
        today_score = date_score[get_unix_day_start_time(
        )] if get_unix_day_start_time() in date_score else 0
        unix_yesterday_start = get_unix_day_start_time()-SECOND_IN_DAY
        yesterday_score = date_score[unix_yesterday_start] if unix_yesterday_start in date_score else 0
        print(f'average score: {average_score}')
        print(f'yesterday score: {yesterday_score}')
        print(f'today score: {today_score}')

    def print(self, group: str, sort: str):
        self.__sort(sort)
        self.__print_header()
        if (group == 'difficulty'):
            difficulties = set()
            for task in self.tasks:
                difficulties.add(task.difficulty)
            difficulties = sorted(difficulties)
            for difficulty in difficulties:
                print(f'difficulty: {difficulty}')
                for task in [task for task in self.tasks if task.difficulty == difficulty]:
                    self.__print_row(task)
                print()
        elif (group == 'tags'):
            tags = {}
            for task in self.tasks:
                for tag in task.tags:
                    if tag not in tags:
                        tags[tag] = 0
            for tag in tags:
                for task in [task for task in self.tasks if tag in task.tags]:
                    tags[tag] += len(task.completions) * task.difficulty
            tags = dict(
                sorted(tags.items(), key=lambda item: item[1], reverse=True))
            for tag in tags:
                print(f'{tag} {tags[tag]}')
                for task in [task for task in self.tasks if tag in task.tags]:
                    self.__print_row(task)
                print()
        elif (group == 'count'):
            counts = set()
            for task in self.tasks:
                counts.add(len(task.completions))
            counts = sorted(counts)
            for count in counts:
                print(f'count: {count}')
                for task in [task for task in self.tasks if len(task.completions) == count]:
                    self.__print_row(task)
                print()
        else:
            for task in self.tasks:
                self.__print_row(task)
        print()
        self.__count_total_score()
