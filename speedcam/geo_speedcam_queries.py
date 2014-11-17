# -*- coding: utf-8 -*-
# CREATED ON DATE: 17.11.14
__author__ = 'vojtek.nowak@gmail.com'

import json
from pymongo import MongoClient

client = MongoClient()
db = client.test


def to_geo_json_points(cursor, json_name, type="Point"):
    geo_json = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry":
                    {
                        "_id": str(point.get('speed')) + " " + str(point.get('loc')),
                        "type": type,
                        "coordinates": [point.get('loc')[1], point.get('loc')[0]]
                    }
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


# speedcams in pomorskie
to_geo_json_points(
    cursor=db.speedcam.find({
        'loc': {
            '$geoIntersects': {
                '$geometry': {
                    'type': "Polygon",
                    'coordinates': [
                        [
                            [54.570489, 16.702425],
                            [54.950828, 19.201752],
                            [53.611260, 19.310739],
                            [53.611260, 16.893747],
                            [54.570489, 16.702425]
                        ]
                    ]
                }
            }
        }
    }),
    json_name='speed_cams_pomorskie.geojson')


# speedcams route
to_geo_json_points(
    cursor=db.speedcam.find({
        'loc': {'$geoIntersects':
                    {'$geometry':
                         {
                             'type': "LineString",
                             'coordinates': [
                                 [52.64373, 19.19789],
                                 [51.17473, 19.46548]
                             ]
                         }
                    }
        }
    }),
    json_name='speed_cams_route.geojson',
    type="Line"
)
