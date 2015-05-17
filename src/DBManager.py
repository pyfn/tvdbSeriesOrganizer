import sqlite3
from configs import PATH
from os.path import isfile as os_isfile, join as os_join, isdir as os_isdir
from os import mkdirs as os_mkdirs
from __future__ import print_function

_PIC_PATH = os_join(PATH, 'banners')
if not os_isdir(_PIC_PATH):
	os_mkdirs(_PIC_PATH)
_DB_PATH = os_join(PATH, 'series.db')
_TABLE_NAMES = {
	'series':{
		'query':'create table series (seriesid integer primary key' + 
			', firstaired text, imdb_id text, overview text, language text,' + 
			' rating real, ratingcount integer, runtime real, banner text,' + 
			' poster text, seriesname text, status text)'
		,'attributes':['seriesid','firstaired','imdb_id','overview'
			,'language','rating','ratingcount','runtime'
			,'banner','poster','seriesname','status']},
	'episode':{
		'query':'create table episode ( episodeid integer primary key,' +
			'seriesid integer, seasonid integer, episodeoverview text,' +
			' director text, episodename text, episodenumber integer,' +
			' firstaired text, seasonnumber integer, rating real,' + 
			' ratingcount integer, writer text, filename text)'
		,'attributes':['episodeid','seriesid','seasonid'
			,'episodeoverview','director','episodename'
			,'episodenumber','firstaired','seasonnumber'
			,'rating','ratingcount','writer','filename']},
	'genre':{
		'query':'create table genre ( ' + 
			'genreid integer primary key autoincrement, tag text unique)'
		,'attributes':['genreid','tag']},
	'genre_relation':{
		'query':'create table genre_relation (seriesid integer, genreid integer)'
		,'attributes':['seriesid','genreid']},
	'actor':{
		'query':'create table actor (actorid integer primary key' + 
			', image text, name text)'
		,'attributes':['actorid','image','name']},
	'acts':{
		'query':'create table acts (seriesid integer' + 
			', role text, actorid text, sortorder integer)'
		,'attributes':['seriesid','role','actorid','sortorder']}
}
_INSERT_Q = 'insert into {table} ({query})'


if not os_isfile(_DB_PATH):
	try:
		db = sqlite3.connect()
		c = db.cursor()
		for key in _TABLE_NAMES:
			c.execute(_TABLE_NAMES[key]['query']
		db.commit()
	except sqlite3.DatabaseError as e:
		print(str(e))
	finally:
		db.close()

def storeData(table, data):
	try:
		db = sqlite3.connect()
		c = db.cursor()
		c.execute(_INSERT_Q.format(table=table
			,query=','.join(
			['\'{'+i+'}\'' for i in _TABLE_NAMES[table]['attributes']]).format(
			**data)))
		db.commit()
	except sqlite3.DatabaseError as e:
		print(str(e))
	finally:
		db.close()

def selectWhere(table, col, val, returnValue='*'):
	result = []
	try:
		db = sqlite3.connect()
		c = db.cursor()
		result = c.execute('select {returnValue} from {table} where {col}=\'{val}\''.format(
			table=table,col=col,val=val,returnValue=returnValue)).fetchall()
		db.commit()
	except sqlite3.DatabaseError as e:
		print(str(e))
	finally:
		db.close()
	return result
	
def storeBanner(name, filedata):
	with open(os_join(_PIC_PATH,name), 'w') as pic:
		pic.write(filedata)
	return os_join(_PIC_PATH,name)