# Wojciech Nowak 
* nr albumu 206354 Informatyka I rok Magisterskie

####Sprzęt:
* procesor: 

		Model:								  Intel Core i7-4650U
		Szybkość procesora:					1,7 GHz  
		Łączna liczba rdzeni:					2    
		Pamięć podręczna L2 (na rdzeń): 	  256KB    
		Pamięć podręczna L3: 				 4MB
		
* pamięć ram:

		Rozmiar: 		8GB 
		Typ:			DDR3
		Prędkość:	   1600MHz

* dysk: 

		model: 			SSD Samsung sm0256f 
		magistrala:		PCIe SSD
		
####Wersje oprogramowania:
* MongoDB shell version: 	2.8.0-rc0
* Postgresql version: 		9.3.5
* OS: Mac OS X 				10.10 (14A389)


#Zadania

###Zadanie 1a 
Polega na zaimportowaniu, do systemów baz danych uruchomionych na swoim komputerze, danych z pliku Train.csv bazy:

*	MongoDB

komenda:

	>> time mongoimport --type csv -c Train --file Desktop/Train.csv --headerline

jednak:

	>>db.Train.findOne()

	{
		"_id" : ObjectId("5463ddb4ab50c94d02a24f07"),
		"Id" : "<p>Is there a way to check if the uploaded file is an image apart from checking the file extension using PHP?</p>"
	}
	
po krótkiej analizie co jest problemem, dochodzimy do wniosku, że należy usunąć "\n"

	>> time cat Train.csv | tr "\n" " " | tr "\r" "\n" > Train_prepared_for_mongoimport.csv
	real	19m42.573s
	user	37m9.401s
	sys		0m38.146s
	
możemy na nowo wywołać import 2.6
	
	>>time mongoimport --type csv -c Train --file Train_prepared_for_mongoimport.csv --headerline
	connected to: 127.0.0.1
	2014-11-13T01:27:39.002+0100 		Progress: 44715137/7253917400     0%
	...
	2014-11-13T01:35:26.016+0100 		Progress: 7212784202/7253917400	99%
	2014-11-13T01:35:26.016+0100 			6000000  12765/second
	2014-11-13T01:35:28.844+0100 check 9 6034197
	2014-11-13T01:35:28.898+0100 imported 6034196 objects

	real	7m52.488s
	user	2m25.171s
	sys	0m26.896s
	
możemy na nowo wywołać import 2.8.0-rc0
	
	>>time mongoimport --type csv -c Train --file Train_prepared_for_mongoimport.csv --headerline
	2014-11-17T01:45:04.590+0100	imported 6034196 documents

	real	6m49.952s
	user	6m16.081s
	sys	0m53.392s

*	PostgreSQL

najpierw użyjemy exportu z mongo do json'a

	>> time mongoexport --db test --collection Train --out train.json --journal
	2014-11-17T00:14:50.951+0100	exported 6034196 records

	real	5m46.904s
	user	2m55.293s
	sys		0m36.245s
	
tworzymy bazę

	>> createdb Train

włączamy hstora

	>> psql Train	
	
	>> CREATE EXTENSION hstore;

tworzymy tabele

	CREATE TABLE train (
    	Id int,
	    Title text,
    	Body text,
	    Tags text[],
	);

import w pythonie z mongodb -> postgresa:
	
	>> time python mongo2postgres.py
	real	68m41.412s
	user	10m26.866s
	sys	6m58.740s	


###Zadanie 1b
Zliczyć liczbę zaimportowanych rekordów (Odpowiedź: powinno ich być 6_034_195).
	
	>> mongo
	> db.Train.count()
	6034196
	
####Zadanie 1c
Zamiana formatu danych.) Zamienić string zawierający tagi na tablicę napisów z tagami następnie zliczyć wszystkie tagi i wszystkie różne tagi.
	
	>>time python3 tags_to_list_v0.py 
	All tags 17407667
	All distinct 42048

	real    71m5.795s
	user    47m8.053s
	sys     3m53.134s
	
Uznałem, że da się dużo lepiej używając greenletów:

	>> time python tags_to_list_v1.py 
	real    32m16.310s
	user    9m25.584s
	sys     0m57.192s


####Zadanie 1d
Zadanie 1d. Wyszukać w sieci dane zawierające obiekty GeoJSON. Następnie dane zapisać w bazie MongoDB.

Szukając danych geojson, natrafiłem na bazę punktów poi. Postanowiłem zanalizować rejestratory w polsce.
[link do pliku](http://www.poiplaza.com/download/zipfiles/1424/PL-FixSpeedcam_mio_moov.zip)

	
przykładowy rekord:

	52.64373, 19.19789, 50@ PL-Modzerowo Fix Speedcam
	
musimy przygotowac do importu do mongodb

1. usunąć polskie znaki

		>> iconv -f utf8 -t utf8 -c PL-speedcam.csv > PL-speedcam_ASCII.csv
	
2. usunąć " ", "@", "PL-", "Fix Speedcam", nazwę miasta oraz podzielić przecinkami

		>> cat PL-speedcam_ASCII.csv | cut -d "@" -f1 > PL-speedcam_toImport.csv

3. import do mongodb

		>>time mongoimport --type csv -c speedcam --file PL-speedcam_toImport.csv --fields lon,lat,speed
		2014-11-17T04:29:26.515+0100	connected to: localhost
		2014-11-17T04:29:26.589+0100	imported 2538 documents

		real	0m0.106s
		user	0m0.034s
		sys	0m0.018s
		
4. przykładoy wpis:

		>>db.speedcam.findOne()
		{
			"_id" : ObjectId("54696b964fa64c9a2a9113fe"),
			"lon" : 52.88185,
			"lat" : 21.32492,
			"speed" : 50
		}
		
5. musimy przemienić go na geojson'a
	

```python
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
```
	
	>> python csv2geojson.py


6. import do mongodb
	
		>>time mongoimport --type json -c speedcam --file speedcamGeo.json
		2014-11-17T04:53:24.583+0100	connected to: localhost
		2014-11-17T04:53:24.615+0100	imported 2538 documents

		real	0m0.042s
		user	0m0.033s
		sys	0m0.008s
		

AGREGACJE GEOJSON:

1. Fotoradary w okolicy 20 km od Gdańska
	
	>> db.speedcam.find({loc: {$near: {$geometry: {type: "Point", coordinates: [54.349683, 18.643335]}, $maxDistance: 20000}}})
	
	
	






