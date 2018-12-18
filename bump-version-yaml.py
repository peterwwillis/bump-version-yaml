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

class Log(object):
    logging = True
    def __init__(self, string, i=0, logging=True):
        if self.logging == False or logging == False: return
        print( (" " * (i*4)) + string )
class Debug(Log):
    """ Debug class. To enable, set logging = True """
    logging = False

# Look in versio/version_scheme.py to see how to extend this with new
# version schemas, as well as what the supported bump fields are for
# existing schemas.
# 
# In the default schema (PEP440), a version is made up of "fields", the
# default of which is the "release" field (like "4.5.6" in "4.5.6rc1").
# Then there are "subfields" of the field, which would be "major" ("4"),
# "minor" ("5"), and "tiny" ("6").
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
        Debug("do(%s) self.bump: %s" % (ver, self.bump))

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
            return str(ver)

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
        stripver = re.search(r"^v", ver, re.IGNORECASE)
        if stripver:
            Debug("Found and replaced a leading 'v' in version string")
            ver = re.sub(r"^v", "", ver)
        ver = super().do(ver)
        Debug("got %s from super().do" % ver)
        if stripver:
            ver = "v" + ver
            Debug("Put the leading 'v' back on version")
        return ver


class BumpVers(object):
    data = {}

    def load_f(self, name, path):
        #yaml = YAML(typ='unsafe')
        yaml = YAML()
        yaml.register_class(SemanticVersion)
        yaml.register_class(ForceSemanticVer)
        self.data[name] = yaml.load(path)

    def walk_data(self, m, d, i=0):
        #Debug("\n")
        #Debug("d: '%s', type: '%s'" % (d, type(d)), i)
        #Debug("m: '%s', type: '%s'" % (m, type(m)), i)

        if isinstance(d, dict):
            for key in d.keys():
                Debug("d key '%s'" % key, i)
                for mkey in m.keys():
                    if key == mkey:
                        Debug("Found key '%s' matching map key" % key, i)
                        newm, newd = self.walk_data( m[mkey], d[key], i+1 )
                        # Replace the old value with the new one
                        Debug("oldd\n%s\nnewd\n%s\n" % (d[key], newd))
                        d[key] = newd
        elif isinstance(d, list) or isinstance(d, tuple):
            #TODO this code is not finished
            raise Exception("TODO: please finish this code path")
            for c, item in enumerate(d):
                Debug("d item '%s'" % key, i)
                #for mitem in m:
                newm, newd = self.walk_data( m, item, i+1 )
                d[c] = newd
        else:
            Debug("d entry: '%s', type: '%s'" % (d, type(d)), i)
            if isinstance(m, SemanticVersion):
                Debug("found SemanticVersion", i)
                d = m.do(d)
                Debug("d result: %s" % d)

        return m, d

    def bump_vers(self):
        self.walk_data( self.data["map"], self.data["data"] )

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
        # Overwrite data file with bumped copy
        fname = a.datafile[0].name
        a.datafile[0].close()
        with open(fname, 'w') as f:
            YAML().dump(v.data["data"], f)

if __name__ == "__main__":
    main()
