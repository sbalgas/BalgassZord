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

''' map(val, min, max, toMin, toMax) dado un valor lo escala segun min/max a toMin toMax '''
def map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

''' Limita n en minn y maxn'''
def constrain(n, minn, maxn):
	return max(min(maxn, n), minn)

def angleToPWM(angle, minAngle = 0, maxAngle = 180, minPWM = 1000, maxPWM = 2000):
	return map(constrain(angle, minAngle, maxAngle), minAngle, maxAngle, minPWM, maxPWM)