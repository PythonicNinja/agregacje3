# -*- coding: utf-8 -*-
# CREATED ON DATE: 17.11.14
__author__ = 'vojtek.nowak@gmail.com'

import json
from pymongo import MongoClient

client = MongoClient()
db = client.test


def to_highcharts(cursor, json_name):
    out_json = {
        'chart': {
            'type': 'bar'
        },
        'title': {
            'text': 'Crime analysis'
        },
        'subtitle': {
            'text': 'Source: http://data.police.uk/data/'
        },
        'xAxis': {
            'categories': [data.get('_id') for data in cursor],
            'title': {
                'text': None
            }
        },
        'yAxis': {
            'min': 0,
            'title': {
                'text': '',
                'align': 'high'
            },
            'labels': {
                'overflow': 'justify'
            }
        },
        'tooltip': {
            'valueSuffix': ' '
        },
        'plotOptions': {
            'bar': {
                'dataLabels': {
                    'enabled': True
                }
            }
        },
        'legend': {
            'layout': 'vertical',
            'align': 'right',
            'verticalAlign': 'top',
            'x': -40,
            'y': 100,
            'floating': True,
            'borderWidth': 1,
            'backgroundColor': '#FFFFFF',
            'shadow': True
        },
        'credits': {
            'enabled': False
        },
        'series': [{
                       'name': 'Data',
                       'data': [data.get('count') for data in cursor]
                   },
        ]
    }

    with open(json_name, 'w') as out_file:
        json.dump(out_json, out_file)

#Uniewinnienia i ich lokalizacje
to_highcharts(
    cursor=db.crime.aggregate([
        { '$match' : { 'Outcome type' : "Offender given absolute discharge" }},
        {
                '$group': {
                    '_id':  "$Location",
                    'count': {'$sum': 1}
                }
        },
        {
            '$sort': {'count': -1}
        },
        {
            '$limit': 10
        }
	    ])['result'],
    json_name='aggregation4.json')