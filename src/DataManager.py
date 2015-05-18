import FileManager as FM
import DBManager as DB
from re import sub

def start():
	series = DB.dirContent()
	reqSer = []
	reqEp = {}
	for ser in series:
		res = selectWhere('series','seriesname',sub('[_\.]',' ',ser),'seriesid')
		if not :
			reqSer.append(ser)
		else:
			reqEp[ser] = []
			for ep in series[ser]:
				ep['id'] = res[0]
				if not executeSelectQuery('select * from episode where \
					seasonnumber=\'{season}\' and episodenumber=\
					\'{episode}\' and seriesid=\'{id}\''.format(**ep))
					reqEp[ser].append(ep)
	if reqSer != [] or reqEp != []:
		import StoreManager as SM
		for ser in reqSer:
			DB.newSeries(ser,series[ser])
		DB.newEpisode(reqEp)