import pygame
from os import environ
from pygame.locals import QUIT, JOYBUTTONUP, JOYBUTTONDOWN, \
	JOYAXISMOTION, JOYHATMOTION
	
class Joystick(object):
	
	JOYSTICKS = []

	AXIS_IDS = {
		'LEFT_X': 0,
		'LEFT_Y': 1,
		'RIGHT_X': 2,
		'RIGHT_Y': 3,
		'RIGHT_TRIGGER': 4,
		'LEFT_TRIGGER': 5,
		'D_PAD_X': 6,
		'D_PAD_Y': 7,
	}

	BUTTON_IDS = {
		'A': 0,
		'B': 1,
		'X': 2,
		'Y': 3,
		'L_BUMPER': 4,
		'R_BUMPER': 5,
		'BACK': 6,
		'START': 7,
		'GUIDE': 8,
		'L_STICK': 9,
		'R_STICK': 10,
	}

	AXIS_NAMES = dict([(idn, name) for name, idn in AXIS_IDS.items()])

	def __init__(self):
		# Don't use drivers we don't need
		environ["SDL_VIDEODRIVER"] = "dummy"
		environ["SDL_AUDIODRIVER"] = "dummy"
		pygame.init()

		clock = pygame.time.Clock()
		for i in range(0, pygame.joystick.get_count()):
			self.JOYSTICKS.append(pygame.joystick.Joystick(i))
			self.JOYSTICKS[-1].init()
			print("Detected joystick '%s'" % self.JOYSTICKS[-1].get_name())

	def refresh(self):
		pygame.event.get()

	def getAxisLeft(self):
		X = 0
		Y = 0
		if (len(self.JOYSTICKS)):
			joystick = self.JOYSTICKS[-1]
			X = round(joystick.get_axis(self.AXIS_IDS.get('LEFT_X')), 3)
			Y = round(joystick.get_axis(self.AXIS_IDS.get('LEFT_Y')), 3)
		
		return {
			'LEFT_X' : X,
			'LEFT_Y' : Y
		}


	def getAxisRight(self):
		X = 0
		Y = 0
		if (len(self.JOYSTICKS)):
			joystick = self.JOYSTICKS[-1]
			X = round(joystick.get_axis(self.AXIS_IDS.get('RIGHT_X')), 3)
			Y = round(joystick.get_axis(self.AXIS_IDS.get('RIGHT_Y')), 3)
		
		return {
			'RIGHT_X' : X,
			'RIGHT_Y' : Y
		}