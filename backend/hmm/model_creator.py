import numpy as np
import hmms
import json
from os import listdir
import os

ITERATIONS = 100

class ModelCreator():

    def __init__(self, in_path, map_file, out_file):
        self.map = load_json(map_file)
        self.out_file = out_file
        self.in_path = in_path
        self.indata = self.create_joint_json()


    def create_model(self):
        print("[DEBUG] Creating model for {}".format(self.in_path))
        inst_n = len(self.map)
        V = [np.array(v) for v in self.indata["v"]]
        print("[DEBUG] {} possible instructions, {} samples".format(inst_n, len(self.indata["v"])))

        dhmm_r = hmms.DtHMM.random(4, inst_n) # 4 Hidden States, inst_n Visible States
        dhmm_r.baum_welch(V, ITERATIONS)

        print("[DEBUG] Baum welch finished, saving file")

        dhmm_r.save_params(self.out_file)


    def train_model(self):
        inst_n = len(self.map)
        V = [np.array(v) for v in self.indata["v"]]
        print("[DEBUG] {} possible instructions, {} samples".format(inst_n, len(self.indata["v"])))
        dhmm_r = hmms.DtHMM.from_file(self.out_file+".npz")
        dhmm_r.baum_welch(V, ITERATIONS)
        print("[DEBUG] Baum welch finished, saving file")
        dhmm_r.save_params(self.out_file)

    def create_joint_json(self):
        files = listdir(self.in_path)
        jsons = []
        joint = {}
        joint["v"] = []

        for f in files:
            jsons.append(load_json(os.path.join(self.in_path, f)))

        for j in jsons:
            v = []
            for ins in j["v"]:
                if ins in self.map:
                    v.append(self.map[ins])
                else:
                    v.append(0) # other
            if len(v) != 0:
                joint["v"].append(v)

        return joint


def load_json(path):
    with open(path, "r") as d:
        data = json.load(d)
    return data
