import json
import pathlib


def load_json(path: pathlib.Path, default_dict=True):
    if path.is_file():
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
