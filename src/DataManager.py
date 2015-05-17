import FileManager as FM
import Load Manager as LM

def start():
	series = FM.dirContent()
	newEpisodes = LM.checkForNew(series)
	if newEpisodes:
		import StoreManager as SM
		for ser in newEpisodes:
			SM.newSeries(ser, newEpisodes[ser])
			