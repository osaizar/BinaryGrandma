import json
import sys
import os
from os import listdir, mkdir
import operator

class MapCreator():

    def __init__(self, in_path, out_file):
        self.in_path = in_path
        self.out_file = out_file


    def create_map(self):
        files = listdir(self.in_path)
        file_name = self.out_file.replace(".json","")+".json"
        jsons = []
        map = {}

        for f in files:
            with open(os.path.join(self.in_path, f)) as d:
                data = json.load(d)
                jsons.append(data)

        for j in jsons:
            v = []
            for ins in j["v"]:
                if ins not in map:
                    map[ins] = 1
                else:
                    map[ins] += 1

        if len(map) < 30:
            top = len(map)
        else:
            top = 30

        rt = {}

        for i in range(top):
            m = max(map.items(), key=operator.itemgetter(1))[0]
            map[m] = 0
            rt[m] = i+1

        rt["other"] = 0

        with open(file_name, 'w') as f:
            f.write(json.dumps(rt))
