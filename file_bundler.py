#!/usr/bin/env

import sys
import os
from zipfile import ZipFile


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

INPUTPATH = sys.argv[1]
print(get_all_files(INPUTPATH))    
