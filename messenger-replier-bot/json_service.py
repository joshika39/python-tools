import os
import json

class JsonService():
    def __init__(self, json_path: str) -> None:
        if not os.path.exists(json_path):
            exit(1)
        self._json_path = json_path
        json_data = open(self._json_path, 'r').read()
        self._data = json.loads(json_data)  # type:dict
        

    def read(self, key: str) -> dict:
        if key in self._data.keys():
            return self._data[key]
        
        return None
    
    def write(self, key:str, value):
        if key in self._data.keys():
            self._data[key] = value
            
        with open(self._json_path, "w") as outfile:
            json.dump(self._data, outfile)
