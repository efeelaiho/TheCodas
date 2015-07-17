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
		artdict = {}

		#pk
		artdict["pk"] = index

		#model
		artdict["model"] = "volumemax.artist"
		
		#fields
		artdict["fields"] = {}
		
		#full_name
		artistname = line
		results = spotify.search(q='artist:' + artistname, type='artist')
		items = results['artists']['items']
		if len(items) > 0:
			artist = items[0]
			artdict["fields"]["full_name"] = artist['name']
		else:
			artdict["fields"]["full_name"] = "N/A"

		#origin
		try:
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
		except KeyError:
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
		artdict["fields"]["spotify_artist_uri"] = artist['uri']

		#biography
		try:
			artdict["fields"]["biography"] = wikipedia.summary(artist['name'])
		except wikipedia.exceptions.DisambiguationError:
			artdict["fields"]["biography"] = 'N/A'

		#youtube_url_1
		artdict["fields"]["youtube_url_1"] = "ADD FROM YOUTUBE"

		#youtube_url_2
		artdict["fields"]["youtube_url_2"] = "ADD FROM YOUTUBE"


		#recommended_album
		results = spotify.artist_albums(artist['uri'], album_type='album')
		albums = results['items']
		if 0 < len(albums):
			artdict["fields"]["recommended_album"] = albums[0]['uri']
		else:
			artdict["fields"]["recommended_album"] = "N/A"

		#img
		searchformat = re.sub(" ",'%20',artist['name'])
		spotstring = "spotify%20"
		url2 = "https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q="
		url = url2+spotstring+searchformat
		res = requests.get(url)
		text = "https://pixabay.com/static/uploads/photo/2013/07/12/17/14/cd-rom-151860_640.png"
		for i in range (0,4):
			if res.json()["responseData"]["results"][i]["width"] == "640" and res.json()["responseData"]["results"][i]["height"] == "640":
				text = res.json()["responseData"]["results"][i]["url"]
				break
		artdict["fields"]["image_url"] = text
		cache.append(artdict)

index = 0

with open('albumlist') as f:
	for line in f:
		albdict = {}

		#model
		albdict["model"] = "volumemax.album"

		albumname = line
		results = spotify.search(q='album:' + albumname, type='album')
		items = results['albums']['items']
		if len(items) > 0:
			album = items[0]
		albumbyuri = spotify.album(album['uri'])
		#pk
		albdict["pk"] = index
		
		#fields
		albdict["fields"] = {}
		
		#album_artist
		albdict["fields"]["album_artist"] =  albumbyuri['artists'][0]['uri']

		#release_date
		albdict["fields"]["release_date"] = albumbyuri['release_date']


		#genre
		if 0 < len(albumbyuri['genres']):
			albdict["fields"]["genre"] = albumbyuri['genres'][0]
		else:
			albdict["fields"]["genre"] = 'N/A'

		#album_name
		albdict["fields"]["album_name"] = album['name']

		#editors_notes
		albdict["fields"]["editors_notes"] = "ADD FROM ITUNES"

		#uri
		albdict["fields"]["spotify_albums_uri"] = album['uri']

		#image_url
		if 0 < len(album['images']): 
			albdict["fields"]["image_url"] = album['images'][0]['url']
		else:
			albdict["fields"]['image_url'] = 'N/A'
		
		cache.append(albdict)
print json.dumps(cache, indent=4)