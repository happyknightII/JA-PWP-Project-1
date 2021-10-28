from Robot import Robot

#IO.setwarnings(False)
robot = Robot()
x = 0.7
y = -1
robot.drive((74.46+x, 68.2+y), 2.9)
robot.pause(1)
robot.drive((50+x, 0), 1.35)
robot.pause(1)
robot.drive((74.46+x, 68.2+y), 3.5)
robot.pause(1)
robot.drive((-66, -68.2), 1.3)
robot.pause(1)
robot.drive((50+x, 0), 1.35)
robot.pause(1)
robot.drive((74.46+x, 68.2+y), 3)