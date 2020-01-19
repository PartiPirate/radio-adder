import os
import taglib
import acoustid
import requests
import datetime
import json
import settings
import urllib.parse

class MusicTrack :

	def __init__(self, path) :

		self.__filePath = os.path.abspath(path)

		musicFile = taglib.File(self.__filePath)

		self.__free = False
		self.__duration = musicFile.length # in seconds

		if 'ALBUMARTIST' in musicFile.tags :
			self.__albumArtist = musicFile.tags['ALBUMARTIST']
		else :
			self.__albumArtist = []

		if 'ARTISTS' in musicFile.tags :
			self.__artists = musicFile.tags['ARTISTS']
		else :
			self.__artists = []

		if 'ALBUM' in musicFile.tags :
			self.__album = musicFile.tags['ALBUM']
		else :
			self.__album = []

		if 'TITLE' in musicFile.tags :
			self.__title = musicFile.tags['TITLE']
		else :
			self.__title = []

		if 'GENRE' in musicFile.tags :
			self.__genres = musicFile.tags['GENRE']
		else :
			self.__genres = []

		if 'MUSICBRAINZ_TRACKID' in musicFile.tags :
			self.__mbRecordingID = musicFile.tags['MUSICBRAINZ_TRACKID']
		else :
			self.__mbRecordingID = []

		if 'MUSICBRAINZ_ALBUMID' in musicFile.tags :
			self.__mbReleaseID = musicFile.tags['MUSICBRAINZ_ALBUMID']
		else :
			self.__mbReleaseID = []

		if 'MUSICBRAINZ_ALBUMARTISTID' in musicFile.tags :
			self.__mbAlbumArtistID = musicFile.tags['MUSICBRAINZ_ALBUMARTISTID']
		else :
			self.__mbAlbumArtistID = []

		if 'MUSICBRAINZ_ARTISTID' in musicFile.tags :
			self.__mbArtistsID = musicFile.tags['MUSICBRAINZ_ARTISTID']
		else :
			self.__mbArtistsID = []

		if 'COVER_URL' in musicFile.tags :
			self.__coverURL = musicFile.tags['COVER_URL']
		else :
			self.__coverURL = []

	def getFilePath(self) :

		return self.__filePath

	def getFileURL(self) :

		fileURL = os.path.relpath(self.__filePath, settings.webServiceRacinePath)

		fileURL = urllib.parse.quote(fileURL)
		
		if settings.webServiceURL.endswith('/') :
			fileURL = settings.webServiceURL + fileURL
		else :
			fileURL = settings.webServiceURL + "/" + fileURL

		return fileURL

	def getCoverURL(sefl) :

		if self.__coverURL == [] :
			return ""

		else :
			return self.__coverURL[0]

	def isFree(self) :

		return self.__free

	def getDuration(self) :

		return self.__duration

	def getTitle(self) :

		if self.__title == [] :
			return ""

		else :
			return self.__title[0]

	def getAlbumArtist(self) :

		if self.__albumArtist == [] :
			return ""

		else :
			return self.__albumArtist[0]

	def getArtists(self) :

		first = True
		output = ""

		for title in self.__artists :

			if not first :
				output += ", "

			output += title
		
		return output ;

	def getAlbum(self) :

		if self.__album == [] :
			return ""

		else :
			return self.__album[0]

	def getGenres(self) :

		first = True
		output = ""

		for title in self.__genres :

			if not first :
				output += ", "

			output += title

			first = False
		
		return output ;

	def getRecordingID(self) :

		if self.__mbRecordingID == [] :
			return ""

		else :
			return self.__mbRecordingID[0]

	def getReleaseID(self) :

		if self.__mbReleaseID == [] :
			return ""

		else :
			return self.__mbReleaseID[0]

	def getAlbumArtistID(self) :

		if self.__mbAlbumArtistID == [] :
			return ""

		else :
			return self.__mbAlbumArtistID[0]

	def getArtistsID(self) :

		if self.__mbArtistsID == [] :
			return ""

		else :
			return self.__mbArtistsID[0] 

	def identify(self) :

		musicFile = taglib.File(self.__filePath) 

		if 'MUSICBRAINZ_TRACKID' in musicFile.tags :
			self.__mbRecordingID = musicFile.tags['MUSICBRAINZ_TRACKID']

		else :
			data = acoustid.match(settings.acoustIDToken, self.__filePath, parse=False)

			#recordingID = data['results'][0]['recordings'][0]['id']

			if data['status'] == "ok" :

				if len(data['results']) <= 0 :
					if settings.display != "none" :
						print("\t\033[91mERROR : unknown music\033[0m")
					return

				for results in data['results'] :
					if 'recordings' in results :
						self.__mbRecordingID = [results['recordings'][0]['id']]

			else :
				if settings.display != "none" :
					print("\t\033[91mERROR : unknown music\033[0m")

	def loadMusicBrainzInfo(self) :

		if self.__mbRecordingID != [] :

			url = "http://musicbrainz.org/ws/2/recording/" + self.__mbRecordingID[0] + "?inc=artist-credits+releases+genres&fmt=json"

			response = requests.get(url)

			if response.status_code == 200 :

				recordingJSON = response.json()

				if 'title' in recordingJSON :
					self.__title = [recordingJSON["title"]]

				if 'genres' in recordingJSON :
					self.__genres = []

					for genre in recordingJSON['genres'] :
						if 'name' in genre :
							self.__genres += [genre['name']]

				if 'artist-credit' in recordingJSON :
					self.__artists = []
					self.__mbArtistsID = []

					for artist in recordingJSON["artist-credit"] :
						if 'name' in artist :
							self.__artists += [artist["name"]]

						if 'artist' in artist :
							if 'id' in artist['artist'] :
								self.__mbArtistsID += [artist['artist']['id']]

				oldestRelease = None ;
				oldestDate = datetime.date.today() ;

				if 'releases' in recordingJSON :
					for release in recordingJSON['releases'] :

						if 'status' in release and release['status'] != "Official" :
							if oldestRelease == None :
								oldestRelease = release

						elif 'date' in release :

							date = release['date']

							if len(date) == 10 :
								date = date.split('-')
								year = int(date[0])
								mounth = int(date[1])
								day = int(date[2])
								date = datetime.date(year, mounth, day)

							elif len(date) == 7 :
								date = date.split('-')
								year = int(date[0])
								mounth = int(date[1])
								date = datetime.date(year, mounth, 31)

							elif len(date) == 4 :
								date = datetime.date(int(date), 12, 31)

							else :
								date = datetime.date.today()

							if date < oldestDate :
								oldestDate = date 
								oldestRelease = release

						else :
							if oldestRelease == None :
								oldestRelease = release

				if oldestRelease != None :
					if 'title' in oldestRelease :
						self.__album = [oldestRelease['title']]

					if 'id' in oldestRelease :
						self.__mbReleaseID = [oldestRelease['id']]

					if self.__genres == [] and 'genres' in oldestRelease :
						for genre in oldestRelease['genres'] :
							if 'name' in genre :
								self.__genres += [genre['name']]

					if 'artist-credit' in oldestRelease :
						self.__albumArtist = []
						self.__mbAlbumArtistID = []

						for artist in oldestRelease['artist-credit'] :
							if 'name' in artist :
								self.__albumArtist += [artist['name']]

							if 'artist' in artist :
								if 'id' in artist['artist'] :
									self.__mbAlbumArtistID += [artist['artist']['id']]

								if self.__genres == [] and 'genres' in artist['artist'] :
									for genre in artist['artist']['genres'] :
										if 'name' in genre :
											self.__genres += [genre['name']]



			else :
				if settings.display != "none" :
					print("\t\033[91mERROR : load MusicBrainz info return ", response.status_code, "\033[0m")

	def loadCoverURL(self) :

		if self.__mbRecordingID != [] :

			musicFile = taglib.File(self.__filePath) 

			if 'COVER_URL' in musicFile.tags :
				self.__coverURL = musicFile.tags['COVER_URL']

			else :

				if self.__mbReleaseID != "" :
					infoCoverURL = "https://ia801900.us.archive.org/13/items/mbid-" + self.__mbReleaseID[0] + "/index.json"

					#print("url : ", infoCoverURL)

					infoCoverResponse = requests.get(infoCoverURL)

					if infoCoverResponse.status_code == 200 :

						infoJSON = infoCoverResponse.json()

						infoImage = None ;

						if 'images' in infoJSON :
							for image in infoJSON['images'] :
								if 'types' in image :
									for types in image['types'] :
										if types == "Front" :
											infoImage = image
											break

						
						if infoImage != None :
							startCoverURL = ""

							#print(json.dumps(infoImage, sort_keys=True, indent=4))

							if 'thumbnails' in infoImage :
								if   'small' in infoImage['thumbnails'] :
									startCoverURL = infoImage['thumbnails']['small']
								elif '250' in infoImage['thumbnails'] :
									startCoverURL = infoImage['thumbnails']['250']
								elif 'large' in infoImage['thumbnails'] :
									startCoverURL = infoImage['thumbnails']['large']
								elif '500' in infoImage['thumbnails'] :
									startCoverURL = infoImage['thumbnails']['500']

							if startCoverURL == "" and 'image' in infoImage :
								startCoverURL = infoImage['image']

							if startCoverURL != "" :
								startCoverURLResponse = requests.get(startCoverURL)

								if startCoverURLResponse.status_code == 200 :
									self.__coverURL = [startCoverURLResponse.url] # get final URL through redirect

								else :
									if settings.display != "none" :
										print("\t\033[91mERROR : get final cover URL return ", startCoverURLResponse.url, "\033[0m")


					else : 
						if settings.display != "none" :
							print("\t\033[93mWARNING : no cover (", infoCoverResponse.status_code, " - url:", infoCoverURL, ")\033[0m")

	def isAlreadyTag(self) :

		musicFile = taglib.File(self.__filePath) 

		if 'TAG_VERSION' in musicFile.tags :
			if musicFile.tags['TAG_VERSION'][0] == settings.tagVersion :
				return True
			else :
				return False
		else :
			return False

	def tag(self) :

		musicFile = taglib.File(self.__filePath) 

		if self.__albumArtist != [] :
			musicFile.tags['ALBUMARTIST'] = self.__albumArtist

		if self.__artists != [] :
			musicFile.tags['ARTISTS'] = self.__artists

		if self.__album != "" :
			musicFile.tags['ALBUM'] = self.__album

		if self.__title != "" :
			musicFile.tags['TITLE'] = self.__title

		if self.__genres != [] :
			musicFile.tags['GENRE'] = self.__genres

		if self.__mbRecordingID != "" :
			musicFile.tags['MUSICBRAINZ_TRACKID'] = self.__mbRecordingID

		if self.__mbReleaseID != "" :
			musicFile.tags['MUSICBRAINZ_ALBUMID'] = self.__mbReleaseID

		if self.__mbAlbumArtistID != [] :
			musicFile.tags['MUSICBRAINZ_ALBUMARTISTID'] = self.__mbAlbumArtistID

		if self.__mbArtistsID != [] :
			musicFile.tags['MUSICBRAINZ_ARTISTID'] = self.__mbArtistsID

		if self.__coverURL != "" :
			musicFile.tags['COVER_URL'] = self.__coverURL

		musicFile.tags['TAG_VERSION'] = [settings.tagVersion]

		#print(musicFile.tags)

		musicFile.save()

	def print(self) :

		print("\tFILE PATH : ",						self.__filePath)
		print("\tALBUM ARTIST : ", 					self.__albumArtist)
		print("\tARTISTS : ", 						self.__artists)
		print("\tALBUM : ", 						self.__album)
		print("\tTITLE : ", 						self.__title)
		print("\tGENRES : ", 						self.__genres)
		print("\tFREE : ", 							self.__free)
		print("\tDURATION : ", 						self.__duration)
		print("\tMUSICBRAINZ RECORDING ID : ", 		self.__mbRecordingID)
		print("\tMUSICBRAINZ RELEASE ID : ", 		self.__mbReleaseID)
		print("\tMUSICBRAINZ ARTIST ID : ", 		self.__mbArtistsID)
		print("\tMUSICBRAINZ ALBUM ARTIST ID : ", 	self.__mbAlbumArtistID)
		print("\tCOVER URL : ", 					self.__coverURL)




			