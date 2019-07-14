# -*- coding: utf-8 -*-
import csv as csv_lib
import json
from os import path, environ

BASE_DIR = path.dirname(path.abspath(__file__))
DEBUG = environ.get('PY_ENV')
DOCKER = environ.get('DOCKER')


class CSV:
    def __init__(self, file_path):
        self.file_path = file_path

    def read(self, drop_header=True):
        with open(self.file_path, mode='rU') as infile:
            table = csv_lib.reader(infile)
            if drop_header:
                next(table, None)
            return [[rows[i] for i in range(len(rows))] for rows in table]

    def write(self, obj_to_write, to_json=False):
        if to_json:
            with open(self.file_path + '.json', 'w') as fp:
                json.dump(obj_to_write, fp)
        else:
            if type(obj_to_write) is dict:
                flatten = []
                for customer, data in obj_to_write.items():
                    for order_id, barcodes in data.items():
                        flatten.append([customer, order_id, barcodes])
                obj_to_write = flatten

            with open(self.file_path + '.csv', 'w') as outfile:
                # TODO: Get rid of the escape char from the barcode list
                wr = csv_lib.writer(outfile, quoting=csv_lib.QUOTE_NONE, delimiter=',', escapechar='\\')

                if type(obj_to_write) is dict:
                    [wr.writerow([key, val]) for key, val in obj_to_write.items()]
                else:
                    for row in obj_to_write:
                        wr.writerow(row)
        return '{}.{} has been generated'.format(self.file_path, 'json' if to_json else 'csv')
