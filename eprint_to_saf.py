import csv
import json
from lxml import etree
import os
import sys
import yaml


class DirLookup(dict):
    '''Class for directory lookup dictionary'''
    def __init__(self, filepath):
        with open(filepath) as handle:
            self.update({
                str(row['eprintid']): row['dir'] for row in json.load(handle)
                })


class DSpaceSAF():
    '''Class for creating simple archive format packages'''
    def __init__(self, metadatapath, datapath, outputpath):
        self.basedir  = outputpath
        self.contents = os.path.join(self.basedir, 'contents')
        self.dc_file  = os.path.join(self.basedir, 'dublin_core.xml')
        self.zippath  = os.path.join(self.basedir, 'revisions.zip')
        self.datapath = datapath
        self.metadata = metadatapath
        self.lookup_files()
    
    def write(self, path):
        # create item SAF dir
        # create contents file
        # create revisions zip 
        # create dublin_core.xml
        # copy files one by one into this directory
        if not os.path.isdir(path):
            os.mkdir(path)
        with open(os.path.join(path, 'contents'), 'w') as chandle:
            for f in self.files:
                chandle.write(os.path.basename(f))
        
    def lookup_files(self):
        self.files = []
        self.revisions = []
        for root, dirs, files in os.walk(self.datapath):
            for f in files:
                fullpath = os.path.join(root, f)
                if f.startswith('.'):  # skip hidden files
                    continue
                elif root.endswith('revisions'):
                    self.revisions.append(fullpath)
                else:
                    self.files.append(fullpath)
    
    def generate_dcxml(self):
        root = etree.Element("dublin_core")
        for key, value in self.metadata.items():
            for instance in value.split(" || "):
                child = root.append(etree.Element("dcvalue", element=key))
                child.text = instance
        with open(self.dc_file, 'w') as handle:
            etree.write(handle, xml_declaration=True, encoding='UTF-8',
                        pretty_print=True)

    def create_revisions_zip(self):
        with ZipFile(self.zippath, 'a') as zip:
            for f in self.files:
                filename = os.path.basename(fullpath)
                zip.write(fullpath, arcname=filename)

    def copy_eprint_files(self):
        pass


def main():
    # create SAF object with metadata dict, 
    #    data path, and outputpath + Item_{n}
    # create contents file
    # create metadata xml
    # create revisions zip
    # copy files to SAF

    with open(sys.argv[1]) as handle:
        config = yaml.load(handle)

    # load lookup dictionary
    lookup = DirLookup(os.path.join(config['ROOT'], 
                                    config['PATH_LOOKUP']))
    
    # load metadata spreadsheet
    spreadsheet = os.path.join(config['ROOT'], 
                               config['METADATA'])
    
    # walk the data
    with open(spreadsheet) as handle:
        reader = csv.DictReader(handle)
        for n, row in enumerate(reader):
            # lookup path using eprint id
            print(n, row)


    
    #testobj = DSpaceSAF()
    #print(testobj.__dict__)


if __name__ == "__main__":
    main()
