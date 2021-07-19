from optional_tasks.times import get_unix_day_start_time


class Task:
    def __init__(self, id: int, description: str, priority: int, tags: set, completions: list = []) -> None:
        self.id = id
        self.description = description
        self.priority = priority
        self.tags = tags
        self.completions = completions

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data['id'], data['description'], data['priority'], set(data['tags']), data['completions'])

    def __str__(self):
        return self.__dict__.__str__()

    def get_tags(self):
        result = str(self.tags)
        result = result.replace('{', '')
        result = result.replace('}', '')
        result = result.replace(',', '')
        result = result.replace("'", '')
        return result

    def get_today_completions(self):
        return [completion for completion in self.completions if completion >= get_unix_day_start_time()]
