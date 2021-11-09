from flask import Flask, request
from Move.Forward import forward
from Move.Turn import turn
from Move.Maze import maze
from Robot import Robot
app = Flask(__name__)
robot = Robot()
@app.route('/')
def myapp():
	message = "To use this app: %s/add?command=___&value=___" % request.base_url
	return message

@app.route('/add')
def add():
	# Checking that both parameters have been supplied
	if 'command' in request.args:
		if not 'value' in request.args:
			return "value parameter is missing"
	else:
		return "2"

	# Make sure they are numbers too
	command = str(request.args['command'])
	try:
		value = float(request.args['time'])
	except:
		return "value parameter should be a number"
	if command =="Maze":
		maze(Robot)
	elif command == "Forward":
		forward(robot, value)
	elif command == "Turn":
		turn(robot, value)
	else:
		return "Invalid Command: Try using 'Maze', 'Forward', or 'Turn'"
	return command + " " + str(value)
