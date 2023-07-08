import os
import logging
import sys
import json
import pickle
import shutil
from time import gmtime, strftime, time


class wsvc():
    def __init__(self):
        """Check wsvc repo if exists, assigns to `self.init`"""
        self.init = True if os.path.exists(".wsvc") else False
        self.currentstate = ""
        for item in os.listdir():
            if item.startswith("wsvc-commit") and os.path.isdir(item):
                shutil.rmtree(item)
    def create(self, reponame: str, force=False):
        """Initialize wsvc repo (name `reponame`)at `savedir`, overwriting if `force`"""
        if not os.path.exists(".wsvc"):
            os.makedirs(".wsvc")
        else:
            if force:
                logging.warning("Over-writing existing directory")
            else:
                logging.error("Path not created, dir already exists")
                sys.exit(-1)
        with open(".wsvc/config.json", "w") as config:
            data = json.dumps({"name": reponame, "created": strftime("%Y-%m-%d %H:%M:%S", gmtime())})
            config.write(data)

    def check(self):
        """Check if wsvc exists in folder"""
        return self.init

    def serialize(self) -> bool:
        """Serialize current repo into a string"""
        if not self.init:
            return False

        tempserial = {}

        for dirpath, dirnames, filenames in os.walk("."):
            if ".wsvc" in dirpath.split(os.sep):
                continue
            for file in filenames:
                file_path = os.path.join(dirpath, file)
                with open(file_path) as f:
                    content = f.read()
                    tempserial[file_path] = content

        self.currentstate = pickle.dumps(tempserial).hex()


    def stash(self, commitmsg):
        """Stashes changes away under name `commitmsg` """
        if not os.path.exists(".wsvc"):
            os.makedirs(".wsvc")
        with open(".wsvc/{0}-{1}.wsvccommit".format(round(time()), commitmsg), "w") as file:
            file.write(self.currentstate)
        print("Changes stashed")

    def grab(self, commit):
        """Grab commit `commit`"""
        files = next(os.walk(".wsvc"), (None, None, []))[2]
        commit_directory = f"wsvc-commit-{commit}"
        potentials = {}
        print(files)
        for file in files:
            if ".wsvccommit" in file:
                pass
            else:
                continue
            _temp = file.split("-")
            name = _temp[1].split(".")[0]
            ts = _temp[0]
            if name == commit:
                potentials[file] = ts
        sortedpots = sorted(potentials.items(), key=lambda item: item[1])
        match len(sortedpots):
            case 0:
                print(f"No matches found for commit {commit}")
                return
            case 1:
                print(f"Exactly 1 match found")
            case _:
                print(f"Multiple matches found. Selecting last commit.")
        with open(".wsvc/" + sortedpots[-1][0]) as f:
            contents = f.read().replace("\n", "")
            file_contents = pickle.loads(bytes.fromhex(contents))
        
        for file_path, value in file_contents.items():
            file_directory, file_name = os.path.split(file_path)
            file_directory = os.path.join(commit_directory, file_directory)
            if not os.path.exists(file_directory):
                os.makedirs(file_directory)

            # If the value is an empty string, create an empty file
            if not value:
                open(os.path.join(file_directory, file_name), "w").close()
            else:
                with open(os.path.join(file_directory, file_name), "w") as f:
                    f.write(value)
    def delete(self):
        shutil.rmtree(".wsvc")


instance = wsvc()
if len(sys.argv) > 1:

    action = sys.argv[1]
    if action == "init":
        instance.create(reponame=sys.argv[2], force=False)
    elif action == "del":
        instance.delete()
    elif action == "check":
        print("Exists:", instance.check())
    elif action == "stash":
        instance.serialize()
        instance.stash(sys.argv[2])
    elif action == "grab":
        instance.grab(sys.argv[2])
    else:
        print("Invalid action")
else:
    print("No action specified")
