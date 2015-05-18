import APIManager as API
import DBManager as DB


def newSeries(name, pathDict, epFlag=0):
	"""
	newSeries(String)
	
	downloads the series info and stores it to the DB.
	"""
	seriesWhole = API.getSeries(name=name)
	series = seriesWhole['series']
	episodes = seriesWhole['episodes']
	if not epFlag:
		newGenre(series)
		newActors(series)
		newBanners('banner', series)
		DB.storeData('series', series)
	for episode in episodes:
		for ep in pathDict:
			if (ep['season'] == episode['seasonnumber'] and
				ep['season'] == episode['episodenumber']):
				episode['path'] = ep['path']
		else:
			episode['path'] = 'NULL'
		if episode['path'] != 'NULL' or not epFlag:
			_storeEpisode(episode)

	
def newGenre(series):
	genres = series['genres'].strip('|').split('|')
	for genre in genres:
		DB.storeData('genre',{'tag':genre,'genreid':'NULL'})
		result = DB.selectWhere('genre','tag',genre,genreid)
		if result:
			DB.storeData('genre_relation',{'genreid':result[0][0]
				,'seriesid':series['seriesid']})
	
def newActors(series):
	actors = DB.getActors(id=series['seriesid'])
	actors['seriesid'] = series['seriesid']
	newBanner('image', actors)
	DB.storeData('acts', actors)
	DB.storeData('actor', actor)
	
def _storeEpisode(episode):
	newBanner('filename', episode)
	DB.storeEpisode('episode',episode)

def newBanners(args, dictionary):
	filedata = API.getBanner(dictionary[args])
	path = DB.storeBanner(dictionary[args].split('/')[-1]
		,filedata)
	dictionary[args] = path
	
def newEpisode(episodes):
	for ser in episodes:
		newSeries(ser,episodes[ser],1)