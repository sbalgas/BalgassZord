import threading
import math
import cv2
import numpy as np
import imutils
from collections import deque
from time import time,sleep

class OpenCVColor(object):
	
	def __init__(self):
		self.cap = cv2.VideoCapture(0)
		self.lastPosition = "LEFT";

		self.stopped = False
		self.requiereStop = False

		self.orange = {
			'lower' : (0,50,80),
			'upper' : (20,255,255)
		}

		self.ball = None
		self.track = deque(maxlen=64)

		self.BallPosAVG = deque(maxlen=3)

		sleep(1)

		t1 = threading.Thread(target = self.detector);
		t1.daemon = True;
		t1.start();

	def __del__(self):

		self.cap.release()
		cv2.destroyAllWindows()


	def detector(self):
		while True:
			(grabbed, frame) = self.cap.read()
			frame = imutils.resize(frame, width=640, height = 480)
			contours = self.getContours(frame)
			center = None

			if len(contours) > 0:
				x, y, center, self.radius = self.getBall(contours)
				if self.radius > 100:
					cv2.circle(frame, (int(x), int(y)), int(self.radius),
						(17, 70, 244), 2)
					cv2.circle(frame, center, 5, (0, 0, 255), -1)
					cv2.putText(frame, "orange ball {}".format(self.radius), (int(x-self.radius),int(y-self.radius)), cv2.FONT_HERSHEY_SIMPLEX, 0.6,(0,140,255),2)

			self.track.appendleft(center)
			
			for i in xrange(1, len(self.track)):
				if self.track[i - 1] is None or self.track[i] is None:
					continue
				
				thickness = int(np.sqrt(64 / float(i + 1)) * 2.5)
				cv2.line(frame, self.track[i - 1], self.track[i], (0, 0, 255), thickness)
		 
			cv2.imwrite( "/var/www/html/capture.jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 50]);
			#cv2.imshow("Frame", frame)
			key = cv2.waitKey(1) & 0xFF

	def getContours(self, frame):
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		mask = cv2.inRange(hsv, self.orange['lower'], self.orange['upper'])
		mask = cv2.erode(mask, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=2)

		return cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

	def getBall(self, contours):
		c = max(contours, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		return x, y, center, radius

	def getAverage(self, value, value2):
		return ((value[0] + value2[0]) / 2), ((value[1] + value2[1]) / 2)

	def getAngle(self, coord1, coord2):
		Y = (480 - coord2[1]) - (480 - coord1[1]) # y
		X = coord2[0] - coord1[0] # x
		
		if X == 0:
			if Y == 0:
				return None
		else:
			angle = math.degrees(math.atan(Y / X))

		if X < 0 and Y > 0 :
			return 180 + angle
		elif X < 0 and Y < 0:
			return 180 + angle
		elif X > 0 and Y < 0:
			return 360 + angle
		elif X == 0 and Y < 0:
			return 270
		elif X == 0 and Y >= 0:
			print coord1, coord2
			return 90

		return angle
	
	def refresh(self):
		iterator = 0
		track = self.track
		average = None

		for crumb in xrange(1, len(track)):
			if track[crumb] is None:
				continue

			if not average:
				average = self.track[crumb]
			else:
				average = self.getAverage(average, self.track[crumb])

			iterator += 1
			if (iterator > 2):
				break

		if average:
			if len(self.BallPosAVG) != 3 or (abs(self.BallPosAVG[0][0] - average[0]) > 50 and abs(self.BallPosAVG[0][1] - average[0]) > 50):
				self.BallPosAVG.appendleft(average)

		direction = None
		if len(self.BallPosAVG) == 3:
			direction = self.getAngle(self.BallPosAVG[0], self.BallPosAVG[1])


		self.ball = {
			'position' : average,
			'direction' : direction
		}


	def isAway(self):
		return self.radius < 100;

	def isNear(self):
		return self.radius > 1000;

	def getAxisLeft(self):
		LEFT_X = 0
		LEFT_Y = 0

		print self.ball

		return {
			'LEFT_X' : LEFT_X,
			'LEFT_Y' : LEFT_Y
		}

		if not self.ball:
			LEFT_Y = 0
			LEFT_X = -0.3
		else:
			if self.isAway() :
			#	pass
				LEFT_Y = -0.2
				#print "AWAY"
			elif self.isNear():
			#	pass
				LEFT_Y = 0.2
				#print "NEAR"

			if (self.ball['position'][0]<=-150 or self.ball['position'][0]>=150):
				print "CENTRANDO"
				if(self.ball['position'][0]<0):
					LEFT_Y = 0
					LEFT_X = -0.3
				elif(self.ball['position'][0]>0):
					LEFT_Y = 0
					LEFT_X = 0.04

		return {
			'LEFT_X' : LEFT_X,
			'LEFT_Y' : LEFT_Y
		}


