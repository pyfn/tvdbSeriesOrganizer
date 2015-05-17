from urllib2 import urlopen
from bs4 import BeautifulSoup as BS
from configs import API_KEY
from re import sub as re_sub

_URL = 'http://thetvdb.com/'
_SERIES_BY_NAME = _URL + 'api/GetSeries.php?seriesname={}'
_SERIES_ALL = _URL + 'api/' + API_KEY + 
	'/series/{series_id}/all/{language}.{format}'
_ACTORS = _URL + 'api/' + API_KEY + 
	'/series/{series_id}/actors.xml'
_BANNERS = _URL + 'banners/{}'
def _getSeriesID(name):
	"""
	_getSeriesID(String) -> String
	
	returns the Series ID for the series name
	"""
	results = BS(urlopen(_SERIES_BY_NAME.format(name)).read())
	for series in results.findAll('Series'):
		if series.seriesname.text.lower() == name.lower():
			return series.seriesid.text
	return None
	
def getBanner(url):
	"""
	getBanner(String) -> filedata
	
	returns a Picture file.
	"""
	return urlopen(_BANNERS.format(url)).read()
 
def getSeries(name='',id='',language='en',format='xml'):
	"""
	getSeries(String,String,String,String) -> Dict
	
	returns a complete Dictionary with Series
		- information and Episode Info
	"""
	if name != '':
		id = _getSeriesID(name)
	result = BS(urlopen(_SERIES_ALL.format(series_id=id
		,language=language
		,format=format)).read())
	series = {}
	episodes = []
	for attr in result.series.findAll():
		if str(attr.name) == 'id':
			series['seriesid'] = attr.text
		elif str(attr.name) == 'seriesid':
			continue
		else:
			series[str(attr.name)] = attr.text
	for ep in result.findAll('episode'):
		episode = {}
		for attr in ep.findAll():
			if str(attr.name) == 'id':
				series['episodeid'] = attr.text
			elif str(attr.name) == 'overview':
				series['episodeoverview'] = attr.text
			else:
				series[str(attr.name)] = attr.text
		episodes.append(episode)
	return {'series':series,'episodes':episodes}
	

def getActors(name='',id=''):
	"""
	getActors(String,String) -> [Dict]
	
	returns a Dictionary with Actor information.
	"""
	if name != '':
		id = _getSeriesID(name)
	result =  BS(urlopen(_ACTORS.format(series_id=id)).read())
	actors = []
	for act in result.findAll('actor'):
		actor = {}
		for attr in act.findAll():
			if str(attr.name) == 'id':
				series['actorid'] = attr.text
			else:
				series[str(attr.name)] = attr.text
		actors.append(actor)
	return actors