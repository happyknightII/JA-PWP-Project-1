from flask import Flask, request
from Robot import Robot

app = Flask(__name__)
robot = Robot()


@app.route('/')
def myapp():
  message = "To use this app: http://192.168.1.200:5000//control?command=___&value=___      Commands: Forward (positive value forwards, negative backwards, Turn(positive turn to the left, negative turn to the right, or Auto(put in 0 to run)" % request.base_url

  return message


@app.route('/control')
def control():
  # Checking that command parameter has been supplied
  if 'command' not in request.args:
    return "Try using 'Auto', 'Forward', or 'Turn'"

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
