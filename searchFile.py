import os
import MusicTrack

audioExt = ('mp3', 'flac', 'ogg')

def searchFile(dirPath) :

	dirPath = os.path.abspath(dirPath)

	musicList = []

	fileList = os.listdir(dirPath)

	os.chdir(dirPath)
	
	for file in fileList :

		filePath = os.path.abspath(file)

		if os.path.isdir(filePath) :
			musicList += searchFile(filePath)

		elif os.path.basename(filePath).lower().endswith(audioExt) and not os.path.basename(filePath).startswith('.') :
			musicTrack = MusicTrack.MusicTrack(filePath)
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


		elif not os.path.basename(filePath).lower().endswith(audioExt) or os.path.basename(filePath).startswith('.') :
			os.remove(filePath)

	os.chdir("..")