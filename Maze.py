def maze(robot):
	x = 0.4
	y = -1.85
	robot.drive((74.46+x, 68.2+y), 2.97)
	robot.pause(1)
	robot.drive((50+x, 0), 1.33)
	robot.pause(1)
	robot.drive((74.46+x, 68.2+y), 3.5)
	robot.pause(1)
	robot.drive((-64, -68.2), 1.3)
	robot.pause(1)
	robot.drive((50+x, 0), 1.33)
	robot.pause(1)
	robot.drive((74.46+x, 68.2+y), 3)