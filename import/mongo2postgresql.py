# -*- coding: utf-8 -*-
# CREATED ON DATE: 17.11.14
__author__ = 'vojtek.nowak@gmail.com'

import psycopg2
import psycopg2.extras

from gevent import monkey
import gevent
from gevent.pool import Group


monkey.patch_all()

from pymongo import MongoClient
mongo_db = MongoClient().test



connection = psycopg2.connect(  # Connect to PostgreSQL Database.
                        host='localhost',
                        database='Train',
                        user='vojtek.nowak',
                        password=''
)
cursor = connection.cursor()

psycopg2.extras.register_hstore(connection)  # This is what forces psycopg2 to interface Dicts with hstores.

'''
{
	"_id" : ObjectId("54654632ab50c94d02bcb81a"),
	"Title" : "How to check if an uploaded file is an image without mime type?",
	"Body" : "<p>I'd like to check if an uploaded file is an image file (e.g png, jpg, jpeg, gif, bmp) or another file. The problem is that I'm using Uploadify to upload the files, which changes the mime type and gives a 'text/octal' or something as the mime type, no matter which file type you upload.</p>  <p>Is there a way to check if the uploaded file is an image apart from checking the file extension using PHP?</p> ",
	"Tags" : [
		"php",
		"image-processing",
		"file-upload",
		"upload",
		"mime-types"
	],
	"Id" : 1
}


CREATE TABLE train (
    Id int,
    Title text,
    Body text,
    Tags text[],
);

'''

def insert_train(train):
    try:
        if isinstance(train.get('Tags'), list):
            cursor.execute("INSERT INTO train (Id, Title, Body, Tags) VALUES (%s, %s, %s, %s)", (
                train.get('Id'),
                train.get('Title'),
                train.get('Body'),
                train.get('Tags')
            ))
            connection.commit()
    except Exception as e:
        print e

g1 = Group()
TASKS = 1000

for i, train in enumerate(mongo_db.Train.find()):
    work = gevent.spawn(insert_train, train)
    g1.add(work)

    if i % TASKS == 0:
        print i
        g1.join()

g1.join()
print('work done')
