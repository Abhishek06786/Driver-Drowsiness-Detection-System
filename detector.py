import cv2

# Face Detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Eye Detector
eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye.xml"
)

closed_eye_count = 0

def detect_drowsiness(frame):

    global closed_eye_count

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:

        # Face Rectangle
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        eyes = eye_cascade.detectMultiScale(roi_gray)

        # Eyes Open
        if len(eyes) > 0:

            closed_eye_count = 0

            cv2.putText(frame,
                        "AWAKE",
                        (20,40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0,255,0),
                        2)

            for (ex, ey, ew, eh) in eyes:

                cv2.rectangle(
                    roi_color,
                    (ex, ey),
                    (ex+ew, ey+eh),
                    (255,0,0),
                    2
                )

        # Eyes Closed
        else:

            closed_eye_count += 1

            cv2.putText(frame,
                        "Eyes Closed",
                        (20,40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0,0,255),
                        2)

            if closed_eye_count > 20:

                cv2.putText(frame,
                            "DROWSINESS ALERT!",
                            (20,80),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0,0,255),
                            3)

    return frame