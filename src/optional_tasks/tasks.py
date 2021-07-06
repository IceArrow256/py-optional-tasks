import json
import pathlib
import datetime

import appdirs


class NameAlreadyExistError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


def load_json(path: pathlib.Path, default_dict=True):
    if path.exists() and path.is_file():
        with open(path, encoding="utf8") as file:
            data = json.load(file)
        file.close()
        return data
    else:
        if default_dict:
            return {}
        else:
            return []


def save_json(data, path: pathlib.Path, indent=None):
    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding="utf-8") as file:
        file.write(json.dumps(data, ensure_ascii=False, indent=indent))
    file.close()


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
                            for task in load_json(self.file, False)]

    def add(self, name: str, difficulty: int, tags: list):
        ids = [task.id for task in self.tasks if task.id != None] or [-1]
        names: list = [task.name for task in self.tasks]
        if name not in names:
            self.tasks.append(Task(max(ids) + 1, name, difficulty, tags))
        else:
            raise NameAlreadyExistError('Task with this name already exists')

    def edit(self, id: int, name: str, difficulty: int, tags: list):
        target_task: Task = None
        for task in self.tasks:
            if task.id == id:
                target_task = task
                self.tasks.remove(task)
        names: list = [task.name for task in self.tasks]
        if name not in names:
            self.tasks.append(Task(target_task.id,
                                   name or target_task.name,
                                   difficulty or target_task.difficulty,
                                   tags or target_task.tags,
                                   target_task.completions))
        else:
            self.tasks.append(target_task)
            raise NameAlreadyExistError('Task with this name already exists')

    def complete(self, id):
        for task in self.tasks:
            if task.id == id:
                task.completions.append((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds())

    def __del__(self):
        self.tasks.sort(key=lambda x: x.id, reverse=False)
        save_json([task.__dict__ for task in self.tasks], self.file)

    def __sort(self, sort: str):
        if (sort == 'name'):
            self.tasks.sort(key=lambda x: x.name, reverse=False)
        elif (sort == 'difficulty'):
            self.tasks.sort(key=lambda x: x.difficulty, reverse=False)
        elif (sort == 'count'):
            self.tasks.sort(key=lambda x: len(x.completions), reverse=False)
        elif (sort == 'date'):
            self.tasks.sort(key=lambda x: max(x.completions), reverse=False)
        else:
            # sort by id
            self.tasks.sort(key=lambda x: x.id, reverse=False)

    def __print_header(self):
        id_len = max(max([len(str(task.id)) for task in self.tasks])+1, 3)
        name_len = max(max([len(task.name) for task in self.tasks])+1, 5)
        tags_len = max(max([len(str(task.tags)) for task in self.tasks])+1, 5)
        print(f'{"id":<{id_len}}{"name":<{name_len}}{"difficulty":<{11}}{"tags":<{tags_len}}{"completion count":<{len("completion count")+1}}{"last completion date"}')

    def __print_row(self, task: Task):
        id_len = max(max([len(str(task.id)) for task in self.tasks])+1, 3)
        name_len = max(max([len(task.name) for task in self.tasks])+1, 5)
        tags_len = max(max([len(str(task.tags)) for task in self.tasks])+1, 5)
        ts = max(task.completions)
        print(f'{task.id:<{id_len}}{task.name:<{name_len}}{task.difficulty:<11}{str(task.tags):<{tags_len}}{len(task.completions):<{len("completion count")+1}}{datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")}')

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
            tags = set()
            for task in self.tasks:
                for tag in task.tags:
                    tags.add(tag)
            tags = sorted(tags)
            for tag in tags:
                score = 0
                for task in [task for task in self.tasks if tag in task.tags]:
                    score += len(task.completions) * task.difficulty
                print(f'{tag} {score}')
                for task in [task for task in self.tasks if tag in task.tags]:
                    self.__print_row(task)
                print()
        elif (group == 'count'):
            counts = set()
            for task in self.tasks:
                counts.add(len(task.completions))
            counts = sorted(counts)
            for count in counts:
                print(f'completion count: {count}')
                for task in [task for task in self.tasks if len(task.completions) == count]:
                    self.__print_row(task)
                print()
        else:
            for task in self.tasks:
                self.__print_row(task)
