
import mysql.connector
import settings

class DBTool :

	def __init__(self) :

		self.__db = mysql.connector.connect(	host="localhost",  		# your host 
                     							user="alex",       		# username
                     							passwd="Mp607bdQ@?",    # password
                     							db="MusicBot")   		# name of the database

	def getMusicDBInfo(self, musicTrack) :

		if not self.__db.is_connected() :
			self.__db.reconnect()

		cursor = self.__db.cursor()

		operation = "SELECT tra_title, tra_author, tra_album, tra_duration, tra_genres, tra_free FROM MusicBot.tracks WHERE tra_url LIKE %(url)s ;"
		params = { 'url': musicTrack.getFileURL() }

		try :
			cursor.execute(operation, params)
		except :
			if settings.display != "none" :
				print("\t\033[91mERROR : bdd execution, statement : ", cursor.statement, "\033[0m")
			return "ERROR"

		print("ROW COUNT : ", cursor.rowcount)

		if cursor.rowcount <= 0 :
			cursor.fetchall()
			cursor.close()
			return "NOT_IN_DB"
		elif cursor.rowcount > 1 :
			if settings.display != "none" :
				print("\t\033[33mWARNING : multiple entry in bdd : ", cursor.statement, "\033[0m")
			cursor.fetchall()
			cursor.close()
			return "MULTIPLE_ENTRY"

		row = cursor.fetchone()

		cursor.fetchall()
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
			"INSERT INTO MusicBot.tracks (tra_url, tra_title, tra_author, tra_album, tra_duration, tra_genres, tra_free) "
			"VALUES (%(url)s, %(title)s, %(author)s, %(album)s, %(duration)s, %(genres)s, %(free)s) ;"
		)

		data = {}

		data['url'] 		= musicTrack.getFileURL()
		data['title'] 		= bytes(musicTrack.getTitle(), 'utf-8')
		data['author'] 		= bytes(musicTrack.getAlbumArtist(), 'utf-8')
		data['album'] 		= bytes(musicTrack.getAlbum(), 'utf-8')
		data['duration']	= musicTrack.getDuration()
		data['genres']		= bytes(musicTrack.getGenres(), 'utf-8')
		data['free']		= musicTrack.isFree()

		print(data)

		try :
			cursor.execute(insert_stmt, data)
		except :
			if settings.display != "none" :
				print("\t\033[91mERROR : bdd execution, statement : ", cursor.statement, "\033[0m")

		self.__db.commit()
		cursor.close()

