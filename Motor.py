import RPi.GPIO as IO
IO.setmode(IO.BCM)

class Motor:
  def __init__(self, pins, ena):
    IO.setup(pins[0],IO.OUT)
    IO.setup(pins[1],IO.OUT)
    IO.setup(ena,IO.OUT)
    self.pins = (IO.PWM(pins[0],100), IO.PWM(pins[1],100))
    self.pins[0].start(0)
    self.pins[1].start(0)
    self.ena = ena
  
  def enable(self, enable = True):
    if enable:
      IO.output(self.ena, IO.HIGH)
    else:
      IO.output(self.ena, IO.LOW)

  def setPower(self, power, brake = False):
    if power > 0:
      self.enable()
      self.pins[0].ChangeDutyCycle(power)
      self.pins[1].ChangeDutyCycle(0)
    else:
      if not power:
        if brake:
          self.enable()
          self.pins[0].ChangeDutyCycle(100)
          self.pins[1].ChangeDutyCycle(100)
        else:
          self.enable(False)
          self.pins[0].ChangeDutyCycle(0)
          self.pins[1].ChangeDutyCycle(0)
      else:
        self.pins[0].ChangeDutyCycle(0)
        self.pins[1].ChangeDutyCycle(-power)

  def __del__(self):
    self.pins[0].ChangeDutyCycle(0)
    self.pins[1].ChangeDutyCycle(0)
    self.pins[0].stop()
    self.pins[1].stop()
    self.enable(False)