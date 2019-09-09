from models import *
from config import *
from db_helper import DB
from hmm.disassembler import Disassembler
from hmm.map_creator import MapCreator
from hmm.model_creator import ModelCreator
from hmm.model_comparator import ModelComparator
import os

def new_model(name, desc, benign, zipfile):
    db = DB()
    model = db.add(Model(name, desc, benign))
    cpdest = os.path.join(FILE_UPLOAD_FOLDER, model.filename+".zip")
    os.system("cp {} {}".format(zipfile, cpdest))
    hm.create_model(model.id)




if __name__ == "__main__":
    MODELS = [{"name" : "", "desc" : "", "benign" : True, "zipfile" : ""}]
    for i, m in enumerate(MODELS):
        print("[+] Starting model {}/{}".format(i, len(MODELS)))
        new_model(m["name"], m["desc"], m["benign"], m["zipfile"])
        print("[+] Endend model {}/{}".format(i, len(MODELS)))  
