import io
from flask import Flask, request, Response, render_template
from picamera import PiCamera
from Robot import Robot


app = Flask(__name__, template_folder='templates', static_folder='static')
app.debug = True

robot = Robot()


@app.route('/')
def myapp():
    # message = "<p>To use this app: http://192.168.1.200:5000//control?command=___&value=___</p> " \
    #           "<p>Commands: Forward (positive value forwards, negative backwards, Turn(positive turn to the left, negative turn to the right, or Auto(put in 0 to run)</p>"

    return render_template('index.html')


def stream():
   framerate = 15
   buffer = io.BytesIO()
   with PiCamera(framerate=framerate) as camera:
       for frame in camera.capture_continuous(buffer, 'jpeg', use_video_port=True):
          buffer.seek(0)
          buffer.flush()
          yield (b'--frame\r\n'
b'Content-Type: image/jpeg\r\n\r\n' + buffer.getvalue() + b'\r\n')


@app.route('/stream')
def streamer():
        return Response(stream(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route('/control')
def control():
    # Checking that command parameter has been supplied
    if 'command' not in request.args:
        return "Try using 'Auto', 'Forward', or 'Turn'"

    command = str(request.args['command'])

    if command == "Auto":
        robot.auto()
    #elif command == "Light":
        #try:
            #r = int(request.args['R'])
            #g = int(request.args['G'])
            #b = int(request.args['B'])
        #except:
            #return "dude stop it"
        #robot.LEDStrip.colorWiple((r, g, b))

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