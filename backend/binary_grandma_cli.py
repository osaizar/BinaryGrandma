from models import *
from config import *
from db_helper import DB
import hmms_helper as hm
import os
import json
import sys

def new_model(name, desc, benign, zipfile):
    db = DB()
    model = db.add(Model(name, desc, benign))
    cpdest = os.path.join(FILE_UPLOAD_FOLDER, model.filename+".zip")
    os.system("cp {} {}".format(zipfile, cpdest))
    hm.create_model(model.id)


def new_binary(name, file):
    db = DB()
    binary = db.add(Binary(name))
    cpdest = os.path.join(FILE_UPLOAD_FOLDER, binary.filename+".bin")
    os.system("cp {} {}".format(file, cpdest))
    hm.analyze_binary(binary.id)


if __name__ == "__main__":
    if sys.argv[1] == "m" or sys.argv[1] == "model":
        with open(sys.argv[2]) as f:
            m = json.load(f)
        new_model(m["name"], m["desc"], m["benign"], m["zipfile"])
    elif sys.argv[1] == "f" or sys.argv[1] == "file":
        with open(sys.argv[2]) as f:
            m = json.load(f)

        cpdest = os.path.join(FILE_UPLOAD_FOLDER, m["zipfile"].split("/")[-1])
        bin_path = os.path.join(FILE_UPLOAD_FOLDER, m["name"].replace(" ",""))
        os.system("mkdir {}".format(bin_path))
        os.system("cp {} {}".format(m["zipfile"], cpdest))
        os.system("unzip {} -d {} > /dev/null".format(cpdest, bin_path))
        bin_files = os.listdir(bin_path)
        for f in bin_files:
            new_binary(m["name"], os.path.join(bin_path, f))
