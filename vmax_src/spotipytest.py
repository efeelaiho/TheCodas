import spotipy
import sys
import json
import wikipedia


spotify = spotipy.Spotify()
'''
if len(sys.argv) > 1:
    name = ' '.join(sys.argv[1:])
else:
    name = 'Radiohead'
'''

tempartists = ['7dGJo4pcD2V6oG8kP0tJRR', '4jXfFzeP66Zy67HM2mvIIF', '5K4W6rqBFWDnAN6FQUkS6x',  '3fMbdgg4jU18AjLCKBhRSm', '0kbYTNQb4Pb1rPbbaF0pT4', '19eLuQmk9aCobbVDHc6eek']
artistcache = {}

'''

{	Artist Spotify URI: 
	{
		'name': artist name, 
		'img': artist image url, 
		'albums': 
			{
				album name: album art url,
				...
			}, 
		'bio': Wikipedia summary of artist, 
		'toptracks': 
			[
				top track of artist,
				2nd top track of artist,
				3rd top track of artist
			]
	}
}
'''

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
	artistcache[aid]['name'] = artist['name']
	artistcache[aid]['albums'] = {}

	#image scrape
	artistcache[aid]['img'] = artist['images'][0]['url']


	#albums scrape {album name: album art url}
	albumresults = spotify.artist_albums(artist['id'], album_type='album')
	albums = albumresults['items']
	while albumresults['next']:
		albumresults = spotify.next(albumresults)
		albums.extend(albumresults['items'])
	for album in albums:
		#albumlist.append(album['name'])
		if 0 < len(album['images']): 
			artistcache[aid]['albums'][album['name']] = album['images'][0]['url']
		else:
			artistcache[aid]['albums'][album['name']] = 'N/A'

	#top tracks scrape
	toptracksresults = spotify.artist_top_tracks(artist['id'])
	toptracks = []
	for track in toptracksresults['tracks'][:3]:
		toptracks.append(track['name'])
	artistcache[aid]['toptracks'] = toptracks

	artistcache[aid]['bio'] = wikipedia.summary(artist['name'])

	#json dump
print (artistcache);
with open ('artistcache.json', 'w') as fp:
	json.dump(artistcache, fp)