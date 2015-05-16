import sqlite3
from configs import PATH
from os.path import isfile as os_isfile, join as os_join, isdir as os_isdir
from os import mkdirs as os_mkdirs

_PIC_PATH = os_join(PATH, 'banners')
if not os_isdir(_PIC_PATH):
	os_mkdirs(_PIC_PATH)
_DB_PATH = os_join(PATH, 'series.db')
_TABLE_NAMES = {
	'series':'',
	'episode':'',
	'genre':'',
	'genre_relation':'',
	'actor':'',
	'acts':''
}

connection = sqlite3.connect(_DB_PATH)
cursor = connection.cursor()
try:
	for name in _TABLE_NAMES:
		colList = cursor.execute('PRAGMA table_info(series)').fetchall()
		if colList != []:
			queryLst = []
			for col in colList:
				queryLst.append('{' + str(col[1]) + '}')
			_TABLE_NAMES[name] = ', '.join(queryLst)
except Exception as e:
	print str(e)
finally:
	connection.close()

def storeBanner(filedata, filename):
	"""
	storeBanner(BYTECODE, String) -> String
	
	stores a Picture and returns the full path.
	"""
	with open(os_join(_PIC_PATH, filename), 'w') as pic:
		pic.write(filedata)
	return os_join(_PIC_PATH, filename)
	
def createTable(name, dictionary):
	"""
	createTable(String, Dict)
	
	creates a table out of a dictionary
	"""
	db = sqlite3.connect(_DB_PATH)
	try:
		cursor = db.cursor()
		seriesAttrs = []
		for tag in dictionary:
			seriesAttrs.append('{' + str(tag) + '}')
		cursor.execute('CREATE TABLE {} ({})'.format(
			name, ', '.join(seriesAttrs))
		_TABLE_NAMES[name] = ', '.join(seriesAttrs)
		db.commit()
	except Exception as e:
		print str(e)
	finally:
		db.close()

def checkForAttr(table, column, value, returnValue=''):
	if returnValue == '':
		returnValue = column
	db = sqlite3.connect(_DB_PATH)
	c = db.cursor() #create cursor
	check = c.execute(
			'SELECT {} FROM {} '\
			'WHERE {}=\'{}\''.format(returnValue, table, column, value))
	return check.fetchone()

		
def checkForTable(id):
	db = sqlite3.connect(_DB_PATH)
	c = db.cursor() #create cursor
	check = c.execute(
			'SELECT name FROM sqlite_master '\
			'WHERE type=\'table\' AND name=\'{}\''.format(id))
	if check.fetchone() == None:
		db.close()
		return False
	db.close()
	return True
	
def storeData(data, id):
	"""
	storeData(Dict, String)
	
	stores data to the Database System
	"""
	try:
		if not checkForTable(id):
			createTable(id, data)
		db = sqlite3.connect(_DB_PATH)
		c = db.cursor() #create cursor
		query = 'INSERT INTO series ({})'.format(_TABLE_NAMES[id])
		c.execute(query.format(**data))
		db.commit()
	except Exception as e:
		print str(e)
	finally:
		db.close()

def loadData():
	pass