#!/usr/bin/env python3
import sys
if sys.version_info < (3, 5):
    raise Exception("Error: must use python 3.5 or greater")

import re
import argparse
from ruamel.yaml import YAML
from versio.version import Version
from versio.version_scheme import Pep440VersionScheme, Simple3VersionScheme, Simple4VersionScheme, PerlVersionScheme, \
            Simple5VersionScheme, VariableDottedIntegerVersionScheme


YAML_FILE = "example.yaml"
MAP_FILE = "map.yaml"

class Log(object):
    logging = True
    def __init__(self, string, i=0, logging=True):
        if self.logging == False or logging == False: return
        print( (" " * (i*4)) + string )
class Debug(Log):
    logging = False

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
    scheme = None
    def __init__(self, bump):
        self.bump = bump
        # Defaulting to the Pep440 version scheme for this class
        self.scheme = Pep440VersionScheme
    def do(self, ver):
        # Bump version
        Debug("self.bump: %s" % self.bump)

        # If bump is a list of bumps to perform, create a new class instance
        # and set its bump, do the bump, then return result
        if isinstance(self.bump, list):
            for item in self.bump:
                classn = self.__class__
                Debug("Creating v2 classn(%s)" % item)
                v2 = classn(item)
                Debug("Running v2.do(%s)" % ver)
                ver = v2.do( str(ver) )
                Debug("v2.do() result: %s" % ver)
            return

        myver = Version(ver, scheme=self.scheme)
        myver.bump(self.bump)
        Debug("ForceSemanticVer(%s) bump '%s': %s" % (ver, self.bump, myver))
        # Make sure we return a string, not a Version() object
        return str(myver)

#>>> Pep440VersionScheme.fields = ['release', 'pre', 'post', 'dev', 'local']
#>>> Pep440VersionScheme.format_str = '{0}{1}{2}{3}{4}'
#>>> Pep440VersionScheme.subfields = {'tiny2': ['Release', 3], 'major': ['Release', 0], 'tiny': ['Release', 2], 'minor': ['Release', 1]}
class ForceSemanticVer(SemanticVersion):
    def do(self, ver):
        Debug("do(%s)" % ver)
        # Clean up version string
        #ver.strip()
        regex = re.compile(r"^v", re.IGNORECASE)
        Debug("regex '%s' ver '%s' ver type '%s'" % (regex, ver, type(ver)))
        match = regex.search(ver)
        if match:
            Debug("Found and replaced a leading 'v' in version string")
            ver = regex.sub("", ver)
        return super().do(ver)

class BumpVers(object):
    y = {}
    logging = True

    def load_f(self, name, path):
        #yaml = YAML(typ='unsafe')
        yaml = YAML()
        yaml.register_class(SemanticVersion)
        yaml.register_class(ForceSemanticVer)
        self.y[name] = yaml.load(path)

    def walk_data(self, m, d, i=0):
        Debug("\n")
        Debug("d: '%s', type: '%s'" % (d, type(d)), i)
        Debug("m: '%s', type: '%s'" % (m, type(m)), i)

        if isinstance(d, dict):
            for key in d.keys():
                Debug("d key '%s'" % key, i)
                for mkey in m.keys():
                    if key == mkey:
                        Debug("Found key '%s' matching map key" % key, i)
                        self.walk_data( m[mkey], d[key], i+1 )
        elif isinstance(d, list) or isinstance(d, tuple):
            raise Exception("TODO: please finish this code path")
            for item in d:
                Debug("d item '%s'" % key, i)
                #for mitem in m:
                self.walk_data( m, item, i+1 )
        else:
            Debug("d entry: '%s', type: '%s'" % (d, type(d)), i)
            if isinstance(m, SemanticVersion):
                Debug("found SemanticVersion", i)
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
