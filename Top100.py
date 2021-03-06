import os

import moviepy.editor as mp

from pytube import YouTube

from requests import get

from string import *

from bs4 import BeautifulSoup as Bsoup


def createUrl(string):

	container = []

	stringUrl = ''

	for names in string:

		for lett in names:
			
			if lett in chars: stringUrl += lett

			elif lett == ' ': stringUrl += '+'

		container.append(stringUrl)

		stringUrl = ''

	return container


path = raw_input('Path:\n')

openFile = lambda mode: open(path + '\\dwd.txt', mode)

try:

		os.chdir(path)

		os.mkdir('mp3')

		os.mkdir('mp4')

except WindowsError: None

try: file = openFile('r')

except IOError:

	file = openFile('w')

	file = openFile('r')

dwded = file.readlines()

board = get('https://www.billboard.com/charts/hot-100').text

boardSoup = Bsoup(board, 'lxml') # html parser

song_artist = {}

url = []

fileTitle = []

stringTitles = []

count = 1

repeat = False

amount = raw_input('Song range:\n').split(': ')

chars = tuple(ascii_letters) + ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')

for titles in boardSoup.findAll('div', {'class': 'chart-row__title'}):

	if count <= int(amount[1]) and count >= int(amount[0]): stringTitles.append(str(titles.get_text()))

	elif count > int(amount[1]): break

	count += 1

for rmv in stringTitles:

	sng_art = rmv.split('\n\n') # song to artist lst

	del sng_art[-1] 

	sng_art[0] = ''.join(list(sng_art[0])[1: ]) # removes beginning '\n'

	song_artist[sng_art[0]] = sng_art[1]

songsURL = createUrl(song_artist.keys())

artistsURL = createUrl(song_artist.values())

for arrange in range(int(amount[1]) + 1 - int(amount[0])): # thats the len of songs and artists

	short = song_artist.values()[arrange] + ' - ' + song_artist.keys()[arrange]

	if (short + '\n') in dwded:

		print '\n' + song_artist.keys()[arrange], 'has already downloaded' + '\n'

		continue

	url = 'https://www.youtube.com/results?search_query=' + songsURL[arrange] + '+by+' + artistsURL[arrange] + '+lyrics'

	tube = get(url).text

	tubeSoup = Bsoup(tube, 'lxml')

	for link in tubeSoup.findAll('a'): # youtube is hard to web scrape

		if '/watch?v=' in link.get('href'):

			if not repeat: href = 'https://www.youtube.com' + link.get('href')

			if link.string == None: repeat = True

			else:

				vidTitle = str(link.string) + '.mp4'

				repeat = False # for the rest of the downloads

				break

	for rmv in range(len(vidTitle) - 3): # to remove the 'mp4' part to be added later

		if vidTitle[rmv] == '(' or vidTitle[rmv] == ')' or vidTitle[rmv] == ' ' or vidTitle[rmv] == '-' or vidTitle[rmv] == '&' or vidTitle[rmv] in chars:

			fileTitle.append(vidTitle[rmv])

	fileTitle = ''.join(fileTitle)

	yt = YouTube(href)

	stream = yt.streams.first()

	stream.download(path + '\\mp4')

	os.chdir(path + '\\mp4')

	try: clip = mp.VideoFileClip(fileTitle + '.mp4')

	except IOError: clip = mp.VideoFileClip(fileTitle + '.webm')

	os.chdir(path + '\\mp3')

	clip.audio.write_audiofile(short + '.mp3')

	file = openFile('a')

	file.write(short + '\n')

	fileTitle = [] # restarting for the other song titles

file.close()

print 'FINISHED'
