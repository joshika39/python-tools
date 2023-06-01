from json_service import JsonService
from base import curr_dir
import os

users_path = os.path.join(curr_dir(), 'test.json')


if __name__ == "__main__":
    print("Writing")
    service = JsonService(users_path)
    # service.write("users/100006367207301/name", "Alma")
    service.write("asd/alma", "sad")
    service.write("asd/alma/rewq", False)
    service.write("asd/alma/igaz", True)



