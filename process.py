#!/usr/bin/env python3
import sys
if sys.version_info < (3, 5):
    raise Exception("Error: must use python 3.5 or greater")

from ruamel.yaml import YAML
from versio.version import Version

import argparse

YAML_FILE = "example.yaml"
MAP_FILE = "map.yaml"

# Look in versio/version_scheme.py to see how to extend this with new
# version schemas, as well as what the supported bump fields are for
# existing schemas.
# 
# In the default schema (PEP440), a version is made up of "fields", the
# default of which is the "release" field, like "1.2.3" in "1.2.3rc1".
# Then there are "subfields" of the field, which would be "major" ("1"),
# "minor" ("2"), and "tiny" ("3").
# 
# Trying to bump a version from "1.2.3rc" to "1.2.3" will require an extra
# promote=True option to bump, and we'll probably need to support an extra
# mapping arg for this. #TODO
class SemanticVersion(object):
    def __init__(self, bump):
        print("Found a semantic version!")
        self.bump = bump

    def do(self, ver):
        print("object '%s', version '%s'" % (self, ver))
        print("bump: %s" % self.bump)
        #>>> Pep440VersionScheme.fields
        #['release', 'pre', 'post', 'dev', 'local']
        #>>> Pep440VersionScheme.format_str
        #'{0}{1}{2}{3}{4}'
        #>>> Pep440VersionScheme.subfields
        #{'tiny2': ['Release', 3], 'major': ['Release', 0], 'tiny': ['Release', 2], 'minor': ['Release', 1]}

        ver = Version(ver)
        print("version: %s" % ver)

        return ver

class BumpVers(object):
    y = {}
    logging = True

    def load_f(self, name, path):
        #yaml = YAML(typ='unsafe')
        yaml = YAML()
        yaml.register_class(SemanticVersion)
        self.y[name] = yaml.load(path)

    def s(self, i):
        return " " * (i*4)
    def log(self, string, i=0):
        if self.logging == False: return
        print( (" " * (i*4)) + string )

    def walk_data(self, m, d, i=0):
        print("\n")
        self.log("d: '%s', type: '%s'" % (d, type(d)), i)
        self.log("m: '%s', type: '%s'" % (m, type(m)), i)

        if isinstance(d, dict):
            for key in d.keys():
                self.log("%sd key '%s'" % (self.s(i), key), i)
                for mkey in m.keys():
                    if key == mkey:
                        self.log("Found key '%s' matching map key" % key, i)
                        self.walk_data( m[mkey], d[key], i+1 )
        elif isinstance(d, list) or isinstance(d, tuple):
            raise Exception("TODO: please finish this code path")
            for item in d:
                self.log("%sd item '%s'" % (self.s(i), key), i)
                #for mitem in m:
                self.walk_data( m, item, i+1 )
        else:
            self.log("d entry: '%s', type: '%s'" % (d, type(d)), i)
            if isinstance(m, SemanticVersion):
                self.log("found SemanticVersion", i)
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
