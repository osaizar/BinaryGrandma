from models import *
from config import *
from db_helper import DB
import hmms_helper as hm
import os
import json
import sys
import argparse
import csv


def parse_arguments():
    argparser = argparse.ArgumentParser(prog="gVuln", \
                description="Binary Grandma CLI interface")
    argparser.add_argument("-m", "--model", help="Add a model.json file to create a model")
    argparser.add_argument("-b", "--binary", help="Add a binary.json file to analyze a binary set")
    argparser.add_argument("-csv", "--csv", help='The directory to write the results into')

    args = argparser.parse_args()
    return args


def new_model(name, desc, benign, zipfile):
    db = DB()
    model = db.add(Model(name, desc, benign))
    cpdest = os.path.join(FILE_UPLOAD_FOLDER, model.filename+".zip")
    os.system("cp {} {}".format(zipfile, cpdest))
    hm.create_model_thr(model.id)


def new_binary(name, file):
    db = DB()
    binary = db.add(Binary(name))
    cpdest = os.path.join(FILE_UPLOAD_FOLDER, binary.filename+".bin")
    os.system("cp {} {}".format(file, cpdest))
    hm.analyze_binary_thr(binary.id)


def get_results(binary_id):
    db = DB()
    results = []
    binary = db.get_binary_by_id(binary_id)
    results = db.get_results_by_binary_id(binary.id)

    if len(results) != 0:
        results = parse_results(results)
        for r in results:
            m = db.get_model_by_id(r.model)
            results.append({"model" : m.name, "score" : str(int(r.score))})

    return results


if __name__ == "__main__":
    args = parse_args()

    if args.model:
        with open(sys.argv[2]) as f:
            m = json.load(f)
        new_model(m["name"], m["desc"], m["benign"], m["zipfile"])
    elif args.binary:
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
    elif args.csv:
        db = DB()
        binary_names = db.get_binary_names()
        for bin_name in binary_names:
            binaries = db.get_binaries_by_name(bin_name)
            with open(os.path.join(args.csv, bin_name+".csv"), "w") as wfile:
                writer = csv.writer(wfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL )
                for bin in binaries:
                    results = get_results(bin.id)
                    results = ["{} ({})".format(r["model"], r["score"]) if int(r["score"]) > 60 for r in results]
                    writer.writerow([str(bin.id), str(results)])
