import io
import sys

from flask import Flask, Response, render_template, request
import cv2
import numpy as np
import time
import json
from Robot import Robot

app = Flask(__name__, template_folder='templates', static_folder='static')

robot = Robot()
piCamera = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_COMPLEX
controlMode = False
settings = {}


def signum(num):
    if num != 0:
        return abs(num) / num
    else:
        return 0


@app.route("/reset")
def load_settings():
    global settings

    with open("settings.json") as settingsFile:
        settings = json.load(settingsFile)
        
    return "Loaded settings"

@app.route("/save")
def save_settings():
    print('Settings saved')
    with open("settings.json", "w") as write_file:
        data = {"maxFrameRate": settings["maxFrameRate"],
                "speed": settings["speed"],
                "kPTurn": settings["kPTurn"],
                "kFTurn": settings["kFTurn"],
                "maxTurnRate": settings["maxTurnRate"],
                "offsetPixels": settings["offsetPixels"],
                "hsvHigh": settings["hsvHigh"],
                "hsvLow": settings["hsvLow"]}
        json.dump(data, write_file, ensure_ascii=False, indent=4)
    return "Saved settings"


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
    robot.strip.turn_off()
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
    def stream(camera):
        global controlMode

        stopFirstTime = 0
        while True:
            ret, img = camera.read()
            leftX = None
            rightX = None
            if ret:
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                row = hsv[100]
                for index in range(img.shape[1]):
                    if settings["hsvLow"][0] < row[index][0] < settings["hsvHigh"][0] \
                            and settings["hsvLow"][1] < row[index][1] < settings["hsvHigh"][1] \
                            and settings["hsvLow"][2] < row[index][2] < settings["hsvHigh"][2]:
                        leftX = index
                        break
                for index in reversed(range(img.shape[1])):
                    if settings["hsvLow"][0] < row[index][0] < settings["hsvHigh"][0] \
                            and settings["hsvLow"][1] < row[index][1] < settings["hsvHigh"][1] \
                            and settings["hsvLow"][2] < row[index][2] < settings["hsvHigh"][2]:
                        rightX = index
                        break
                if leftX is not None and rightX is not None:
                    center = int((leftX + rightX) / 2)
                    cv2.line(img, (leftX, 0), (leftX, img.shape[0]), (255, 192, 203))
                    cv2.line(img, (rightX, 0), (rightX, img.shape[0]), (255, 192, 203))
                    cv2.arrowedLine(img, (center, 100), (center, 200), (0, 255, 0), 5)
                else:
                    center = img.shape[1] / 2
                    rightX = img.shape[1]
                    leftX = 0

                if controlMode:
                    error = center
                    leftrighterror = 600
                    print(abs(rightX - leftX))
                    if leftX < img.shape[1] / 2 and rightX < img.shape[1] / 2:
                        error -= img.shape[1] * 0.1
                        cv2.circle(img, (int(img.shape[1] / 0.1), 100), 100, (255, 255, 255), -1)
                        stopFirstTime = 0
                        print("left turn")
                    elif leftX > img.shape[1] / 2 and rightX > img.shape[1] / 2:
                        cv2.circle(img, (int(img.shape[1] / 0.9), 100), 100, (255, 255, 255), -1)
                        error -= img.shape[1] * 0.9
                        stopFirstTime = 0
                        print("right turn")
                    elif abs(rightX - leftX) < leftrighterror and leftX < img.shape[1] / 2 and rightX < img.shape[1] / 2:
                            if stopFirstTime == 0:
                                stopFirstTime = time.time()
                            elif time.time() - stopFirstTime < settings["offsetPixels"]:
                                controlMode = False
                                stopFirstTime = 0
                            print("stop")

                    else:
                        stopFirstTime = 0
                        error -= img.shape[1] / 2

                    turnRate = settings["kPTurn"] * error + signum(error) * settings["kFTurn"]
                    if abs(turnRate) > settings["maxTurnRate"]:
                        turnRate = signum(turnRate) * settings["maxTurnRate"]
                    elif abs(turnRate) < 1:
                        turnRate = 0
                    if controlMode:
                        robot.enable()
                        robot.drive_raw(-settings["speed"], turnRate)
                    else:
                        robot.stop()


                cv2.line(img, (0, 100), (img.shape[1], 100), (0, 0, 255))

                frame = cv2.imencode('.jpg', img)[1].tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            else:
                break
    return Response(stream(piCamera), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route('/colorPicker')
def color_picker():
    def stream(camera):
        lastTime = time.time()
        while True:
            if time.time() > 1 / settings["maxFrameRate"] + lastTime:
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


@app.route('/threshold')
def threshold():
    def stream(camera):
        lastTime = time.time()
        while True:
            if time.time() > 1/settings["maxFrameRate"] + lastTime:
                lastTime = time.time()
                ret, img = camera.read()
                if ret:
                    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                    HSV_MIN = np.array(settings["hsvLow"], np.uint8)
                    HSV_MAX = np.array(settings["hsvHigh"], np.uint8)

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


@app.route('/getParameters')
def get_parameters():
    def gen():
        yield " ".join(str(e) for e in settings["hsvHigh"]) + " " \
              + " ".join(str(e) for e in settings["hsvLow"]) + \
              f' {settings["kPTurn"]} {settings["kFTurn"]} {settings["maxTurnRate"]} {settings["offsetPixels"]} {settings["speed"]}'
    return Response(gen())


@app.route('/changeParameters')
def change_parameters():
    if 'hh' in request.args:
        settings["hsvHigh"][0] = int(request.args['hh'])
    if 'sh' in request.args:
        settings["hsvHigh"][1] = int(request.args['sh'])
    if 'vh' in request.args:
        settings["hsvHigh"][2] = int(request.args['vh'])

    if 'hl' in request.args:
        settings["hsvLow"][0] = int(request.args['hl'])
    if 'sl' in request.args:
        settings["hsvLow"][1] = int(request.args['sl'])
    if 'vl' in request.args:
        settings["hsvLow"][2] = int(request.args['vl'])

    if 'speed' in request.args:
        settings["speed"] = int(request.args['speed'])
    if 'kp' in request.args:
        settings["kPTurn"] = float(request.args['kp'])
    if 'kf' in request.args:
        settings["kFTurn"] = float(request.args['kf'])
    if 'maxTurn' in request.args:
        settings["maxTurnSpeed"] = int(request.args['maxTurn'])
    if 'offset' in request.args:
        settings["offsetPixels"] = int(request.args['offset'])

    return "arguments saved"


@app.route('/control')
def control():
    global controlMode

    if 'command' not in request.args:
        if 'mode' not in request.args:
            return "Try using 'Auto', 'Forward', or 'Turn'"
        else:
            if request.args['mode'] == "True":
                controlMode = True
                return "Switched to autonomous mode"
            elif request.args['mode'] == "False":
                controlMode = False
                robot.stop()
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


@app.route('/bigAssButton')
def save_settings_page():
    return render_template("saveButton.html")


if __name__ == '__main__':
    load_settings()
    app.run(host="0.0.0.0", port=8000)
