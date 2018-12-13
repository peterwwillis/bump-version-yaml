#!/usr/bin/env python3
import sys
if sys.version_info < (3, 5):
    raise Exception("Error: must use python 3.5 or greater")

from ruamel.yaml import YAML
import argparse

YAML_FILE = "example.yaml"
MAP_FILE = "map.yaml"

class SemanticVersion(object):
    def __init__(self, bump):
        print("Found a semantic version!")
        self.bump = bump

    def do(self, ver):
        print("object '%s', version '%s'" % (self, ver))
        print("bump: %s" % self.bump)
        return ver

class BumpVers(object):
    y = {}

    def load_f(self, name, path):
        #yaml = YAML(typ='unsafe')
        yaml = YAML()
        yaml.register_class(SemanticVersion)
        self.y[name] = yaml.load(path)

    def s(self, i):
        return " " * (i*4)

    def walk_data(self, m, d, i=0):
        print("\n")
        print( self.s(i) + "d: '%s', type: '%s'" % (d, type(d)) )
        print( self.s(i) + "m: '%s', type: '%s'" % (m, type(m)) )

        if isinstance(d, dict):
            for key in d.keys():
                print( "%sd key '%s'" % (self.s(i), key) )
                for mkey in m.keys():
                    if key == mkey:
                        print( self.s(i) + "Found key '%s' matching map key" % key)
                        self.walk_data( m[mkey], d[key], i+1 )
        elif isinstance(d, list) or isinstance(d, tuple):
            raise Exception("TODO: fix me")
            for item in d:
                print("i %i" % i)
                print( "%sd item '%s'" % (self.s(i), key) )
                #for mitem in m:
                self.walk_data( m, item, i+1 )
        else:
            print( self.s(i) + "d entry: '%s', type: '%s'" % (d, type(d)) )
            if isinstance(m, SemanticVersion):
                print( self.s(i) + "found SemanticVersion")
                d = m.do(d)


    def bump_vers(self):
        self.walk_data( self.y["map"], self.y["data"] )

def options():
    parser = argparse.ArgumentParser(description='Bump version strings in YAML files')
    parser.add_argument('datafile', nargs=1, type=argparse.FileType('r'), help='The YAML file to bump versions in')
    parser.add_argument('mapfile', nargs=1, type=argparse.FileType('r'), help='The YAML map of where the versions are and how to bump them')
    return parser


def main():
    p = options()
    a = p.parse_args()
    if a.datafile != None and a.mapfile != None:
        v = BumpVers()
        v.load_f('data', a.datafile[0])
        v.load_f('map', a.mapfile[0])
        v.bump_vers()

if __name__ == "__main__":
    main()
