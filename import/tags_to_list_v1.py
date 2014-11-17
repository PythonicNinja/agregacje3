# -*- coding: utf-8 -*-
# CREATED ON DATE: 13.11.14


__author__ = 'vojtek.nowak@gmail.com'

from gevent import monkey
import gevent
from gevent.pool import Group


monkey.patch_all()

from pymongo import MongoClient


client = MongoClient()
db = client.test
collection = db.Train


def old_new(old_document):
    try:
        tags_list = old_document.get('Tags').split()
        old_document.update({'Tags': tags_list})
        result = collection.update({'_id': old_document.get('_id')}, old_document)
    except:
        pass


cursor = collection.find()

g1 = Group()

TASKS = 1000

for i, old_document in enumerate(cursor):


    work = gevent.spawn(old_new, old_document)
    g1.add(work)

    if i % TASKS == 0:
        print i
        g1.join()

g1.join()
print('work done')
