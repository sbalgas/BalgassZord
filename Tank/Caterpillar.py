from Motor.Servo import Servo
from Utils.functions import map, constrain

class Caterpillar(object):
	
	def __init__(self, connectMotors = False, stillLeft = 1500, stillRight = 1500):

		self.WMin = 1050
		self.WMax = 1950

		self.motorLeft	=  Servo('motorLeft',	19, self.WMin, self.WMax, False)
		self.motorRight	=  Servo('motorRight',	20, self.WMin, self.WMax, False)

		self.stillLeft = stillLeft
		self.stillRight = stillRight

		self.powered = False

		if (connectMotors):
			self.connectMotors()

	def isPowered(self):
		return self.powered

	def connectMotors(self):
		print("Starting motors")
		self.motorLeft.start()
		self.motorRight.start()

		self.stop()

		self.powered = True

	def disconnectMotors(self):
		print("Disconnecting motors")
		self.powered = False
		self.motorLeft.stop()
		self.motorRight.stop()

	def stop(self):
		print("Stopping Motors")
		self.motorLeft.setW(self.stillLeft)
		self.motorRight.setW(self.stillRight)

	def setDirection(self, axis):
		Y = axis.get('LEFT_Y') ** 2
		X = axis.get('LEFT_X') / 2

		if (axis.get('LEFT_Y') < 0):
			Y = Y * -1

		if (Y == 0.0 and X == 0.0):
			self.stop()
			return

		self.motorLeft.setW( map(constrain(Y *-1 + X, -1, 1), -1, 1, self.WMin, self.WMax) )
		self.motorRight.setW(map(constrain(Y + X    , -1, 1), -1, 1, self.WMin, self.WMax) )
		