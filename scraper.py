#!/usr/bin/env python3

import requests
import csv

URI_PATTERN = ''' http://health-equity.lib.umd.edu/cgi/export/{0}/DC/minorityhealth-archive-{0}.txt'''

class DublinCore:
    def __init__(self, uri):
        response = requests.get(uri)
        self.body = response.text

    def parse_response_body(self):
        lines = self.body.split('\n')
        for line in lines:
            if line == '':
                continue
            (key, value) = tuple(line.split(': ', 1))
            if hasattr(self, key):
                current = getattr(self, key)
                if type(current) is list:
                    newval = current.append(value)
                else:
                    newval = [current, value]
                setattr(self, key, newval)
            else:
                setattr(self, key, value)
        
for x in range(1000, 1050):
    uri = URI_PATTERN.format(x)
    response = requests.head(uri)
    if response.status_code == 200:
        dc_metadata = DublinCore(uri)
        dc_metadata.parse_response_body()
        for k, v in dc_metadata.__dict__.items():
            if k == 'body':
                continue
            else:
                print(k, v)


#eprint = Eprint(URI)
#print(eprint.body)
