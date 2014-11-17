# -*- coding: utf-8 -*-
# CREATED ON DATE: 17.11.14
__author__ = 'vojtek.nowak@gmail.com'


import csv,json, decimal, codecs

file = open("PL-speedcam_toImport.csv")
reader = csv.reader(file, delimiter=",", quotechar='"')

keys = ['lon', 'lat', 'speed']

with codecs.open("speedcamGeo.json", "w", encoding="utf-8") as out:
    for r in reader:
        line = dict(zip(keys, r))

        out.write(json.dumps({
            'speed': int(line.get('speed')),
            'loc': [float(line.get('lon')), float(line.get('lat'))]
        })+"\n")

file.close()