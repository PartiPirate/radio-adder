
import mysql.connector
import settings

class DBTool :

	def __init__(self) :

		self.__db = mysql.connector.connect(	host=settings.bddHost,  		# your host 
                     							user=settings.bdduser,       	# username
                     							passwd=settings.bddPassword,    # password
                     							db=settings.bddName)   			# name of the database

	def getMusicDBInfo(self, musicTrack) :

		if not self.__db.is_connected() :
			self.__db.reconnect()

		cursor = self.__db.cursor()

		operation = "SELECT tra_title, tra_author, tra_album, tra_duration, tra_genres, tra_free FROM tracks WHERE tra_url = %(url)s ;"
		params = { 'url': musicTrack.getFileURL() }

		try :
			cursor.execute(operation, params)
		except :
			if settings.display != "none" :
				print("\t\033[91mERROR : bdd execution, statement : ", cursor.statement, "\033[0m")
			return "ERROR"

		rowCount = 0 

		for row in cursor.fetchall() :
			rowCount += 1


		if rowCount <= 0 :
			return "NOT_IN_DB"
		elif rowCount > 1 :
			if settings.display != "none" :
				print("\t\033[93mWARNING : multiple entry in bdd : ", cursor.statement, "\033[0m")
			return "MULTIPLE_ENTRY"

		#row = cursor.fetchone()

		#cursor.fetchall()
		cursor.close()

		if 		row[0] != musicTrack.getTitle() :
			return "NEED_UPDATE"
		elif 	row[1] != musicTrack.getAlbumArtist() :
			return "NEED_UPDATE"
		elif 	row[2] != musicTrack.getAlbum() :
			return "NEED_UPDATE"
		elif 	row[3] != musicTrack.getDuration() :
			return "NEED_UPDATE"
		elif 	row[4] != musicTrack.getGenres() :
			return "NEED_UPDATE"
		elif 	row[5] != musicTrack.isFree() :
			return "NEED_UPDATE"

		return "OK"

	def addMusicInDB(self, musicTrack) :

		if not self.__db.is_connected() :
			self.__db.reconnect()

		cursor = self.__db.cursor()

		#bytes(test, 'utf-8')

		insert_stmt = (	
			"INSERT INTO tracks (tra_url, tra_title, tra_author, tra_album, tra_duration, tra_genres, tra_free) "
			"VALUES (%(url)s, %(title)s, %(author)s, %(album)s, %(duration)s, %(genres)s, %(free)s) ;"
		)

		data = {}

		data['url'] 		= musicTrack.getFileURL()
		data['title'] 		= musicTrack.getTitle()
		data['author'] 		= musicTrack.getAlbumArtist()
		data['album'] 		= musicTrack.getAlbum()
		data['duration']	= musicTrack.getDuration()
		data['genres']		= musicTrack.getGenres()
		data['free']		= musicTrack.isFree()

		try :
			cursor.execute(insert_stmt, data)
		except :
			if settings.display != "none" :
				print("\t\033[91mERROR : bdd execution, statement : ", cursor.statement, "\033[0m")

		self.__db.commit()
		cursor.close()

	def updateMusicInDB(self, musicTrack) :

		if not self.__db.is_connected() :
			self.__db.reconnect()

		cursor = self.__db.cursor()

		#bytes(test, 'utf-8')

		# UPDATE `tracks` SET `tra_title`='Antauparolo de Prapatra Kaciko', `tra_author`='BaRok\' Projeto', `tra_duration`='236' WHERE `tra_id`='1';


		insert_stmt = (	
			"UPDATE `tracks` SET "
			"`tra_title`=%(title)s, "
			"`tra_author`=%(author)s, "
			"`tra_album`=%(album)s, "
			"`tra_duration`=%(duration)s, "
			"`tra_genres`=%(genres)s, "
			"`tra_free`=%(free)s "
			"WHERE `tra_url`=%(url)s ; "
		)

		data = {}

		data['url'] 		= musicTrack.getFileURL()
		data['title'] 		= musicTrack.getTitle()
		data['author'] 		= musicTrack.getAlbumArtist()
		data['album'] 		= musicTrack.getAlbum()
		data['duration']	= musicTrack.getDuration()
		data['genres']		= musicTrack.getGenres()
		data['free']		= musicTrack.isFree()

		try :
			cursor.execute(insert_stmt, data)
		except :
			if settings.display != "none" :
				print("\t\033[91mERROR : bdd execution, statement : ", cursor.statement, "\033[0m")

		self.__db.commit()
		cursor.close()


