import os
import taglib
import time
import acoustid
import requests
import datetime
import json
import settings
import urllib.parse
import re

class MusicTrack :

	def __init__(self, path, audioFormat) :

		self.__filePath = os.path.abspath(path)

		musicFile = taglib.File(self.__filePath)

		MusicTrack.__lastMusicBrainzCall = 0
		MusicTrack.__lastCoverCall = 0

		self.__audioFormat = audioFormat ;

		self.__free = False
		self.__duration = musicFile.length # in seconds

		self.__discNum 	 	= 0
		self.__discCount 	= 0

		self.__trackNum 	= 0
		self.__trackCount 	= 0

		if self.__audioFormat == "audio/mpeg" :
			if 'DISCNUMBER' in musicFile.tags and musicFile.tags['DISCNUMBER'] != [] :
				discStr = musicFile.tags['DISCNUMBER'][0]

				discStr = discStr.split("/")
				
				if len(discStr) == 2 :
					discStr[0] = re.sub('[^0-9]+', '', discStr[0])
					discStr[1] = re.sub('[^0-9]+', '', discStr[1])

					if discStr[0] != "" and discStr[1] != "" :
						self.__discNum 		= int(discStr[0])
						self.__discCount 	= int(discStr[1])

			if 'TRACKNUMBER' in musicFile.tags :
				trackStr = musicFile.tags['TRACKNUMBER'][0]

				trackStr = trackStr.split("/")
				
				if len(trackStr) == 2 :
					trackStr[0] = re.sub('[^0-9]+', '', trackStr[0])
					trackStr[1] = re.sub('[^0-9]+', '', trackStr[1])

					if trackStr[0] != "" and trackStr[1] != "" :
						self.__trackNum 	= int(trackStr[0])
						self.__trackCount 	= int(trackStr[1])
		elif self.__audioFormat == "audio/x-flac" or self.__audioFormat == "audio/ogg" :

			if 'DISCNUMBER' in musicFile.tags and musicFile.tags['DISCNUMBER'] != [] :
				discNum = re.sub('[^0-9]+', '', musicFile.tags['DISCNUMBER'][0])
				if discNum != "" :
					self.__discNum = int(discNum)

			if 'DISCTOTAL' in musicFile.tags and musicFile.tags['DISCTOTAL'] != [] :
				discCount = re.sub('[^0-9]+', '', musicFile.tags['DISCTOTAL'][0])
				if discCount != "" :
					self.__discCount = int(discCount)

			elif 'TOTALDISCS' in musicFile.tags and musicFile.tags['TOTALDISCS'] != [] :
				discCount = re.sub('[^0-9]+', '', musicFile.tags['TOTALDISCS'][0])
				if discCount != "" :
					self.__discCount = int(discCount)

			if 'TRACKNUMBER' in musicFile.tags and musicFile.tags['TRACKNUMBER'] != [] :
				trackNum = re.sub('[^0-9]+', '', musicFile.tags['TRACKNUMBER'][0])
				if trackNum != "" :
					self.__trackNum = int(trackNum)

			if 'TOTALTRACKS' in musicFile.tags and musicFile.tags['TOTALTRACKS'] != [] :
				trackCount = re.sub('[^0-9]+', '', musicFile.tags['TOTALTRACKS'][0])
				if trackCount != "" :
					self.__trackCount = int(trackCount)

			elif 'TRACKTOTAL' in musicFile.tags and musicFile.tags['TRACKTOTAL'] != [] :
				trackCount = re.sub('[^0-9]+', '', musicFile.tags['TRACKTOTAL'][0])
				if trackCount != "" :
					self.__trackCount = int(trackCount)

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
			genres = []
			for genre in self.__genres :
				genres += genre.split("/")
			self.__genres = genres
		else :
			self.__genres = []

		if 'LANGUAGE' in musicFile.tags :
			self.__language = musicFile.tags['LANGUAGE']
		else :
			self.__language = []

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

	def checkInfo(self) :

		if self.__mbRecordingID == [] :

			if self.__identify() :
				self.__mbReleaseID = []
				self.__mbAlbumArtistID = []
				self.__mbArtistsID = []
				self.__albumArtist = []
				self.__artists = []
				self.__album = []
				self.__title = []
				self.__genres = []
				self.__language = []
				self.__coverURL = []
				self.__language = []
				self.__coverURL = []
				self.__trackNum = 0
				self.__trackCount = 0
				self.__discNum = 0
				self.__discCount = 0

				self.__loadMusicBrainzRecording()

		else :
			if self.__title == [] :
				self.__loadMusicBrainzRecording()

			elif self.__album == [] :
				self.__loadMusicBrainzRecording()

			elif self.__artists == [] :
				self.__loadMusicBrainzRecording()

			elif self.__albumArtist == [] :
				self.__loadMusicBrainzRecording()

			elif self.__genres == [] :
				self.__loadMusicBrainzRecording()

			elif self.__language == [] or ( self.__language[0] != "none" and len(self.__language[0]) > 3 ) :
				self.__language = []
				self.__loadMusicBrainzRecording()

		if self.__mbReleaseID != [] :
			if self.__coverURL == [] :
				self.__loadCoverURL()

			if self.__trackNum == 0 :
				self.__loadMusicBrainzRelease()

			elif self.__trackCount == 0 :
				self.__loadMusicBrainzRelease()

			elif self.__discNum == 0 :
				self.__loadMusicBrainzRelease()

			elif self.__discCount == 0 :
				self.__loadMusicBrainzRelease()

		if settings.retagFile :
			self.__updateFileTags()


	def print(self) :

		print("\tFILE PATH : ",						self.__filePath)
		print("\tFILE URL : ",						self.getFileURL())
		print("\tALBUM ARTIST : ", 					self.__albumArtist)
		print("\tARTISTS : ", 						self.__artists)
		print("\tALBUM : ", 						self.__album)
		print("\tTRACK NUMBER : ", self.__trackNum, "/", self.__trackCount)
		print("\tDISC NUMBER : ", self.__discNum, "/", self.__discCount)
		print("\tTITLE : ", 						self.__title)
		print("\tGENRES : ", 						self.__genres)
		print("\tLANGUAGE : ", 						self.__language)
		print("\tFREE : ", 							self.__free)
		print("\tDURATION : ", 						self.__duration)
		print("\tMUSICBRAINZ RECORDING ID : ", 		self.__mbRecordingID)
		print("\tMUSICBRAINZ RELEASE ID : ", 		self.__mbReleaseID)
		print("\tMUSICBRAINZ ARTIST ID : ", 		self.__mbArtistsID)
		print("\tMUSICBRAINZ ALBUM ARTIST ID : ", 	self.__mbAlbumArtistID)
		print("\tCOVER URL : ", 					self.__coverURL)


	def __updateFileTags(self) :

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

		if self.__genres != [] :
			musicFile.tags['LANGUAGE'] = self.__language

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

		if self.__audioFormat == "audio/mpeg" :
			if self.__trackNum != 0 and self.__trackCount != 0 :
				musicFile.tags['TRACKNUMBER'] = [str(self.__trackNum)+"/"+str(self.__trackCount)]

			if self.__discNum != 0 and self.__discCount != 0 :
				musicFile.tags['DISCNUMBER'] = [str(self.__discNum)+"/"+str(self.__discCount)]

		elif self.__audioFormat == "audio/x-flac" or self.__audioFormat == "audio/ogg" :
			if self.__discNum != 0 :
				musicFile.tags['DISCNUMBER'] = [str(self.__discNum)]

			if self.__discCount != 0 :
				musicFile.tags['DISCTOTAL']  = [str(self.__discCount)]
				musicFile.tags['TOTALDISCS'] = [str(self.__discCount)]

			if self.__trackNum != 0 :
				musicFile.tags['TRACKNUMBER'] = [str(self.__trackNum)]

			if self.__trackCount != 0 :
				musicFile.tags['TOTALTRACKS'] = [str(self.__trackCount)]
				musicFile.tags['TRACKTOTAL']  = [str(self.__trackCount)]

		musicFile.save()

	def __identify(self) :

		if settings.display != "none" and settings.display != "error" :
			print("\t\033[96mIdentify track in AcoustID database\033[0m")

		data = acoustid.match(settings.acoustIDToken, self.__filePath, parse=False)

		#recordingID = data['results'][0]['recordings'][0]['id']

		if data['status'] == "ok" :

			if len(data['results']) <= 0 :
				if settings.display != "none" :
					print("\t\033[33mWARNING : unknown music\033[0m")
				return False

			for results in data['results'] :
				if 'recordings' in results :
					self.__mbRecordingID = [results['recordings'][0]['id']]
					return True
				else :
					if settings.display != "none" :
						print("\t\033[33mWARNING : unknown music\033[0m")

					return False


		else :
			if settings.display != "none" :
				print("\t\033[33mWARNING : unknown music\033[0m")
			return False

	def __loadMusicBrainzRecording(self) :

		if self.__mbRecordingID != [] :

			if settings.display != "none" and settings.display != "error" :
				print("\t\033[92mGet Recording info in MusicBrainz\033[0m")

			url = "http://musicbrainz.org/ws/2/recording/" + self.__mbRecordingID[0] + "?inc=artist-credits+releases+genres&fmt=json"

			OK = False

			## GET MusicBrainz Recording json ##

			for tryCount in range(1,100):
				try:
					timeSinceLastCall = time.time() - MusicTrack.__lastMusicBrainzCall
					if timeSinceLastCall < 1.1 :
						time.sleep(1.1 - timeSinceLastCall)

					response = requests.get(url)
					MusicTrack.__lastMusicBrainzCall = time.time()
				except :
					if settings.display != "none" :
						print("\t\033[33mWARNING : MusicBrainz Recording error, retry in 1 s \033[0m")

					time.sleep(1)
				else :
					OK = True
					break
			
			if not OK :
				if settings.display != "none" :
					print("\t\033[91mERROR : MusicBrainz Recording error after 100 retry\033[0m")
				return

			if response.status_code == 200 :

				## Parce json ###

				recordingJSON = response.json()

				if 'title' in recordingJSON :
					self.__title = [recordingJSON["title"]]

				if 'genres' in recordingJSON :

					for genre in recordingJSON['genres'] :
						if 'name' in genre :
							self.__genres += [genre['name']]

				if 'artist-credit' in recordingJSON and ( self.__artists == [] or self.__mbArtistsID == [] ) :
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

						if self.__mbReleaseID != [] and 'id' in release and release['id'] != self.__mbReleaseID :
							oldestRelease = release
							break

						if 'status' in release and release['status'] != "Official" :
							if oldestRelease == None :
								oldestRelease = release

						elif 'date' in release :

							date = re.sub('[^0-9]+', '', release['date'])

							if len(date) == 8 :
								year = int(date[0:4])
								mounth = int(date[4:6])
								day = int(date[6:8])

								if mounth > 12 :
									mounth = 12

								if mounth < 1 :
									mounth = 1

								if day > 31 :
									day = 31

								if day < 1 :
									day = 1

								date = datetime.date(year, mounth, day)

							elif len(date) == 6 :
								year = int(date[0:4])
								mounth = int(date[4:6])

								if mounth > 12 :
									mounth = 12

								if mounth < 1 :
									mounth = 1

								date = datetime.date(year, mounth, 28)

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

					if self.__language == [] :
						if 'text-representation' in oldestRelease and 'language' in oldestRelease['text-representation'] :
							if oldestRelease['text-representation']['language'] != None :
								self.__language = [oldestRelease['text-representation']['language']]
							else :
								self.__language = ["none"]
						else :
							self.__language = ["none"]

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
					print("\t\033[91mERROR : load MusicBrainz Recording info return ", response.status_code, "\033[0m")

	def __loadMusicBrainzRelease(self) :

		if self.__mbReleaseID != [] :

			if settings.display != "none" and settings.display != "error" :
				print("\t\033[92mGet Release info in MusicBrainz\033[0m")

			url = "http://musicbrainz.org/ws/2/release/" + self.__mbReleaseID[0] + "?inc=artist-credits+labels+discids+recordings&fmt=json"

			OK = False

			## GET MusicBrainz Recording json ##

			for tryCount in range(1,100):
				try:
					timeSinceLastCall = time.time() - MusicTrack.__lastMusicBrainzCall
					if timeSinceLastCall < 1.1 :
						time.sleep(1.1 - timeSinceLastCall)

					response = requests.get(url)
					MusicTrack.__lastMusicBrainzCall = time.time()
				except :
					if settings.display != "none" :
						print("\t\033[33mWARNING : MusicBrainz Release error, retry in 1 s \033[0m")

					time.sleep(1)
				else :
					OK = True
					break
			
			if not OK :
				if settings.display != "none" :
					print("\t\033[91mERROR : MusicBrainz Release error after 100 retry\033[0m")
				return

			if response.status_code == 200 :

				releaseJSON = response.json()

				if 'media' in releaseJSON :
					self.__discCount = len(releaseJSON['media'])
					mediaPos = 0
					for media in releaseJSON['media'] :
						mediaPos += 1
						if 'tracks' in media :
							for track in media['tracks'] :
								if 'recording' in track :
									recording = track['recording']
									if 'id' in recording and self.__mbRecordingID != [] and recording['id'] == self.__mbRecordingID[0] :
										if 'position' in track :
											self.__trackNum = track['position']
										elif 'number' in track :
											self.__trackNum = int(track['number'])
										if 'track-count' in media : 
											self.__trackCount = media['track-count']
										self.__discNum = mediaPos
					self.__discCount = mediaPos


			else :
				if settings.display != "none" :
					print("\t\033[91mERROR : load MusicBrainz Release info return ", response.status_code, "\033[0m")

	def __loadCoverURL(self) :


		if settings.display != "none" and settings.display != "error" :
			print("\t\033[92mGet album cover URL\033[0m")


		if self.__mbReleaseID != [] and len(self.__mbReleaseID) > 0 :
			infoCoverURL = "https://ia801900.us.archive.org/13/items/mbid-" + self.__mbReleaseID[0] + "/index.json"

			#print("url : ", infoCoverURL)

			OK = False

			for tryCount in range(1, 100) :
				try:
					timeSinceLastCall = time.time() - MusicTrack.__lastCoverCall
					if timeSinceLastCall < 1.1 :
						time.sleep(1.1 - timeSinceLastCall)

					infoCoverResponse = requests.get(infoCoverURL)
					MusicTrack.__lastCoverCall = time.time()
				except :
					if settings.display != "none" :
						print("\t\033[33mWARNING : cover request error, retry in 1 s \033[0m")

					time.sleep(1)
				else :
					OK = True
					break
			
			if not OK :
				if settings.display != "none" :
					print("\t\033[91mERROR : cover request error after 100 retry\033[0m")
				return


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
							self.__coverURL = "no cover"

							if settings.display != "none" :
								print("\t\033[91mERROR : get final cover URL return ", startCoverURLResponse.url, "\033[0m")


			else : 
				self.__coverURL = "no cover"

				if settings.display != "none" :
					print("\t\033[33mWARNING : no cover (", infoCoverResponse.status_code, " - url:", infoCoverURL, ")\033[0m")
	
	def folderSort(self, startDir) :

		startDir = os.path.abspath(startDir)
		artist 	= "Unknown"
		album 	= "Unknown"
		title 	= "Unknown"

		fileBaseName = os.path.basename(self.__filePath)

		fileExt = fileBaseName.split(".")[-1]

		if self.__albumArtist != [] : 
			artist = self.__albumArtist[0].replace("/", "")

		if self.__album != [] :
			album = self.__album[0].replace("/", "")

		if self.__title != [] :
			title = self.__title[0].replace("/", "")


		fileName = 	startDir
		fileName += "/"+artist
		fileName += "/"+album+"/"

		if self.__discNum != 0 :
			fileName += str(self.__discNum) + "."

		if self.__trackNum != 0 :
			fileName += str(self.__trackNum) + " - "

		fileName += title+"."+fileExt

		if self.__filePath != fileName :

			folderName = startDir+"/"+artist

			if not os.path.exists(folderName) :
				os.mkdir(folderName)

			folderName += "/"+album

			if not os.path.exists(folderName) :
				os.mkdir(folderName)

			if not os.path.exists(fileName) :
				os.rename(self.__filePath, fileName)
				self.__filePath = fileName

				if settings.display != "none" and settings.display != "error" :
					print("\t\033[92mRename file as ", fileName, "\033[0m")

			else :
				i=2

				while True:

					fileName = folderName+"/"

					if self.__discNum != 0 :
						fileName += str(self.__discNum) + "."

					if self.__trackNum != 0 :
						fileName += str(self.__trackNum) + " - "

					fileName += title+" ("+str(i)+")."+fileExt

					if self.__filePath == fileName :
						break
					elif not os.path.exists(fileName) :
						os.rename(self.__filePath, fileName)
						self.__filePath = fileName

						if settings.display != "none" and settings.display != "error" :
							print("\t\033[92mRename file as ", fileName, "\033[0m")

					else :
						i += 1
