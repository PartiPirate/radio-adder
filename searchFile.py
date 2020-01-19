import os
import MusicTrack

audioExt = ('mp3', 'flac', 'ogg')

def searchFile(dirPath) :

	dirPath = os.path.abspath(dirPath)

	musicList = []

	fileList = os.listdir(dirPath)

	for file in fileList :

		os.chdir(dirPath)

		filePath = os.path.abspath(file)

		if os.path.isdir(filePath) :
			musicList += searchFile(filePath)

		elif os.path.basename(filePath).lower().endswith(audioExt) and not os.path.basename(filePath).startswith('.') :
			musicTrack = MusicTrack.MusicTrack(filePath)
			musicList.append(musicTrack)

	return musicList

