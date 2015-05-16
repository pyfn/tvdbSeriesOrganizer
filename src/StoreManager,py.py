import APIManager as API
import DBManager as DB


def newSeries(name, pathDict):
	"""
	newSeries(String)
	
	downloads the series info and stores it to the DB.
	"""
	seriesWhole = API.getSeries(name)
	series = seriesWhole['series']
	episodes = seriesWhole['episodes']
	_handleGenre(series)
	del series['genre']
	_handleActors(series)
	del series['actors']
	for episode in episodes:
		seasonNr = episode['seasonnumber']
		if len(seasonNr) == 1:
			seasonNr = '0' + seasonNr
		episodeNr = episode['episodenumber']
		if len(episodeNr) == 1:
			episodeNr = '0' + episodeNr
		path = pathDict.get(seasonNr + episodeNr, default='')
		episode['path'] = path
		_handleEpisodeBanners(episode)
		_handleEpisode(episode)
	_handleSeriesBanners(series)
	DB.storeData(series,'series')
	
def _handleSeriesBanners(series):
	filedata = API.getBanner(series['banner'])
	series['banner'] = DB.storeBanner(
		filedata, series['banner'].split('/')[-1])
	
def _handleEpisodeBanners(episode):
	filedata = API.getBanner(episode['filename'])
	episode['filename'] = DB.storeBanner(
		filedata, episode['filename'].split('/')[-1])
		
def _handleActorBanners(actor):
	filedata = API.getBanner(actor['image'])
	actor['image'] = DB.storeBanner(
		filedata, actor['image'].split('/')[-1])
	
def _handleEpisode(episode):
	DB.storeData(episode,'episode')

def _handleActors(series):
	serid = series['seriesid']
	actors = API.getActors(serid)
	for actor in actors:
		role = actor['role']
		del actor['role']
		_handleActorBanners(actor)
		if not DB.checkForAttr('actor','actorid',actor['actorid']):
			DB.storeData(actor, 'actor')
		DB.storeData(
			{'actorid':actor['actorid'],'seriesid':serid,'role':role},'acts')

def _handleGenre(series):
	genres = series['genre'].strip('|').split('|')
	if not DB.checkForTable('genre'):
		DB.createTable('genre',{'genreid INTEGER PRIMARY KEY':'',
			'genrename':''})
	for genre in genres:
		genreid = DB.checkForAttr('genre','genrename', genre, 'genreid')
		if genreid == None:
			DB.storeData({'genreid':'NULL','genrename':genre},'genre'
			genreid = DB.checkForAttr('genre','genrename', genre, 'genreid')
		DB.storeData('genre_relation',{'genreid':genreid,
			'seriesid':series['seriesid']})

def newEpisode(series, path):
	"""
	newEpisode(String,String,String,String)
	
	Downloads the Episode info and stores it to the Database
	"""
	for ser in series:
		seriesWhole = getSeries(ser)
		for ep in seriesWhole['episodes']:
			if ((ep['seasonnumber'],ep['episodenumber']) in series[ser]):
				episode = ep
				episode['path'] = path
				_handleEpisodeBanners(episode)
				_handleEpisode(episode)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	