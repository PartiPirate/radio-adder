import os
import MusicTrack
import filetype
import settings

audioExt = ('mp3', 'flac', 'ogg')
audioType = ('audio/mpeg', 'audio/ogg', 'audio/x-flac')

def searchFile(dirPath) :

	dirPath = os.path.abspath(dirPath)

	musicList = []

	fileList = os.listdir(dirPath)

	os.chdir(dirPath)
	
	for file in fileList :

		filePath = os.path.abspath(file)

		if os.path.isdir(filePath) :
			musicList += searchFile(filePath)

		else :
			fileType = filetype.guess(filePath) ;

			if fileType is not None and fileType.mime in audioType :
				musicTrack = MusicTrack.MusicTrack(filePath, fileType.mime)
				musicList.append(musicTrack)
	

	os.chdir("..")

	return musicList


def clearDir(dirPath) :

	dirPath = os.path.abspath(dirPath)

	fileList = os.listdir(dirPath)

	os.chdir(dirPath)

	for file in fileList :

		filePath = os.path.abspath(file)

		if os.path.isdir(filePath) :
			clearDir(filePath)

			if len(os.listdir(filePath)) == 0 :
				os.rmdir(filePath)
				if settings.display != "none" and settings.display != "error" :
					print("\033[93mRemove ", filePath, "\033[0m")

		else :
			fileType = filetype.guess(filePath) ;

			if fileType is None or fileType.mime not in audioType :
				os.remove(filePath)
				if settings.display != "none" and settings.display != "error" :
					print("\033[93mRemove ", filePath, "\033[0m")

	os.chdir("..")