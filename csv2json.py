#!/usr/bin/env python

import csv
import json
import os
import re
import sys

cast = {
    'string': str,
    'int': int,
    'boolean': (lambda x: x.lower() == 'true')
}


def camel2snake(s):
    if isinstance(s, list): return [camel2snake(sub) for sub in s]
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def read_csv(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        rows = csv.reader(f)

        line = 0
        data = []

        cols = []
        subkey = None
        types = []

        for r in rows:
            line += 1

            if line == 1:
                cols = camel2snake(r)
                continue

            if line == 2:
                types = [el.lower() for el in r]
                continue

            if len(cols) != len(r):
                print('Bad line in file ', filepath, '. Ignored line:', line)
                continue

            d = {}
            if r[0] == '':
                d = data.pop()

            if not d:
                subkey = 0
            if d:
                subkey += 1

            for i in range(len(cols)):
                if r[i] == '': continue

                key = cols[i]
                value = cast[types[i]](r[i])

                if key not in d:
                    d[key] = value
                elif isinstance(d[key], dict):
                    d[key][subkey] = value
                else:
                    aux = d[key]
                    d[key] = {}
                    d[key][subkey - 1] = aux
                    d[key][subkey] = value

            data.append(d)

    return data


def csv2json(csv_path, ensure_ascii=False):
    data = read_csv(csv_path)

    if len(data) <= 0:
        print('Empty file: ', csv_path)
        return

    csv_path = csv_path.split('/')
    if len(csv_path) > 1:
        csv_path.pop(0)

    newpath = os.path.join('json/', '/'.join(csv_path))
    newpath = os.path.splitext(newpath)[0] + '.json'
    os.makedirs(os.path.dirname(newpath), exist_ok=True)

    with open(newpath, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=ensure_ascii)


if __name__ == '__main__':
    indir = sys.argv[1]

    if not indir:
        print('You must add a filename or directory')
        quit()

    if os.path.isfile(indir):
        if os.path.splitext(indir)[1] != '.csv':
            print('The file have to be csv')
        else:
            csv2json(indir)
        quit()

    for path, _, filenames in os.walk(indir):
        for filename in filenames:
            if os.path.splitext(filename)[1] != '.csv':
                continue
            csv2json(os.path.join(path, filename))
