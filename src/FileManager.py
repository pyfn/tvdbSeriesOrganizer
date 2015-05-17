from os import walk
from os.path import split, join
from configs import PATH
import re

FILE_ENDINGS = ['.avi','.mp4','.wmv','.rar'
	, '.mpg', '.mp2', '.mpeg', '.mpe', '.mpv']

def _findFiles(path):
	for root,dir,files in walk(path):
		for name in files:
			for end in FILE_ENDINGS:
				if name.endswith(end):
					yield root,dir,name

def _extractSE(name):
	m = re.search('^.*?S(\d+)E(\d+).*',name,re.I)
	if m != None:
		return int(m.group(1)),int(m.group(2))
	m = re.search('^.*?(\d+)x(\d+).*',name,re.I)
	if m != None:
		return int(m.group(1)),int(m.group(2))
	m = re.search('^.*?(\d{3,}).*')
	if m != None:
		try:
			s, e = m.group(1)[0:-2], m.group(1)[-2:]
			return int(s), int(e)
		except IndexError:
			pass
	return '', ''
	
def dirContent():
	series = {}
	for root, dir, name in _findFiles(PATH):
		r, h = split(root)
		while PATH != r:
			r, h = split(r)
		s, e = _extractSE(name)
		if h not in series:
			series[h] = []
		series[h].append({'season':s,'episode':e,'path':join(root,name)})
	return series