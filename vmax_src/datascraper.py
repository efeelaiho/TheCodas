import wikipedia
import spotipy
from bs4 import BeautifulSoup
import re
import requests
import lxml
import mwparserfromhell
import simplejson
import urllib3
import json

spotify = spotipy.Spotify()
cache = []
index = 0

with open('artistlist') as f:
	for line in f:
		#if (' ' in line):
		#	artistname = ' '.join(line[1:])
		#	print (artistname)
		#else:
		artdict = {}

		#model
		artdict["model"] = "volumemax.artist"

		#pk
		artdict["pk"] = index
		
		#fields
		artdict["fields"] = {}
		
		#full_name
		artistname = line
		results = spotify.search(q='artist:' + artistname, type='artist')
		items = results['artists']['items']
		if len(items) > 0:
			artist = items[0]
		artdict["fields"]["full_name"] = artist['name']

		#origin
		undscore = re.sub(" ",'_',artist['name'])
		url1 = "https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&rvsection=0&titles="
		format = "&format=json"
		url = url1+undscore+format
		res = requests.get(url)
		text = res.json()["query"]["pages"].values()[0]["revisions"][0]["*"]
		wiki = mwparserfromhell.parse(text)
		templates = wiki.filter_templates(matches="birth_place")
		if 0 < len(templates):
			template = templates[0]
			origin = template.get("birth_place").value
			origin = re.sub(r'\[\[(?:[^\]|]*\|)?([^\]|]*)\]\]', r'\1',str(origin))
		else: 
				templates = wiki.filter_templates(matches="origin")
				if 0 < len(templates):
					template = templates[0]
					try:
						origin = template.get("origin").value
						origin = re.sub(r'\[\[(?:[^\]|]*\|)?([^\]|]*)\]\]', r'\1',str(origin))
					except ValueError:
						origin = 'N/A'
				else:
					origin = 'N/A'
		artdict["fields"]["origin"] = origin

		#popularity
		artdict["fields"]["popularity"] = artist['popularity']

		#genre
		if 0 < len(artist['genres']):
			artdict["fields"]["genre"] = artist['genres'][0]
		else:
			artdict["fields"]["genre"] = 'N/A'

		#uri
		artdict["fields"]["genre"] = artist['uri']

		#biography
		try:
			artdict["fields"]["biography"] = wikipedia.summary(artist['name'])
		except wikipedia.exceptions.DisambiguationError:
			artdict["fields"]["biography"] = 'N/A'

		#youtube_url_1
		#youtube_url_2

		#recommended_album
		artdict["fields"]["recommended_album"] = index
		index+=1

		#img
		searchformat = re.sub(" ",'%20',artist['name'])
		spotstring = "spotify%20"
		url2 = "https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q="
		url = url2+spotstring+searchformat
		res = requests.get(url)
		text = res.json()["responseData"]["results"][0]["url"]
		artdict["fields"]["image_url"] = text
		cache.append(artdict)
		# wiki = mwparserfromhell.parse(text)
		# templates = wiki.filter_templates(matches="results")
		# print (templates)
		# if 0 < len(templates):
		# 	template = templates[0]
		# 	origin = template.get("birth_place").value
		# 	origin = re.sub(r'\[\[(?:[^\]|]*\|)?([^\]|]*)\]\]', r'\1',str(origin))
		# else: 
		# 		templates = wiki.filter_templates(matches="origin")
		# 		template = templates[0]
		# 		if 0 < len(templates):
		# 			origin = template.get("origin").value
		# 			origin = re.sub(r'\[\[(?:[^\]|]*\|)?([^\]|]*)\]\]', r'\1',str(origin))
		# 		else:
		# 			origin = 'N/A'
		# print(origin)
print json.dumps(cache, indent=4)
#jsonfile = open("finalcache.json", "w")
#jsonfile.write(simplejson.dumps.loads(cache), indent=4, sort_keys=True)
#jsonfile.close()