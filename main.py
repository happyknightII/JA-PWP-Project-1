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
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                endpoints = []
                ret, threshed = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
                # find contours without approx
                cnts = cv2.findContours(threshed, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[-2]

                # get the max-area contour
                cnt = sorted(cnts, key=cv2.contourArea)[-1]

                # calc arclength
                arclen = cv2.arcLength(cnt, True)

                # do approx
                eps = 0.0005
                epsilon = arclen * eps
                approx = cv2.approxPolyDP(cnt, epsilon, True)

                # draw the result
                canvas = img.copy()

                for pt in approx:
                    cv2.circle(canvas, (pt[0][0], pt[0][1]), 7, (0, 255, 0), -1)
                    i = 0
                    n = approx.ravel()
                    for j in n:
                        if i % 2 == 0:
                            x = n[i]
                            y = n[i + 1]

                            # String containing the co-ordinates.
                            string = str(x) + " " + str(y)
                            if i == 0:
                                # text on topmost co-ordinate.
                                cv2.putText(canvas, "Arrow tip", (x, y),
                                            font, 1.0, (255, 0, 0))
                                endpoints.extend([x, y])
                            else:
                                # text on remaining co-ordinates.
                                cv2.putText(canvas, string, (x, y),
                                            font, 0.5, (0, 255, 0))
                        i = i + 1
                cv2.drawContours(canvas, [approx], -1, (0, 0, 255), 2, cv2.LINE_AA)
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
