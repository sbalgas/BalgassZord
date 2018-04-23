from Servo import Servo
from Utils.functions import angleToPWM

class Bone(Servo):
	"""docstring for Bone"""
	def __init__(self, name, pin, minAngle = 0, maxAngle = 180, angle = 0, minPWM=1000, maxPWM=2000, simulation=True):
		
		self.setAngleLimit(minAngle, maxAngle)
		self.angle = angle

		Servo.__init__(self, name, pin, minPWM, maxPWM, simulation)


	def setAngleLimit(self, minAngle, maxAngle):
		self.minAngle = minAngle
		self.maxAngle = maxAngle


	def incrementAngle(self, angle = 2):
		self.setAngle(self.angle + angle)

	def decreaseAngle(self, angle = 2):
		self.setAngle(self.angle - angle)

	def setAngle(self, angle):

		self.angle = angle;
		self.setW(angleToPWM(self.angle, self.minAngle, self.maxAngle, self.getWMin(), self.getWMax()))

	def start(self):
		super(Bone, self).start()
		
		self.setAngle(self.angle)