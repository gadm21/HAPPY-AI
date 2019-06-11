import mysql.connector
import cv2
import sys
import os

class Database:
	def __getitem__(self,key):
		return getattr(self,key)

	def __setitem__(self,key,value):
		setattr(self,key,value)

	def addFaceToDemographic(self,faceAttr):
		try:
			self.db = mysql.connector.connect(
				host="localhost",
				user="root",
				passwd="root",
				database="face"
			)

			stmt1 = "INSERT INTO DemographicSingle (Gender,Age,PathToImage) VALUES (%s,%s,%s);"

			#into demographicSingle
			gender = faceAttr.gender
			age = faceAttr.age
			pathToImage = faceAttr.pathToImage
			param1 = (gender,age,pathToImage)

			cursor = self.db.cursor()
			cursor.execute(stmt1, param1)
			cursor.close()
			self.db.commit()

			print('Image of face {} is saved to mysql database.'.format(faceAttr.awsID))
					
		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)
			print("[MYSQL]",e)

	def close(self):
		self.db.close()

if __name__ == '__main__':
	db = Database('localhost','oka','oka12345','face')