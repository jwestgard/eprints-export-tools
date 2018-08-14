#!/usr/bin/env python3

import csv
import os
import requests
import sys

URI_PATTERN = '''http://health-equity.lib.umd.edu/cgi/export/{0}/DC/minorityhealth-archive-{0}.txt'''
OUTPUT_DIR = sys.argv[2]

def fetch_dc_metadata(filepath, uri):
    print('Fetching {0}...'.format(uri))
    response = requests.get(uri)
    body = response.text
    with open(filepath, 'w') as outfile:
        outfile.write(body)

def read_dc_metadata(filepath, uri, id):
    print('Reading {0}...'.format(filepath))
    result = {'id':[str(id)], 'dc_uri':[uri]}
    with open(filepath, 'r') as infile:
        body = infile.read()
        for line in body.split('\n'):
            if line == '':
                continue
            (key, value) = tuple(line.split(': ', 1))
            result.setdefault(key, []).append(value)
    return result

eprints = []
existing_files = [os.path.join(OUTPUT_DIR, f) for f in os.listdir(OUTPUT_DIR)]
print(existing_files)
for id in range(5000):
    print('Processing Eprint id {0}...'.format(id))
    filepath = os.path.join(OUTPUT_DIR, '{0}.txt'.format(id))
    uri = URI_PATTERN.format(id)
    if filepath not in existing_files:
        response = requests.head(uri)
        if response.status_code == 200:
            fetch_dc_metadata(filepath, uri)
        else:
            continue
    eprints.append(read_dc_metadata(filepath, uri, id))
print('\nComplete!')

fieldnames = set().union(*(e.keys() for e in eprints))
with open(sys.argv[1], 'w') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for e in eprints:
        for k,v in e.items():
            e[k] = ' || '.join(v)
        writer.writerow(e)
