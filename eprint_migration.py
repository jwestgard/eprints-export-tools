#!/usr/bin/env python3

import csv
import json
import os
import requests
import sys

def read_from_json(inpath):
    if os.path.isfile(inpath):
        with open(inpath, 'r') as inhandle:
            print('Reading from JSON: {0}'.format(inpath))
            data = json.load(inhandle)
            return data
    else:
        print('ERROR: Input file not found.')
        sys.exit()

def write_csv(outpath, data):
    with open(outpath, 'w') as outhandle:
        print('Writing to CSV: {0}'.format(outpath))
        datakeys = list(data[0].keys())
        writer = csv.DictWriter(outhandle, 
                                fieldnames=datakeys, 
                                lineterminator='\n')
        writer.writeheader()
        for item in data:
            writer.writerow(item)
    return True

INPATH  = sys.argv[1]
OUTPATH = sys.argv[2]

data = read_from_json(INPATH)

fields = [f for f in data[0]]
for field in fields:
    if all([r[field] == None for r in data]):
        print('Removing {}'.format(field.upper()))
        for row in data:
            del row[field]

# write_csv(OUTPATH, data)

url_data = []
with open(OUTPATH, 'w') as outhandle:
    for n, row in enumerate(data, 1):
        print('Checking URL #{}'.format(n), end='\r')
        if row['official_url'] is not None:
            id = str(row['eprintid'])
            url = row['official_url']
            try:
                response = str(
                    requests.head(row['official_url'], timeout=1).status_code
                    )    
            except:
                response = 'error'
            outhandle.write('\t'.join([id, response, url]) + '\n')
            outhandle.flush()
