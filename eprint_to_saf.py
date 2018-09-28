import csv
import json
import lxml
import os
import sys

path_dictionary = sys.argv[1]

class DirLookup(dict):
    '''Class for directory lookup dictionary'''
    def __init__(self, filepath):
        with open(filepath) as handle:
            data = json.load(handle)
            for row in data:
                id = str(row['eprintid'])
                dir = row['dir']
                self[id] = dir


class DSpaceSAF():
    '''Class for creating simple archive format packages'''
    def __init__(self):
        pass
    
    def write(self, path):
        if not os.path.isdir(path):
            os.mkdir(path)
        with open(os.path.join(path, 'contents'), 'w') as chandle:
            pass
            # write files line by line
        with open(os.path.join(path, 'dublin_core.xml'), 'w') as dchandle:
            pass
            # write dc xml
            # copy files one by one into this directory


def main():
    
    d = DirLookup(path_dictionary)
    print(d)


if __name__ == "__main__":
    main()
