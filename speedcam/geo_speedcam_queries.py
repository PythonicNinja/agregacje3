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

# 1. speedcams near 20 km from Gdansk
to_geo_json_points(
    cursor=db.speedcam.find({
        'loc': {
            '$near': {'$geometry': {'type': "Point", 'coordinates': [54.349683, 18.643335]}, '$maxDistance': 20000}}}),
    json_name='speed_cams_near_gdansk.geojson')


# 2. speedcams in pomorskie
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


# 3. speedcams route
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
    json_name='speed_cams_route.geojson')


# 4. speedcams near Warsaw but not in warsaw center 4km < center < 20km
to_geo_json_points(
    cursor=db.speedcam.find({
        'loc': {
            '$near': {'$geometry': {'type': "Point", 'coordinates': [52.232728, 21.010382]}, '$maxDistance': 20000, '$minDistance': 4000}}}),
    json_name='speed_cams_around_center_of_warsaw.geojson')


# 5. speedcams 15 around polish seaside
to_geo_json_points(
    cursor=db.speedcam.find({
        'loc': {
            '$near': {
                '$geometry': {
                    'type': "Point",
                    'coordinates': [55.634283, 15.403922]
                }
            }
        }
    }).limit(15),
    json_name='speed_cams_near_seaside.geojson')


# 6. speedcams around pomorskie
to_geo_json_points(
    cursor=db.speedcam.find({
        'loc': {
            '$geoWithin': {
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
    json_name='speed_cams_around_pomorskie.geojson')


# 7. speedcams near Karkow < 100
to_geo_json_points(
    cursor=db.speedcam.find({
        'loc': {
            '$near': {'$geometry': {'type': "Point", 'coordinates': [50.059441, 19.940328]}}}}).limit(100),
    json_name='speed_cams_around_krakow.geojson')


# 8. speedcams all in poland
to_geo_json_points(
    cursor=db.speedcam.find(),
    json_name='speed_cams_poland.geojson')