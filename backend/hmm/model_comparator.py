import numpy as np
import hmms
import json


class ModelComparator():

    def __init__(self, bin_file, map_file, model_file):
        self.bin_file = bin_file
        self.map = load_json(map_file)
        self.model_file = model_file
        self.bin_data = self.get_mapped_bin()


    def get_mapped_bin(self):
        j = load_json(self.bin_file)
        rt = {"v" : []}

        for ins in j["v"]:
            if ins in self.map:
                rt["v"].append(self.map[ins])
            else:
                rt["v"].append(0) # other

        return rt


    def get_rating(self):
        print("[DEBUG] Getting rating for {} model and {} file".format(self.model_file, self.bin_file))
        dhmm = hmms.DtHMM.from_file(self.model_file)
        print("[DEBUG] Model loaded")
        estimate = dhmm.emission_estimate(np.array(self.bin_data["v"]))
        print("[DEBUG] Got rating {}".format(estimate))
        return estimate # np.exp() ??



def load_json(path):
    with open(path) as d:
        data = json.load(d)
    return data
