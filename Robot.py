from Motor import Motor
from time import time, sleep

class Robot:
  def __init__(self, leftPins, rightPins):
    self.motors = (Motor((leftPins[0],leftPins[1]), leftPins[2]), Motor((rightPins[0], rightPins[1]), rightPins[2]))

  def drive(self, power, duration, brake=False):
    start = duration * 0.2
    basetime = time()
    deltatime = 0
    #slow start
    while deltatime < start:
      self.motors[0].setPower(power[0] * deltatime / start, brake)
      self.motors[1].setPower(power[1] * deltatime / start, brake)
      deltatime = time() - basetime
    #max speed
    while deltatime < duration - start:
      deltatime = time() - basetime
    # slow stop
    basetime = time()
    deltatime = time() - basetime
    while deltatime < start:
      self.motors[0].setPower(power[0] - power[0] * deltatime / start, brake)
      self.motors[1].setPower(power[1] - power[1] * deltatime / start, brake)
      deltatime = time() - basetime
