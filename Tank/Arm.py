from Motor.Bone import Bone

class Arm(object):
	
	def __init__(self, connectMotors = False):

		self.skeleton = {
			'FOOT'	: Bone('FOOT',	4, 0, 180, 90, 1050, 1950, False),
			'Y1'	: Bone('Y1',	17, 0, 180, 90, 1050, 1950, False),
			'Y2'	: Bone('Y2',	27, 0, 180, 90, 1050, 1950, False),
			'Y3'	: Bone('Y3',	27, 0, 180, 90, 1050, 1950, False)
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
		Y = axis.get('LEFT_Y')
		X = axis.get('LEFT_X')

		if (X > 0):
			self.skeleton['FOOT'].incrementAngle()
		elif (X < 0):
			self.skeleton['FOOT'].decreaseAngle()

		if (Y > 0):
			self.skeleton['Y3'].incrementAngle()
		elif (Y < 0):
			self.skeleton['Y3'].decreaseAngle()

arm = Arm(True)

