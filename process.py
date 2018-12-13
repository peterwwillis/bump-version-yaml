#!/usr/bin/env python3
import sys
if sys.version_info < (3, 5):
    raise Exception("Error: must use python 3.5 or greater")

#from ruamel.yaml import YAML
import ruamel.yaml

YAML_FILE = "example.yaml"
MAP_FILE = "map.yaml"

class SemanticVersion(object):
    def __init__(self, bump):
        self.bump = bump

class BumpVers(object):
    def load_y(self, path):
        yaml = YAML()
        with open(YAML_FILE) as f:
            yaml.load(f)
        return yaml

    def walk_file(self, m, d):
        for entry in d:
            print("d entry: %s" % entry)

    def bump_vers(self, data_file, map_file):
        data = load_y(data_file)
        dmap = load_y(map_file)
        self.walk_file(dmap, data)

def main():
    v = BumpVers()
    v.bump_vers(YAML_FILE, MAP_FILE)

if __name__ == "__main__":
    main()
