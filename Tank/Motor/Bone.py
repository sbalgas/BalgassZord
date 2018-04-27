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

from Servo import Servo
from Tank.Utils.functions import angleToPWM

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
		if (angle < self.minAngle):
			angle = self.minAngle
		if (angle > self.maxAngle):
			angle =  self.maxAngle

		self.angle = angle;
		print self.name, self.angle
		self.setW(angleToPWM(self.angle, 0, 180, self.getWMin(), self.getWMax()))

	def start(self):
		print "Starting ", self.name
		super(Bone, self).start()
		
		self.setAngle(self.angle)