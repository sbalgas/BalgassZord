
class Servo(object):
	def __init__(self, name, pin, WMin=1000, WMax=2000, simulation=True):
		self.name = name
		self.powered = False
		self.simulation = simulation
		self.__pin = pin
		self.setWLimits(WMin, WMax)

		self.__W = self.__WMin

	def setWLimits(self, WMin, WMax):
		self.__WMin = WMin
		self.__WMax = WMax

	def start(self):
		if not self.simulation:
			try:
				from RPIO import PWM
				self.__IO = PWM.Servo()
				self.powered = True
				print "Motor ", self.name, " Started"
				self.setW(self.__WMin)
			except ImportError:
				print "MOTOR ERROR ", self.name
				self.simulation = True
				self.powered = False

		if self.simulation:
			print "SIMULATION MODE FOR ", self.name

	def stop(self):
		self.setW(1000)
		if self.powered:
			self.__IO.stop_servo(self.__pin)
			self.powered = False

	def increaseW(self, step=10):
		self.setW(self.__W + int(step))

	def decreaseW(self, step=10):
		self.setW(self.__W - int(step))

	def setW(self, W):

		W = int(round(float(W) / 10)) * 10
		if W < self.__WMin:
			W = self.__WMin
		if W > self.__WMax:
			W = self.__WMax

		if (self.simulation):
			self.__W = W
			print self.name, self.__W

		if (W != self.__W and self.powered):
			self.__W = W
			self.__IO.set_servo(self.__pin, self.__W)

