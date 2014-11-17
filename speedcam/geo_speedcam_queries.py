# -*- coding: utf-8 -*-
# CREATED ON DATE: 17.11.14
__author__ = 'vojtek.nowak@gmail.com'

import json
from pymongo import MongoClient

client = MongoClient()
db = client.test


def to_geo_json_points(cursor, json_name):
    geo_json = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry":
                    {
                        "_id": str(point.get('speed')) + " " + str(point.get('loc')),
                        "type": "Point",
                        "coordinates": point.get('loc')
                    },
                "properties": {"prop0": "value0"}
            } for point in cursor
        ]
    }

    with open(json_name, 'w') as out_json:
        json.dump(geo_json, out_json)

# speedcams near 20 km from Gdansk
to_geo_json_points(
    cursor=db.speedcam.find({
        'loc': {
            '$near': {'$geometry': {'type': "Point", 'coordinates': [54.349683, 18.643335]}, '$maxDistance': 20000}}}),
    json_name='speed_cams_near_gdansk.geojson')

