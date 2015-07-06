import spotipy
import sys
import json


spotify = spotipy.Spotify()
'''
if len(sys.argv) > 1:
    name = ' '.join(sys.argv[1:])
else:
    name = 'Radiohead'
'''

tempartists = ['7dGJo4pcD2V6oG8kP0tJRR', '19eLuQmk9aCobbVDHc6eek', '4jXfFzeP66Zy67HM2mvIIF', '0kbYTNQb4Pb1rPbbaF0pT4', '3fMbdgg4jU18AjLCKBhRSm', '5K4W6rqBFWDnAN6FQUkS6x']


artistcache = {}
'''
imgresults = spotify.search(q='artist:' + name, type='artist')
items = imgresults['artists']['items']
if len(items) > 0:
    artist = items[0]
    '''
for temp in tempartists:
	artist = spotify.artist(temp)
	aid = artist['id']
	artistcache[aid] = {}

	#image scrape
	artistcache[aid]['img'] = artist['images'][0]['url']


	#albums scrape
	albumresults = spotify.artist_albums(artist['id'], album_type='album')
	albums = albumresults['items']
	while albumresults['next']:
		albumresults = spotify.next(albumresults)
		albums.extend(albumresults['items'])
	albumlist = []
	for album in albums:
		albumlist.append(album['name'])
	artistcache[aid]['albums'] = albumlist

	#top tracks scrape
	toptracksresults = spotify.artist_top_tracks(artist['id'])
	toptracks = []
	for track in toptracksresults['tracks'][:3]:
		toptracks.append(track['name'])
	artistcache[aid]['toptracks'] = toptracks

	#json dump
	with open ('artistcache.json', 'w') as fp:
		json.dump(artistcache, fp)