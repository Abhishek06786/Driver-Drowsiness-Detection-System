from flask import Flask, render_template, Response, jsonify
import cv2
import time

from mediapipe_detector import (
    detect_face_mesh,
    get_live_data,
    reset_data
)

app = Flask(__name__)

camera = None
camera_running = False


def generate_frames():

    global camera
    global camera_running

    while True:

        # Camera stopped
        if not camera_running or camera is None:
            time.sleep(0.1)
            continue

        success, frame = camera.read()

        if not success:
            continue

        frame = cv2.flip(frame, 1)

        frame = detect_face_mesh(frame)

        ret, buffer = cv2.imencode(".jpg", frame)

        frame = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'
            + frame +
            b'\r\n'
        )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/video")
def video():

    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )
# ---------------- START CAMERA ----------------

@app.route("/start")
def start():

    global camera
    global camera_running

    if not camera_running:

        camera = cv2.VideoCapture(0)

        if camera.isOpened():
            camera_running = True

    return jsonify({
        "success": True,
        "camera_running": camera_running
    })


# ---------------- STOP CAMERA ----------------

@app.route("/stop")
def stop():

    global camera
    global camera_running

    camera_running = False

    if camera is not None:

        camera.release()
        camera = None

    return jsonify({
        "success": True,
        "camera_running": camera_running
    })


# ---------------- DASHBOARD DATA ----------------

@app.route("/data")
def data():

    return jsonify(get_live_data())


# ---------------- RESET ----------------

@app.route("/reset")
def reset():

    reset_data()

    return jsonify({
        "success": True
    })


# ---------------- MAIN ----------------

if __name__ == "__main__":

    camera = cv2.VideoCapture(0)

    if camera.isOpened():
        camera_running = True

    app.run(
        debug=True,
        threaded=True
    )