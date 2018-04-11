from Tank.Control.Joystick import Joystick
from Tank.Control.OpenCV import OpenCV
from Tank.Caterpillar import Caterpillar

from time import time,sleep

class Tank():

	def __init__(self):
		
		self.cycling = True
		self.cycletime = 0.01
		
		self.__setup()

		self.__baton()

	def __setup(self):
		self.__control = OpenCV()
		self.__caterpillar = Caterpillar(True, 1500, 1420)


	def __baton(self):
		initialTime = time()
		while self.cycling:
			
			self.__loop()

			waitTime = time() - initialTime
			if waitTime < self.cycletime:
				sleep(self.cycletime - waitTime)
			initialTime = time()

	def __loop(self):
		self.__control.refresh()
		axisLeft = self.__control.getAxisLeft()

		print axisLeft

		self.__caterpillar.setDirection(axisLeft)

		return


Tank()