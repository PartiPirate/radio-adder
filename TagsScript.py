#!/usr/bin/python3

import searchFile
import os
import time
import settings
import sys
import DBTool

arg = sys.argv

if len(arg) < 2 :
	print("Please use : ", arg[0], " [directory]")
	exit()
elif not os.path.isdir(arg[1]) :
	print(arg[1], " is not a directory")
	exit()

startDir = arg[1] ;

result = searchFile.searchFile(startDir)

dbTool = DBTool.DBTool()

if settings.display != "none" and settings.display != "error" :
	print(str(len(result))+ " music file find")

i=0

for track in result :

	i += 1

	if settings.display != "none" and settings.display != "error" :
		print("file ", end='')
		print(i, end='/')
		print(len(result), end=' : ')
		print(track.getFilePath(), end='')

	if not track.isAlreadyTag() :
		if settings.display != "none" and settings.display != "error" :
			print("\033[92m TAG\033[0m")

		track.identify()
		track.loadMusicBrainzInfo()
		track.loadCoverURL()
		track.tag()

		time.sleep(1)
		
	else :
		if settings.display != "none" and settings.display != "error" :
			print("\033[96m SKIP\033[0m")

	musicDBInfo = dbTool.getMusicDBInfo(track)

	print("DBInfo : ", musicDBInfo)

	if musicDBInfo == "NOT_IN_DB" :
		dbTool.addMusicInDB(track)

	if settings.display == "all" :
		track.print()

	#print("\tFILE URL : ", track.getFileURL())


#print("FILE : "+result[0].getFilePath())