import os

from string import Template


class SQLProvider:

    def __init__(self, file_path: str):
        self._scripts = {}
        for file in os.listdir(file_path):
            self._scripts[file] = Template(open(f'{file_path}/{file}').read())

    def get(self, name: str, **kwargs) -> str:
        if name not in self._scripts:
            raise ValueError(f'No such file {name}')
        return self._scripts[name].substitute(**kwargs)
