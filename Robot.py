from Motor import Motor
from time import time, sleep
#import math
#from Light import LEDStrip
import RPi.GPIO as IO

LEFT_PINS = (14, 15, 24)
RIGHT_PINS = (17, 27, 23)

class Robot:
	def __init__(self, leftPins=LEFT_PINS, rightPins=RIGHT_PINS):
		self.motors = (Motor((leftPins[0], leftPins[1]), leftPins[2]), Motor((rightPins[0], rightPins[1]), rightPins[2]))
		#self.LEDStrip = LEDStrip()

	def drive(self, power, duration, brake=False):
		self.motors[0].enable()
		self.motors[1].enable()
		#start = 1.4
		basetime = time()
		deltatime = 0
		while deltatime < duration:
			self.motors[0].setPower(power[0])
			self.motors[1].setPower(power[1])
			deltatime = time() - basetime
		# while deltatime < duration / 2:
		# 	deltatime = time() - basetime
		# 	sig = 1 - 1 / (1 + math.exp(deltatime - start))
		# 	self.motors[0].setPower(power[0] * sig)
		# 	self.motors[1].setPower(power[1] * sig)

		# while deltatime < duration:
		# 	deltatime = time() - basetime
		# 	sig = 1 / (1 + math.exp(deltatime - start - duration))
		# 	self.motors[0].setPower(power[0] * sig)
		# 	self.motors[1].setPower(power[1] * sig)
		self.motors[0].setPower(0)
		self.motors[1].setPower(0)


	def pause(self, time1):
		sleep(time1)
  
	def __del__(self):
		del self.motors
		IO.cleanup()
