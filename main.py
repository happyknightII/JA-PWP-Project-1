import io
import sys

from flask import Flask, Response, render_template, request
import cv2
import numpy as np
import time

from Robot import Robot

app = Flask(__name__, template_folder='templates', static_folder='static')

robot = Robot()
piCamera = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_COMPLEX
hsvThresholdLow = [70, 60, 70]
hsvThresholdHigh = [120, 255, 255]
controlMode = False
kPTurn = 0.1
OFFSET_PIXELS = 0
MAX_TURNRATE = 0.3

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
    robot.strip.turnOff()
    robot.indicate()
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
    global controlMode, kPTurn, OFFSET_PIXELS, MAX_TURNRATE

    def stream(camera):
        while True:
            ret, img = camera.read()
            if ret:
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                row = hsv[100]
                for index in range(img.shape[1]):
                    if hsvThresholdLow[0] < row[index][0] < hsvThresholdHigh[0] \
                            and hsvThresholdLow[1] < row[index][1] < hsvThresholdHigh[1] \
                            and hsvThresholdLow[2] < row[index][2] < hsvThresholdHigh[2]:
                        leftX = index
                        break
                for index in reversed(range(img.shape[1])):
                    if hsvThresholdLow[0] < row[index][0] < hsvThresholdHigh[0] \
                            and hsvThresholdLow[1] < row[index][1] < hsvThresholdHigh[1] \
                            and hsvThresholdLow[2] < row[index][2] < hsvThresholdHigh[2]:
                        rightX = index
                        break
                if leftX is not None and rightX is not None:
                    center = int((leftX + rightX) / 2)
                    cv2.line(img, (leftX, 0), (leftX, img.shape[0]), (255, 192, 203))
                    cv2.line(img, (rightX, 0), (rightX, img.shape[0]), (255, 192, 203))
                    cv2.arrowedLine(img, (center, 100), (center, 200), (0, 255, 0), 5)

                    if controlMode:
                        turnRate = kPTurn * (center - img.shape[1] / 2 + OFFSET_PIXELS)
                        if abs(turnRate) > MAX_TURNRATE:
                            turnRate = abs(turnRate) / turnRate * MAX_TURNRATE
                        elif abs(turnRate) < 0.5:
                            turnRate = 0
                        robot.enable()
                        robot.driveRaw(0.2, turnRate)
                    del leftX
                    del rightX
                cv2.line(img, (0, 100), (img.shape[1], 100), (0, 0, 255))

                frame = cv2.imencode('.jpg', img)[1].tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            else:
                break
    return Response(stream(piCamera), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route('/tuning/getrgb')
def tuning():
    def stream(camera):
        while True:
            ret, img = camera.read()
            if ret:
                cropped_image = img[int(img.shape[0]/2) - 15:int(img.shape[0]/2 + 15), int(img.shape[1]/2) - 15:int(img.shape[1]/2) + 15]
                hsv = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2HSV)
                rgb_average = np.average(cropped_image, axis=(0, 1))
                average = np.average(hsv, axis=(0, 1))

                cv2.line(img, (int(img.shape[1]/2), 0), (int(img.shape[1]/2), int(img.shape[0])), (255, 255, 255), 1)
                cv2.line(img, (0, int(img.shape[0]/2)), (int(img.shape[1]), int(img.shape[0]/2)), (255, 255, 255), 1)
                cv2.circle(img, (int(img.shape[1]/2), int(img.shape[0]/2)), 20, (255, 255, 255), 1)
                cv2.circle(img, (int(img.shape[1]/2), int(img.shape[0]/2)), 10, rgb_average, -1)
                cv2.putText(img, f"{average}", (10, 200), cv2.FONT_HERSHEY_COMPLEX,  0.5, (255, 255, 255), 1)
                frame = cv2.imencode('.jpg', img)[1].tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            else:
                break
    return Response(stream(piCamera), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route('/tuning/')
def create():
    return render_template('tuning.html')


@app.route('/tuning/threshold')
def threshold():
    def stream(camera):
        lastTime = time.time()
        while True:
            if time.time() > 0.1 + lastTime:
                lastTime = time.time()
                ret, img = camera.read()
                if ret:
                    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                    HSV_MIN = np.array(hsvThresholdLow, np.uint8)
                    HSV_MAX = np.array(hsvThresholdHigh, np.uint8)

                    frame_threshed = cv2.inRange(hsv, HSV_MIN, HSV_MAX)

                    frame = cv2.imencode('.jpg', frame_threshed)[1].tobytes()
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


@app.route('/thresholdparameters')
def thresholdparameters():
    global hsvThresholdLow
    global hsvThresholdHigh
    if 'hh' not in request.args or 'vh' not in request.args or 'sh' not in request.args or 'hl' not in request.args or 'vl' not in request.args or 'sl' not in request.args:
        return "missing arguments"
    hsvThresholdLow = [int(request.args['hl']), int(request.args['sl']), int(request.args['vl'])]
    hsvThresholdHigh = [int(request.args['hh']), int(request.args['sh']), int(request.args['vh'])]

    return "arguments saved"


@app.route('/control')
def control():
    global controlMode
    if 'command' not in request.args:
        if 'mode' not in request.args:
            return "Try using 'Auto', 'Forward', or 'Turn'"
        else:
            if request.args['value'] == "True":
                controlMode = True
                return "Switched to autonomous mode"
            elif request.args['value'] == "False":
                controlMode = False
                return "Switched to manual mode"
    else:
        if not controlMode:
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
        else:
            return "Autonomous mode"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
