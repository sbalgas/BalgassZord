'''
This file is part of BalgassZord.

    BalgassZord is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    BalgassZord is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with BalgassZord.  If not, see <http://www.gnu.org/licenses/>.
'''

from Tank.Control.Joystick import Joystick
from Tank.Control.OpenCVClassifier import OpenCVClassifier
from Tank.Caterpillar import Caterpillar
from Tank.Arm import Arm

from time import time,sleep

class Tank():

	def __init__(self):
		
		self.cycling = True
		self.cycletime = 0.2
		
		self.__setup()

		self.__baton()

	def __setup(self):
		self.__control = OpenCVClassifier()
		self.__caterpillar = Caterpillar(True)
		self.__arm = Arm(True)

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
		axisRight = self.__control.getAxisRight()

		print axisRight

		self.__caterpillar.setDirection(axisLeft)
		self.__arm.setDirection(axisRight)

		return


Tank()