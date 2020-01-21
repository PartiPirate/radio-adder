import os
import MusicTrack
import filetype

audioExt = ('mp3', 'flac', 'ogg')
audioType = ('audio/mpeg', 'audio/ogg', 'audio/x-flac')

def searchFile(dirPath) :

	dirPath = os.path.abspath(dirPath)

	musicList = []

	fileList = os.listdir(dirPath)

	for file in fileList :

		os.chdir(dirPath)

		filePath = os.path.abspath(file)

		if os.path.isdir(filePath) :
			musicList += searchFile(filePath)

		else :
			fileType = filetype.guess(filePath) ;

			if fileType is not None and fileType.mime in audioType :
				musicTrack = MusicTrack.MusicTrack(filePath)
				musicList.append(musicTrack)
	

	return musicList

