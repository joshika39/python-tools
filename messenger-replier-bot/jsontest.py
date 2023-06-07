from json_service import JsonService
from base import curr_dir
import os

users_path = os.path.join(curr_dir(), 'test.json')


if __name__ == "__main__":
    print("Writing")
    service = JsonService(users_path)
    # service.write("users/100006367207301/name", "Alma")
    # service.write("", "users", ["u1", "u2", "u3", "u4"])
    # service.write("settings", "visibility", "visible")
    # service.write("settings", "password", "asd123")
    # service.write("settings", "email", "test@asd.com")
    service.write("conv/id1/type", "person")
    service.write("conv/id2/type", "person")
    service.write("conv/id3/type", "group")
    service.write("conv/id3/last_read", "none")
    service.write("conv/id3/last_read", "Ufff")
    service.write("conv/id3/keep_open", True)

    # service.write("asd/alma", "test2", "sad")
    # service.write("asd/alma/rewq", False)
    # service.write("asd/alma/igaz", True)



