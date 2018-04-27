from Motor.Bone import Bone

from time import time,sleep


class Arm(object):
	
	def __init__(self, connectMotors = False):

		self.skeleton = {
			'FOOT'	: Bone('FOOT',	4, 0, 180, 60, 1050, 1950, False),
			'Y1'	: Bone('Y1',	17, 40, 150, 150, 1050, 1950, False),
			'Y2'	: Bone('Y2',	27, 0, 180, 0, 1050, 1950, False),
			'Y3'	: Bone('Y3',	18, 0, 180, 90, 1050, 1950, False)
		}
		
		self.powered = False

		if (connectMotors):
			self.connectMotors()


	def isPowered(self):
		return self.powered

	def connectMotors(self):
		print("Starting motors")

		for bone in self.skeleton:
			self.skeleton[bone].start()

		self.powered = True

	def disconnectMotors(self):
		print("Disconnecting motors")

		self.powered = False
		for bone in self.skeleton:
			self.skeleton[bone].stop()

	def setDirection(self, axis):
		X = axis.get('RIGHT_X')
		Y = axis.get('RIGHT_Y')

		if (X < 0):
			self.skeleton['FOOT'].incrementAngle(5)
		elif (X > 0):
			self.skeleton['FOOT'].decreaseAngle(5)

		if (Y < 0):
			self.skeleton['Y1'].decreaseAngle(3)
			self.skeleton['Y2'].incrementAngle(5)
		elif (Y > 0):
			self.skeleton['Y1'].incrementAngle(3)
			self.skeleton['Y2'].decreaseAngle(5)

