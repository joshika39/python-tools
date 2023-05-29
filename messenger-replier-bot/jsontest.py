from json_service import JsonService
from base import curr_dir
import os

users_path = os.path.join(curr_dir(), 'test.json')


if __name__ == "__main__":
    service = JsonService(users_path)

    test = service.write("users/100006367207301/name", "Alma")

