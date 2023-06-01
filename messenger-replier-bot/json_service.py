import os
import json


class JsonService():
    def __init__(self, json_path: str) -> None:
        if not os.path.exists(json_path):
            exit(1)
        self._json_path = json_path
        json_data = open(self._json_path, 'r').read()
        self._data = json.loads(json_data)  # type:dict

    def read(self, key: str) -> dict | list | str | int:
        if '/' in key:
            return self.read_subkey(key.split('/'), self._data)
        else:
            return self.read_subkey([key], self._data)

    def has_key(self, key: str) -> bool:
        if '/' in key:
            res = self.read_subkey(key.split('/'), self._data)
        else:
            res = self.read_subkey([key], self._data)

        return res is not None

    def read_subkey(self, keys: list[str], source: dict):
        if len(keys) == 0 or type(source) is not dict:
            return None

        if len(keys) == 1:

            if keys[0] in source.keys():
                return source[keys[0]]
            else:
                return None

        if keys[0] in source.keys():
            return self.read_subkey(keys[1:], source[keys[0]])

        return None

    def write_subkey(self, keys: list[str], source: dict, value) -> dict:
        if len(keys) == 0 or type(source) is not dict:
            return {}

        if len(keys) == 1:
            # if keys[0] in source.keys():s
            source[keys[0]] = value
            # else:
            #     return {keys[0]: value}

        return { keys[0]: self.write_subkey(keys[1:], source, value) }

    def write(self, key: str, value):
        if '/' in key:
            # keys = key.split('/')
            # fst_key = keys[0]
            self._data = self.write_subkey(key.split('/'), self._data, value)
            
        else:
            self._data[key] = value

        with open(self._json_path, "w") as outfile:
            json.dump(self._data, outfile)
