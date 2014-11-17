# -*- coding: utf-8 -*-
# CREATED ON DATE: 13.11.14
__author__ = 'vojtek.nowak@gmail.com'
import json
from collections import defaultdict

# pip install motor
# Motor, the non-blocking python driver for monogdb
import motor

from tornado.ioloop import IOLoop
from tornado import gen


client = motor.MotorClient('mongodb://localhost:27017')
db = client['test']
collection = db['Train']

tag_dict = defaultdict(int)

@gen.coroutine
def tags2list():
    cursor = collection.find().skip(12).limit(1)
    while (yield cursor.fetch_next):
        old_document = cursor.next_object()
        try:
            tags_list = old_document.get('Tags').split()
            for tag in tags_list:
                tag_dict[tag] += 1
            old_document.update({'Tags': tags_list})
            result = yield collection.update({'_id': old_document.get('_id')}, old_document)
        except:
            pass

IOLoop.current().run_sync(tags2list)

print('All tags', sum(tag_dict.values()))
print('All distinct', len(tag_dict))

# For further analysis
# Tag - occurance
with open('tag_dict.txt', 'w') as outfile:
    json.dump(tag_dict, outfile)