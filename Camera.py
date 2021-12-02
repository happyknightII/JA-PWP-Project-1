from picamera import PiCamera

with PiCamera as camera:
	camera.capture("capture.jpg")