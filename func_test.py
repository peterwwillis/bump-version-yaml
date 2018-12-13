#!/usr/bin/env python3
import sys
if sys.version_info < (3, 5):
    raise Exception("Error: must use python 3.5 or greater")

import unittest
from subprocess import run

class TestCmdLine(unittest.TestCase):
    exe = "./process.py"
    def test_tool(self):
        cp = run( [ self.exe, "example.yaml", "map.yaml" ] )
        self.assertEqual(cp.returncode, 0)

if __name__ == "__main__":
    unittest.main()
