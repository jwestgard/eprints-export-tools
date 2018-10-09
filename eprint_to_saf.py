import csv
import json
from lxml import etree
import os
import sys
import yaml
from zipfile import ZipFile


class DirLookup(dict):
    '''Class for directory lookup dictionary'''
    def __init__(self, filepath):
        with open(filepath) as handle:
            self.update({
                str(row['eprintid']): row['dir'] for row in json.load(handle)
                })


class DSpaceSAF():
    '''Class for creating simple archive format packages'''
    def __init__(self, metadata, inputpath, outputpath):
        self.id        = metadata.get('dc.identifier.other')
        self.metadata  = metadata
        self.filespath = inputpath
        self.basedir   = outputpath
        self.contents  = os.path.join(self.basedir, 'contents')
        self.dc_file   = os.path.join(self.basedir, 'dublin_core.xml')
        self.zippath   = os.path.join(self.basedir, 'revisions.zip')

        #self.lookup_files()
    
    def write(self):
        # create item SAF dir
        try:
            os.mkdir(self.basedir)
        except FileExistsError:
            print("Output dir exists: {0}".format(self.basedir)) 
        # create contents file
        with open(self.contents, 'w') as chandle:
            for f in self.files:
                chandle.write(os.path.basename(f))
        # create revisions zip
        self.create_revisions_zip()
        # create dublin_core.xml
        self.generate_dcxml()
        # copy files one by one into this directory
        self.copy_eprint_files()

        
    def lookup_files(self):
        self.files = []
        self.revisions = []
        for root, dirs, files in os.walk(self.filespath):
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
            if value is not None and value != '':
                for instance in value.split(" || "):
                    child = etree.Element("dcvalue", element=key)
                    child.text = instance
                    root.append(child)
        with open(self.dc_file, 'w') as handle:
            etree.write(handle, xml_declaration=True, encoding='UTF-8',
                        pretty_print=True)

    def create_revisions_zip(self):
        with ZipFile(self.zippath, 'a') as zip:
            for f in self.files:
                filename = os.path.basename(f)
                zip.write(f, arcname=filename)

    def copy_eprint_files(self):
        pass


def main():
    # load batch configuration
    with open(sys.argv[1]) as handle:
        config = yaml.load(handle)

    # load lookup dictionary
    lookup = DirLookup(os.path.join(config['ROOT'], 
                                    config['PATH_LOOKUP']))

    # load metadata spreadsheet
    spreadsheet = os.path.join(config['ROOT'], 
                               config['METADATA'])

    # base dir for input
    files_base = os.path.join(config['ROOT'], config['DATA'])

    # base dir for output
    saf_base = os.path.join(config['ROOT'], config['SAF_DIR'])
    try:
        os.mkdir(saf_base)
        print("Created output dir: {0}".format(saf_base)) 
    except FileExistsError:
        print("Output dir exists: {0}".format(saf_base)) 
    
    # walk the data
    with open(spreadsheet) as handle:
        reader = csv.DictReader(handle)
        for n, row in enumerate(reader, 1):
            # lookup path using eprint id
            input_dir = os.path.join(files_base, 
                            lookup.get(row['dc.identifier.other'])
                            )
            # generate output path
            output_dir = os.path.join(saf_base, 
                                      'Item_{0}'.format(n)
                                      )
            # create SAF object with metadata dict, 
            # data path, and outputpath + Item_{n}
            saf = DSpaceSAF(dict(row), input_dir, output_dir)
            saf.lookup_files()
            saf.write()


if __name__ == "__main__":
    main()
