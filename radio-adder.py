#!/usr/bin/python3

import FileTools
import os
import settings
import sys
import DBTools

arg = sys.argv

if len(arg) < 2 :
	print("Please use : ", arg[0], " [directory]")
	exit()
elif not os.path.isdir(arg[1]) :
	print(arg[1], " is not a directory")
	exit()

startDir = arg[1] ;

result = FileTools.searchFile(startDir)

dbTools = DBTools.DBTools()

if settings.display != "none" and settings.display != "error" :
	print(str(len(result))+ " music file find")

i=0

for track in result :

	i += 1

	if settings.display != "none" and settings.display != "error" :
		print("file ", end='')
		print(i, end='/')
		print(len(result), end=' : ')
		print(track.getFilePath())

#	if settings.display != "none" and settings.display != "error" :
#		print("\t\033[92mTAG SET\033[0m")

	track.checkInfo()

	if settings.sortFile :
		track.folderSort(startDir)

	musicDBInfo = dbTools.getMusicDBInfo(track)

	if   musicDBInfo == "NOT_IN_DB" :
		dbTools.addMusicInDB(track)

		if settings.display != "none" and settings.display != "error" :
			print("\t\033[92mAdd track in database\033[0m")

	elif musicDBInfo == "NEED_UPDATE" :

		if settings.updateDirection is "FiletoDB":

			dbTools.updateMusicInDB(track)

			if settings.display != "none" and settings.display != "error" :
				print("\t\033[95mUpdate track in database\033[0m")

		elif settings.updateDirection is "DBtoFile":

			dbTools.updateMusicFromDB(track)

			if settings.display != "none" and settings.display != "error" :
				print("\t\033[95mUpdate track from database\033[0m")




	if settings.display == "all" :
		track.print()

	#print("\tFILE URL : ", track.getFileURL())

if settings.removeUselessFileAndFolder :
	FileTools.clearDir(startDir)

if settings.removeNotFoundFileInDB :
	dbTools.removeNotFoundFileInDB()

#print("FILE : "+result[0].getFilePath())
