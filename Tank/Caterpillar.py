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
from Motor.Servo import Servo
from Utils.functions import map, constrain

from time import time,sleep

class Caterpillar(object):
	
	def __init__(self, connectMotors = False, stillLeft = 1500, stillRight = 1500):

		self.LeftWMin = 1100
		self.RightWMin = 1250

		self.LeftWMax = 1850
		self.RightWMax = 1950

		self.motorLeft	=  Servo('motorLeft',	19, self.LeftWMin, self.LeftWMax, False)
		self.motorRight	=  Servo('motorRight',	16, self.RightWMin, self.RightWMax, False)

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

	def getPWM(self, value, still, minOut, maxOut):

		if value > 0:
			return map(value, 0, 1, still, maxOut)
		else:
			return map(value, -1, 0, minOut, still)


	def setDirection(self, axis):
		Y = axis.get('LEFT_Y') ** 2
		X = axis.get('LEFT_X') / 2

		if (axis.get('LEFT_Y') < 0):
			Y = Y * -1

		if (Y == 0.0 and X == 0.0):
			self.stop()
			return

		limitLeft = self.getPWM(constrain(Y *-1 + X, -1, 1), self.stillLeft, self.LeftWMin, self.LeftWMax)
		limitRight = self.getPWM(constrain(Y + X    , -1, 1), self.stillRight, self.RightWMin, self.RightWMax)

		self.motorLeft.setW( limitLeft)
		self.motorRight.setW(limitRight)
