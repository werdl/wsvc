import os,logging,sys
import json
from time import gmtime, strftime
import shutil


class wsvc():
    def __init__(self):
        self.init=True if os.path.exists(".wsvc") else False
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
    def delete(self):
        shutil.rmtree(".wsvc")
instance=wsvc()
match sys.argv[1]:
    case "init":
        instance.create(reponame=sys.argv[2],force=False)
    case "del":
        instance.delete()