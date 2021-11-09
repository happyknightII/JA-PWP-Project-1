def forward(robot, feet):
	x = 0.4
	y = -1.85
	if feet > 0:
		robot.drive((74.46+x, 68.2+y), 0.75 * feet)
	elif feet < 0:
		robot.drive((-64, -68.2), 1 * feet)