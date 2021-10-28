from Motor import Motor
from time import time, sleep
#from Light import LEDStrip
import RPi.GPIO as IO

LEFT_PINS = (14, 15, 24)
RIGHT_PINS = (17, 27, 23)
LEFT_BIAS = 20


class Robot:
  def __init__(self, leftPins=LEFT_PINS, rightPins=RIGHT_PINS):
    self.motors = (Motor((leftPins[0], leftPins[1]), leftPins[2]),
                    Motor((rightPins[0], rightPins[1]), rightPins[2]))
    #self.LEDStrip = LEDStrip()

  def drive(self, power, duration, brake=False):
    self.motors[0].enable()
    self.motors[1].enable()
    start = duration * 0.2
    basetime = time()
    deltatime = 0
    self.motors[0].setPower(power[0])
    sleep(0.005)
    self.motors[1].setPower(power[1])
    #slow start
    # while deltatime < start:
    #   self.motors[0].setPower((power[0] - LEFT_BIAS) * deltatime / start + LEFT_BIAS, brake)
    #   self.motors[1].setPower(power[1] * deltatime / start, brake)
    #   deltatime = time() - basetime
    # #max speed
    while deltatime < duration:# - start
      deltatime = time() - basetime
    # # slow stop
    # basetime = time()
    # deltatime = time() - basetime
    #while deltatime < start:
      #self.motors[0].setPower(power[0],brake)
      #self.motors[1].setPower(power[1],brake)
      # self.motors[0].setPower(power[0] - ((power[0] - LEFT_BIAS) * deltatime / start + LEFT_BIAS), brake)
      # self.motors[1].setPower(power[1] - power[1] * deltatime / start,
      #                         brake)
      #deltatime = time() - basetime
      self.motors[0].enable(False)
      self.motors[1].enable(False)


  def pause(self, time1):
    sleep(time1)
  
  def __del__(self):
    del self.motors
    IO.cleanup()
