import os,logging,sys
import json,pickle
from time import gmtime, strftime
import shutil
class wsvc():
    def __init__(self):
        """Check wsvc repo if exists, assigns to `self.init`"""
        self.init=True if os.path.exists(".wsvc") else False
        self.currentstate=""
    def create(self,reponame:str,force=False):
        """ Initialize wsvc repo (name `reponame`)at `savedir`, overwriting if `force` """
        if not os.path.exists(".wsvc"):
            os.makedirs(".wsvc")
        else:
            if force:
                logging.warning("Over-writing existsing directory")
            else:
                logging.error("Path not created, dir already exists")
                sys.exit(-1)
        with open(f".wsvc/config.json","w") as config:
            data=json.dumps({"name":reponame,"created":strftime("%Y-%m-%d %H:%M:%S", gmtime())})
            config.write(data)    
    def check(self):
        """Check if wsvc exists in folder"""
        return self.init
    def serialize(self) -> bool:
        """Serialize current repo into a string"""
        if not self.init:
            return False
        files=[os.path.join(dirpath,f) for (dirpath, dirnames, filenames) in os.walk(".") for f in filenames]
        tempserial={}
        for file in files:
            with open(file) as f:
                content=f.readlines()
                real=""
                for x in content:
                    real+=x
                tempserial[file]=real
        self.currentstate=pickle.dumps(tempserial)
    def stash(self,commitmsg):
        """Stashes changes away under name `commitmsg` """
        with open(f".wsvc/{commitmsg}.wsvc","w") as file:
            specialstate=str(self.currentstate)[2:]
            specialstate=specialstate[:-1]
            file.write(str(specialstate))
        print("Changes stashed")
    def grab(self,commit):
        """Grab commit `commit`"""
        pass
    def delete(self):
        shutil.rmtree(".wsvc")
instance=wsvc()
match sys.argv[1]:
    case "init":
        instance.create(reponame=sys.argv[2],force=False)
    case "del":
        instance.delete()
    case "check":
        print("Exists:",instance.check())
    case "stash":
        instance.serialize()
        instance.stash(sys.argv[2])