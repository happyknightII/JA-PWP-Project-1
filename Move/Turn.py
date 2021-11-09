def turn(robot, degrees):
	x = 0.4
	y = -1.85
	if degrees > 0:
		robot.drive((50+x, 0), 1.33 * degrees/90)
	elif degrees < 0:
		robot.drive((0, 43.74+y), 1.33 * degrees/90)
	