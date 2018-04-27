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

	def getWMin(self):
		return self.__WMin

	def getWMax(self):
		return self.__WMax

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

