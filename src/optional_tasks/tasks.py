import pathlib

import appdirs

from optional_tasks.colors import Colors
from optional_tasks.times import *
import optional_tasks.exceptions as exceptions
import optional_tasks.files as files


class Task:
    def __init__(self, id: int, name: str, difficulty: int, tags: set, completions: list = []) -> None:
        self.id = id
        self.name = name
        self.difficulty = difficulty
        self.tags = tags
        self.completions = completions

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data['id'], data['name'], data['difficulty'], data['tags'], data['completions'])

    def __str__(self):
        return self.__dict__.__str__()


class Tasks:
    def __init__(self):
        appname = "optional_tasks"
        appauthor = "IceArrow256"
        user_data_dir = appdirs.user_data_dir(appname, appauthor)
        self.file = pathlib.Path(user_data_dir) / 'tasks.json'
        self.tasks: list = [Task.from_dict(task)
                            for task in files.load_json(self.file, False)]
        self.lens = self.__count_lengths()

    def add(self, name: str, difficulty: int, tags: set):
        ids = [task.id for task in self.tasks if task.id != None] or [-1]
        names: list = [task.name for task in self.tasks]
        if name not in names:
            self.tasks.append(Task(max(ids) + 1, name, difficulty, tags))
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
        files.save_json([task.__dict__ for task in self.tasks], self.file)

    def __sort(self, sort: str):
        if (sort == 'name'):
            self.tasks.sort(key=lambda x: x.name, reverse=False)
        elif (sort == 'difficulty'):
            self.tasks.sort(key=lambda x: x.difficulty, reverse=False)
        elif (sort == 'count'):
            self.tasks.sort(key=lambda x: len(x.completions), reverse=False)
        elif (sort == 'score'):
            self.tasks.sort(key=lambda x: len(x.completions) * x.difficulty, reverse=False)
        elif (sort == 'date'):
            self.tasks.sort(key=lambda x: max(
                x.completions or [0]), reverse=False)
        else:
            # sort by id
            self.tasks.sort(key=lambda x: x.id, reverse=False)

    def __tags_to_str(self, tags: set):
        result = str(tags)
        result = result.replace('[', '')
        result = result.replace(']', '')
        result = result.replace("'", '')
        return result

    def __count_lengths(self):
        lens = {}
        if self.tasks:
            lens['id'] = max(max([len(str(task.id))
                             for task in self.tasks]), 2)
            lens['name'] = max(max([len(task.name) for task in self.tasks]), 4)
            lens['tags'] = max(
                max([len(self.__tags_to_str(task.tags)) for task in self.tasks]), 4)
            lens['count'] = max(
                max([len(str(len(task.completions))) for task in self.tasks]), 5)
            lens['score'] = max(
                max([len(str(len(task.completions)*task.difficulty)) for task in self.tasks]), 5)
        else:
            lens['id'] = 2  # 'id'
            lens['name'] = 4  # 'name'
            lens['tags'] = 4  # 'tags'
            lens['count'] = 5  # 'count'
            lens['score'] = 5  # 'score'
        lens['difficulty'] = 10  # 'difficulty'
        lens['last completion date'] = 20
        return lens

    def __print_header(self):
        output = (f'| {Colors.HEADER}{"id":<{self.lens["id"]}}{Colors.ENDC} |'
                  f' {Colors.HEADER}{"name":<{self.lens["name"]}}{Colors.ENDC} |'
                  f' {Colors.HEADER}{"difficulty":<{self.lens["difficulty"]}}{Colors.ENDC} |'
                  f' {Colors.HEADER}{"tags":<{self.lens["tags"]}}{Colors.ENDC} |'
                  f' {Colors.HEADER}{"count":<{self.lens["count"]}}{Colors.ENDC} |'
                  f' {Colors.HEADER}{"score":<{self.lens["score"]}}{Colors.ENDC} |'
                  f' {Colors.HEADER}{"last completion date":<{self.lens["last completion date"]}}{Colors.ENDC} |')
        print(output)
        print('-'*(len(output) - 9*7))

    def __print_row(self, task: Task):
        last_completion_date = max(task.completions or [0])
        output = (f'| {task.id:<{self.lens["id"]}} |'
                  f' {task.name:<{self.lens["name"]}} |'
                  f' {task.difficulty:<{self.lens["difficulty"]}} |'
                  f' {self.__tags_to_str(task.tags):<{self.lens["tags"]}} |'
                  f' {len(task.completions):<{self.lens["count"]}} |'
                  f' {len(task.completions)*task.difficulty:<{self.lens["score"]}} |')
        if last_completion_date > get_unix_day_start_time():
            output += f' {Colors.OKGREEN}{unix_time_to_iso(last_completion_date):<{self.lens["last completion date"]}}{Colors.ENDC} |'
        else:
            output += f' {unix_time_to_iso(last_completion_date):<{self.lens["last completion date"]}} |'
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
        dates = set(date_score.keys())
        average_score = sum(date_score.values())/len(date_score.values())
        today_score = date_score[max(dates)]
        dates.remove(max(dates))
        yesterday_score = date_score[max(dates)]
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
            tags = dict(sorted(tags.items(), key=lambda item: item[1], reverse=True))
            for tag in tags:
                print(f' {tag} {tags[tag]}')
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
