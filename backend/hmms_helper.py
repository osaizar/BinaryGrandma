import threading
import os
import hashlib
from config import *
from models import *
from db_helper import DB
from hmm.disassembler import Disassembler
from hmm.map_creator import MapCreator
from hmm.model_creator import ModelCreator
from hmm.model_comparator import ModelComparator


def get_file_sha_hash(file):
    hasher = hashlib.sha256()
    with open(file, 'rb') as f:
        while True:
            data = f.read(65536) # 64kb chunks
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()


def create_model_thr(model_id):
    db = DB()
    model = db.get_model_by_id(model_id)

    bin_path = os.path.join(FILE_UPLOAD_FOLDER, model.filename)
    model_path = os.path.join(MODEL_FOLDER, model.filename)
    diss_path = os.path.join(model_path, "diss")
    map_path = os.path.join(model_path, "map.json")
    model_file_path = os.path.join(model_path, "model")

    os.system("mkdir {}".format(bin_path))
    os.system("mkdir {}".format(model_path))
    os.system("mkdir {}".format(diss_path))
    os.system("unzip {} -d {} > /bin/false".format(bin_path+".zip", bin_path))
    bin_files = os.listdir(bin_path)

    for i, binf in enumerate(bin_files):
        Disassembler(os.path.join(bin_path, binf)).disassemble_to_file(os.path.join(diss_path, str(i)+".json"))

    MapCreator(diss_path, map_path).create_map()
    ModelCreator(diss_path, map_path, model_file_path).create_model()

    db.set_model_analyzed(model.id)
    os.system("rm {}".format(bin_path+".zip"))
    os.system("rm -rf {}".format(bin_path))


def create_model(model_id):
     thr = threading.Thread(target=create_model_thr,
                            args=(model_id,)).start()


def analyze_binary_thr(binary_id):
    db = DB()
    binary = db.get_binary_by_id(binary_id)
    models = db.get_available_models()

    bin_path = os.path.join(FILE_UPLOAD_FOLDER, binary.filename+".bin")
    diss_path = os.path.join(DISS_BINARY_FOLDER, binary.filename+".json")

    hash = get_file_sha_hash(bin_path)
    db.binary_add_hash(binary.id, hash)

    Disassembler(bin_path).disassemble_to_file(diss_path)

    for m in models:
        model_path = os.path.join(MODEL_FOLDER, m.filename)
        map_path = os.path.join(model_path, "map.json")
        model_file_path = os.path.join(model_path, "model.npz")
        rating = ModelComparator(diss_path, map_path, model_file_path).get_rating()

        db.add(Result(binary.id, m.id, rating))

    os.system("rm {}".format(bin_path))


def analyze_binary(binary_id):
     thr = threading.Thread(target=analyze_binary_thr,
                            args=(binary_id,)).start()
