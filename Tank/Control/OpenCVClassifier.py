import threading
import math
import cv2
import numpy as np
import imutils
from collections import deque
from time import time,sleep

class OpenCVClassifier(object):
	
	def __init__(self):
		self.cap = cv2.VideoCapture(0)

		self.imageSize = (320, 240)
		self.imageCenter = (self.imageSize[0]/2, self.imageSize[1]/2)

		self.ball = None
		self.requireStop = False
		self.requireWait = False

		self.lastLocated = None

		self.topCascade = cv2.CascadeClassifier('OpenCVClassifier/top_cascade.xml')
		self.bottomCascade = cv2.CascadeClassifier('OpenCVClassifier/bottom_cascade.xml')

		t1 = threading.Thread(target = self.detector);
		t1.daemon = True;
		t1.start();

	def __del__(self):

		self.cap.release()
		cv2.destroyAllWindows()


	def detector(self):

		lostAttempts = 0
		while True:
			initial = time()

			_, frame = self.cap.read()
			frame = imutils.resize(frame, width=self.imageSize[0], height=self.imageSize[1])

			'''if self.isFrameBlurry(frame):
				self.requireStop = 0.2
				cv2.waitKey(1)
				sleep(0.03)
				continue'''

			detected = self.bottomCascade.detectMultiScale(frame)

			if detected == ():
				detected = self.topCascade.detectMultiScale(frame)
		
			for (x, y, w, h) in detected:
				self.ball = {
					'position'	: (x+w/2, y+h/2),
					'size'		: w/2
				}
				
				lostAttempts = 10

				cv2.circle(frame, self.ball['position'], self.ball['size'], (255,0,0), 2)
				cv2.circle(frame, self.ball['position'], 5, (0,0,255), -1)
				break

			if lostAttempts == 0:
				self.ball = None
			else:
				lostAttempts -= 1

			cv2.imwrite( "/var/www/html/capture.jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 50]);
			#cv2.imshow('image',frame)

			#print time() - initial
			cv2.waitKey(5)

	
	def isFrameBlurry(self, frame):
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		blur = cv2.Laplacian(gray, cv2.CV_64F).var()
		print blur
		return blur < 50



	def refresh(self):
		if self.requireWait == True:
			self.requireWait = False
			sleep(self.requireStop)
			self.requireStop = False

	def isAway(self):
		return self.ball['size'] < 35;

	def isNear(self):
		return self.ball['size'] > 50;

	def getAxisLeft(self):
		LEFT_X = 0
		LEFT_Y = 0

		return {
			'LEFT_X' : LEFT_X,
			'LEFT_Y' : LEFT_Y
		}

		if self.requireStop:
			self.requireWait = True
			sleep(0.1)
		elif not self.ball:
			print "BUSCANDO"
			if (self.lastLocated == 180):
				LEFT_Y = 0
				LEFT_X = -0.2
			else:
				LEFT_Y = 0
				LEFT_X = 0.2

			self.requireStop = 0.2
		else:
			if (self.ball['position'][0]<=self.imageCenter[0] -75 or self.ball['position'][0]>=self.imageCenter[0] +75):
				print "CENTRANDO"

				if(self.ball['position'][0] < self.imageCenter[0]):
					self.lastLocated = 180
					LEFT_Y = 0
					LEFT_X = -0.2

				elif(self.ball['position'][0] > self.imageCenter[0]):
					self.lastLocated = 0
					LEFT_Y = 0
					LEFT_X = 0.2

				self.requireStop = 0.2
			else:
				print self.ball['size'];
				if self.isAway() :
					print "ADELANTE"
					LEFT_Y = -0.8
				elif self.isNear():
					print "ATRAS"
					LEFT_Y = 0.8
				self.requireStop = 0.5

		return {
			'LEFT_X' : LEFT_X,
			'LEFT_Y' : LEFT_Y
		}


	def getAxisRight(self):
		RIGHT_X = 0
		RIGHT_Y = 0

		if not self.ball:
			print "BUSCANDO"
			if (self.lastLocated == 180):
				RIGHT_Y = 0
				RIGHT_X = 0
			else:
				RIGHT_Y = 0
				RIGHT_X = 0

		else:
			if (self.ball['position'][0]<=self.imageCenter[0] -50 or self.ball['position'][0]>=self.imageCenter[0] +50):
				print "CENTRANDO"

				if(self.ball['position'][0] < self.imageCenter[0]):
					self.lastLocated = 180
					RIGHT_X = -1

				elif(self.ball['position'][0] > self.imageCenter[0]):
					self.lastLocated = 0
					RIGHT_X = 1

			elif (self.ball['position'][1]<=self.imageCenter[1] -20 or self.ball['position'][1]>=self.imageCenter[1] +20):
				if (self.ball['position'][1] < self.imageCenter[1]) :
					RIGHT_Y = -1
				elif (self.ball['position'][1] > self.imageCenter[1]):
					RIGHT_Y = 1

		return {
			'RIGHT_X' : RIGHT_X,
			'RIGHT_Y' : RIGHT_Y
		}