#!/usr/bin/env python3

import csv
import json
import os
import sys
from zipfile import ZipFile

INPUTPATH = sys.argv[1]
DIRLOOKUP = sys.argv[2]
OUTPUTPATH = sys.argv[3]

BASE = "/Volumes/GoogleDrive/Team Drives/DPI Team Drive/Project Docs/saf_builder"

# https://drumdev.lib.umd.edu:8084/1903.DEV/

def get_all_files(inputpath):
    ZIPPATH = os.path.join(inputpath, 'revisions.zip')
    allfiles = []
    to_zip = []
    for root, dirs, files in os.walk(inputpath):
        for f in files:
            if f.startswith('.'):
                continue
            filepath = os.path.join(root, f)
            if root.endswith('revisions'):
                to_zip.append(filepath)
            else:
                allfiles.append(filepath)
    with ZipFile(ZIPPATH, 'a') as zip:
        for fullpath in to_zip:
            filename = os.path.basename(fullpath)
            zip.write(fullpath, arcname=filename)
        allfiles.append(ZIPPATH)
    return allfiles


def generate_dirs(filepath):
    with open(filepath) as handle:
        data = json.load(handle)
        lookup = {}
        for row in data:
            id = row['eprintid']
            dir = row['dir']
            lookup[str(id)] = dir
    return lookup

class DSpaceSAF():
    '''Class for creating simple archive format packages'''
    def __init__(self):
        pass
    
    def write(self, path):
        if not os.path.isdir(path):
            os.mkdir(path)
        with open(os.path.join(path, 'contents'), 'w') as chandle:
            # write files line by line
        with open(os.path.join(path, 'dublin_core.xml'), 'w') as dchandle:
            # write dc xml
        # copy files one by one into this directory
        

def main():
    with open(INPUTPATH) as inhandle, open(OUTPUTPATH, 'w') as outhandle:
        fieldnames = inhandle.readline().strip().split(',')
        fieldnames.append('filename')
        inhandle.seek(0)
        reader = csv.DictReader(inhandle)
        writer = csv.DictWriter(outhandle, fieldnames=fieldnames)
        writer.writeheader()
        data = [row for row in reader]
        path_lookup = generate_dirs(DIRLOOKUP)
        for row in data:
            id = row['dc.identifier.other']
            path = os.path.join(BASE, path_lookup[id])
            files = get_all_files(path)
            row['filename'] = " || ".join(files)
            writer.writerow(row)


if __name__ == "__main__":
    main()
