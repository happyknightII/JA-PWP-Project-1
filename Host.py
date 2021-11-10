from flask import Flask, request
from Robot import Robot

app = Flask(__name__)
robot = Robot()


@app.route('/')
def myapp():
  message = "To use this app: %s/control?command=___&value=___ \n Commands: Forward (positive value forwards, negative backwards, Turn(positive turn to the left, negative turn to the right, or Auto(put in any number to run)" % request.base_url
  return message


@app.route('/control')
def control():
  # Checking that both parameters have been supplied
  if 'command' in request.args:
    if not 'value' in request.args:
      return "value parameter is missing"
  else:
    return "2"

  # Make sure they are numbers too
  command = str(request.args['command'])
  
  if command == "Auto":
    robot.auto()
  else:
    try:
      value = float(request.args['value'])
    except:
      return "value parameter should be a number"
    if command == "Forward":
      robot.forward(value)
    elif command == "Turn":
      robot.turn(value)
    else:
      return "Invalid Command: Try using 'Auto', 'Forward', or 'Turn'"
  return command + " " + str(value)
