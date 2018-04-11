from Motor.Servo import Servo
from Utils.functions import map, constrain

class Arm(object):
	
	def __init__(self, connectMotors = False):

		self.minPWM = 1050
		self.maxPWM = 1950

		self.maxAngle = 180
		self.minAngle = 0

		self.servo {
			'FOOT' : Servo('servoFoot',	19, self.minPWM, self.maxPWM, False)
		}
		
		self.powered = False

		if (connectMotors):
			self.connectMotors()


	def isPowered(self):
		return self.powered

	def connectMotors(self):
		print("Starting motors")

		for oneServo in self.servo:
			self.oneServo.start()

		self.powered = True

	def disconnectMotors(self):
		print("Disconnecting motors")

		self.powered = False
		or oneServo in self.servo:
			self.oneServo.stop()

	def setFootAngle(self, angle):
		
		self.servoFoot.setW(angleToPWM(angle, self.minAngle, self.maxAngle, self.minPWM, self.maxPWM))
		