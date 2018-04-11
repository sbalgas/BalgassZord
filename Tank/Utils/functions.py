
''' map(val, min, max, toMin, toMax) dado un valor lo escala segun min/max a toMin toMax '''
def map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

''' Limita n en minn y maxn'''
def constrain(n, minn, maxn):
	return max(min(maxn, n), minn)

def angleToPWM(angle, minAngle = 0, maxAngle = 180, minPWM = 1000, maxPWM = 2000):
	return map(constrain(angle, minAngle, maxAngle), minAngle, maxAngle, minPWM, maxPWM)