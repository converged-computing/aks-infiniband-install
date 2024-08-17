#!/usr/bin/env python3

import subprocess
import argparse
import os
import sys

# usage
# python parse-links.py

parser = argparse.ArgumentParser()
parser.add_argument("--rename", help="rename the network to this name", default='ib0')
args = parser.parse_args()

links = subprocess.check_output(['ip', 'link']).decode('utf-8')
lines = [x for x in links.split('\n') if x.strip()]
lines = [x for x in lines if 'ib' in x]
lines = lines[0]
linkname = [x for x in lines.split(' ') if 'ib' in x][0].replace(':','')

print(f"Found link {linkname}")

# Rename
subprocess.check_output(["ip", "link", "set", linkname, "name", args.rename])
subprocess.check_output(["ip", "link", "set", args.rename, "up"])
