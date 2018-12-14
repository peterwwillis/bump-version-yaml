#!/usr/bin/env python3
import sys
if sys.version_info < (3, 5):
    raise Exception("Error: must use python 3.5 or greater")

import unittest
from subprocess import run
from shutil import copyfile
import os

class TestCmdLine(unittest.TestCase):
    exe = "./process.py"
    def test_tool(self):
        copyfile("example.yaml", "example.yaml.tmp")
        cp = run( [ self.exe, "example.yaml.tmp", "map.yaml" ] )
        cp2 = run( [ "diff", "-Naur", "example.yaml", "example.yaml.tmp" ] )
        os.remove("example.yaml.tmp")
        self.assertEqual(cp.returncode, 0)

if __name__ == "__main__":
    unittest.main()
