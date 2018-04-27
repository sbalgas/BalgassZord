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

from ctypes import *
import cv2
import math
import random


from time import time,sleep

class BOX(Structure):
	_fields_ = [("x", c_float),
				("y", c_float),
				("w", c_float),
				("h", c_float)]

class DETECTION(Structure):
	_fields_ = [("bbox", BOX),
				("classes", c_int),
				("prob", POINTER(c_float)),
				("mask", POINTER(c_float)),
				("objectness", c_float),
				("sort_class", c_int)]


class IMAGE(Structure):
	_fields_ = [("w", c_int),
				("h", c_int),
				("c", c_int),
				("data", POINTER(c_float))]

class METADATA(Structure):
	_fields_ = [("classes", c_int),
				("names", POINTER(c_char_p))]


class Yolo(object):
	
	def __init__(self):
		self.lib = CDLL("YoloData/libdarknet.so", RTLD_GLOBAL)
		self.lib.network_width.argtypes = [c_void_p]
		self.lib.network_width.restype = c_int
		self.lib.network_height.argtypes = [c_void_p]
		self.lib.network_height.restype = c_int

		self.predict = self.lib.network_predict
		self.predict.argtypes = [c_void_p, POINTER(c_float)]
		self.predict.restype = POINTER(c_float)

		self.set_gpu = self.lib.cuda_set_device
		self.set_gpu.argtypes = [c_int]

		self.make_image = self.lib.make_image
		self.make_image.argtypes = [c_int, c_int, c_int]
		self.make_image.restype = IMAGE

		self.get_network_boxes = self.lib.get_network_boxes
		self.get_network_boxes.argtypes = [c_void_p, c_int, c_int, c_float, c_float, POINTER(c_int), c_int, POINTER(c_int)]
		self.get_network_boxes.restype = POINTER(DETECTION)

		self.make_network_boxes = self.lib.make_network_boxes
		self.make_network_boxes.argtypes = [c_void_p]
		self.make_network_boxes.restype = POINTER(DETECTION)

		self.free_detections = self.lib.free_detections
		self.free_detections.argtypes = [POINTER(DETECTION), c_int]

		self.free_ptrs = self.lib.free_ptrs
		self.free_ptrs.argtypes = [POINTER(c_void_p), c_int]

		self.network_predict = self.lib.network_predict
		self.network_predict.argtypes = [c_void_p, POINTER(c_float)]

		self.reset_rnn = self.lib.reset_rnn
		self.reset_rnn.argtypes = [c_void_p]

		load_net = self.lib.load_network
		load_net.argtypes = [c_char_p, c_char_p, c_int]
		load_net.restype = c_void_p

		self.do_nms_obj = self.lib.do_nms_obj
		self.do_nms_obj.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

		self.do_nms_sort = self.lib.do_nms_sort
		self.do_nms_sort.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

		self.free_image = self.lib.free_image
		self.free_image.argtypes = [IMAGE]

		self.letterbox_image = self.lib.letterbox_image
		self.letterbox_image.argtypes = [IMAGE, c_int, c_int]
		self.letterbox_image.restype = IMAGE

		load_meta = self.lib.get_metadata
		self.lib.get_metadata.argtypes = [c_char_p]
		self.lib.get_metadata.restype = METADATA

		self.load_image = self.lib.load_image_color
		self.load_image.argtypes = [c_char_p, c_int, c_int]
		self.load_image.restype = IMAGE

		self.rgbgr_image = self.lib.rgbgr_image
		self.rgbgr_image.argtypes = [IMAGE]

		self.predict_image = self.lib.network_predict_image
		self.predict_image.argtypes = [c_void_p, IMAGE]
		self.predict_image.restype = POINTER(c_float) 

		self.net = load_net("YoloData/yolov2-tiny.cfg", "YoloData/yolov2-tiny.weights", 0)
		self.meta = load_meta("YoloData/coco.data")

		self.cam = cv2.VideoCapture(0)  # 0 -> index of camera
	
	def c_array(self, ctype, values):
		arr = (ctype*len(values))()
		arr[:] = values
		return arr
		
	def classify(self, im):
		out = self.predict_image(self.net, im)
		res = []
		for i in range(self.meta.classes):
			res.append((self.meta.names[i], out[i]))

		res = sorted(res, key=lambda x: -x[1])
		return res

	def detect(self, im, thresh=.5, hier_thresh=.5, nms=.45):
		num = c_int(0)
		pnum = pointer(num)
		self.predict_image(self.net, im)
		dets = self.get_network_boxes(self.net, im.w, im.h, thresh, hier_thresh, None, 0, pnum)
		num = pnum[0]
		if (nms): self.do_nms_obj(dets, num, self.meta.classes, nms);

		res = []
		for j in range(num):
			for i in range(self.meta.classes):
				if dets[j].prob[i] > 0:
					b = dets[j].bbox
					res.append({
						"object" : self.meta.names[i], 
						"probability" : dets[j].prob[i], 
						"position" : (b.x, b.y),
						"center" : (b.x - im.w/2, b.y - im.h/2),
						"size" : (b.w, b.h),
						"imageSize" : (im.w, im.h)
					})

		self.free_detections(dets, num)
		return res

	def findObject(self, objectToFind = ""):
		im = self.getPicture()

		for anObject in self.detect(im):
			#if (anObject['object'] == objectToFind):
			return anObject;

		return False;

	def getPicture(self):
		s, img = self.cam.read()
		if not s: 
			print "NO IMAGE"
			return
			
		#cv2.imshow('my webcam', img)
		cv2.waitKey(1)

		return self.array_to_image(img)

	def array_to_image(self, arr):
		arr = arr.transpose(2,0,1)
		c = arr.shape[0]
		h = arr.shape[1]
		w = arr.shape[2]
		arr = (arr/255.0).flatten()
		data = self.c_array(c_float, arr)
		im = IMAGE(w,h,c,data)
		return im
		
	def refresh(self):
		pass;

	def getAxisLeft(self):
		X = 0
		Y = 0

		objectFinded = self.findObject("car");
		print objectFinded
		if (objectFinded):

			
			if (objectFinded['center'][0] > 10):
				X = 0.5
			elif (objectFinded['center'][0] < 10):
				X = -0.5

			
			percentW = objectFinded['size'][0] * 100 / objectFinded['imageSize'][0]
			print percentW
			if (percentW < 50):
				Y = 0.5
			elif (percentW > 60):
				Y = -0.5


		return {
			'LEFT_X' : X,
			'LEFT_Y' : Y
		}
