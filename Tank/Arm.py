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

