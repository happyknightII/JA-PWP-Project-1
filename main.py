import io
import sys

from flask import Flask, Response, render_template, request
import cv2
import numpy as np

from Robot import Robot

app = Flask(__name__, template_folder='templates', static_folder='static')

robot = Robot()
piCamera = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_COMPLEX


class Logger:
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush()  # If you want the output to be visible immediately

    def flush(self):
        for f in self.files:
            f.flush()


log = io.StringIO()  # buffer

sys.stdout = Logger(sys.stdout, log)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/stream')
def streamer():
    def stream(camera):
        while True:
            ret, img = camera.read()
            if ret:
                frame = cv2.imencode('.jpg', img)[1].tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            else:
                break
    return Response(stream(piCamera), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route('/annotation')
def annotation():
    def stream(camera):
        while True:
            ret, img = camera.read()
            if ret:
                row = img[100]
                for index in range(img.shape[0]):
                    if row[index][0] > 100:
                        cv2.circle(img, (index, 100), 10, (255, 255, 255), -1)
                frame = cv2.imencode('.jpg', img)[1].tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            else:
                break
    return Response(stream(piCamera), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route('/logpage')
def log_page():
    def gen():
        log.seek(0)
        log_list = log.readlines()
        yield "<br>".join(log_list[-100:])
    return Response(gen())


@app.route('/control')
def control():
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
    print(command + " " + str(value))
    return command + " " + str(value)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
