import cv2
import mediapipe as mp
from ear import eye_aspect_ratio
from mar import mouth_aspect_ratio
from alarm import play_alarm, stop_alarm

# -------- Live Dashboard Data --------
LIVE_DATA = {
    "status": "Awake",
    "ear": 0.0,
    "mar": 0.0,
    "blinks": 0,
    "yawns": 0
}

# -------- MediaPipe Face Mesh --------
mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# -------- Eye Landmark Indexes --------
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

# -------- Mouth Landmark Indexes --------
MOUTH = [61, 291, 13, 14]

# -------- Drowsiness Settings --------
COUNTER = 0
EAR_THRESHOLD = 0.22
CLOSED_FRAMES = 20

# -------- Blink Settings --------
BLINK_COUNT = 0
BLINK_FLAG = False

# -------- Yawning Settings --------
YAWN_COUNT = 0
YAWN_COUNTER = 0
MAR_THRESHOLD = 0.60
YAWN_FRAMES = 15


def detect_face_mesh(frame):

    global COUNTER
    global BLINK_COUNT
    global BLINK_FLAG
    global YAWN_COUNT
    global YAWN_COUNTER

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:

        h, w, _ = frame.shape

        for face_landmarks in results.multi_face_landmarks:

            left_eye = []
            right_eye = []
            mouth = []

            # Left Eye
            for idx in LEFT_EYE:
                x = int(face_landmarks.landmark[idx].x * w)
                y = int(face_landmarks.landmark[idx].y * h)
                left_eye.append((x, y))
                cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

            # Right Eye
            for idx in RIGHT_EYE:
                x = int(face_landmarks.landmark[idx].x * w)
                y = int(face_landmarks.landmark[idx].y * h)
                right_eye.append((x, y))
                cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

            # Mouth
            for idx in MOUTH:
                x = int(face_landmarks.landmark[idx].x * w)
                y = int(face_landmarks.landmark[idx].y * h)
                mouth.append((x, y))
                cv2.circle(frame, (x, y), 3, (255, 0, 0), -1)

            # EAR
            leftEAR = eye_aspect_ratio(left_eye)
            rightEAR = eye_aspect_ratio(right_eye)
            ear = (leftEAR + rightEAR) / 2.0

            # MAR
            mar = mouth_aspect_ratio(mouth)

            # Live Dashboard Update
            LIVE_DATA["ear"] = round(ear, 2)
            LIVE_DATA["mar"] = round(mar, 2)
            LIVE_DATA["blinks"] = BLINK_COUNT
            LIVE_DATA["yawns"] = YAWN_COUNT

            cv2.putText(frame,f"EAR : {ear:.2f}",(20,40),
                        cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)

            cv2.putText(frame,f"MAR : {mar:.2f}",(20,200),
                        cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)

            cv2.putText(frame,f"Blinks : {BLINK_COUNT}",(20,170),
                        cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,0),2)

            cv2.putText(frame,f"Yawns : {YAWN_COUNT}",(20,270),
                        cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,0),2)

            # -------- Yawning Detection --------
            if mar > MAR_THRESHOLD:

                YAWN_COUNTER += 1

                cv2.putText(frame,"Yawning",(20,240),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8,(0,0,255),2)

            else:

                if YAWN_COUNTER >= YAWN_FRAMES:
                    YAWN_COUNT += 1

                YAWN_COUNTER = 0

            # -------- Eye Detection --------
            if ear < EAR_THRESHOLD:

                LIVE_DATA["status"] = "Eyes Closed"

                COUNTER += 1
                BLINK_FLAG = True

                cv2.putText(
                    frame,
                    "Eyes Closed",
                    (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2
                )

                # Alarm Start
                if COUNTER == CLOSED_FRAMES:
                    play_alarm()

                if COUNTER >= CLOSED_FRAMES:

                    LIVE_DATA["status"] = "Drowsy"

                    cv2.putText(
                        frame,
                        "DROWSINESS ALERT!",
                        (20, 130),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        3
                    )

            else:

                LIVE_DATA["status"] = "Awake"

                # Blink Count
                if BLINK_FLAG:
                    BLINK_COUNT += 1
                    BLINK_FLAG = False

                COUNTER = 0
                stop_alarm()

                cv2.putText(
                    frame,
                    "Awake",
                    (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

    else:

        COUNTER = 0
        stop_alarm()
        YAWN_COUNTER = 0
        BLINK_FLAG = False

        LIVE_DATA["status"] = "No Face"

    return frame


def get_live_data():
    return LIVE_DATA


def reset_data():
    global COUNTER
    global BLINK_COUNT
    global BLINK_FLAG
    global YAWN_COUNT
    global YAWN_COUNTER

    COUNTER = 0
    BLINK_COUNT = 0
    BLINK_FLAG = False
    YAWN_COUNT = 0
    YAWN_COUNTER = 0

    stop_alarm()

    LIVE_DATA["status"] = "Awake"
    LIVE_DATA["ear"] = 0.0
    LIVE_DATA["mar"] = 0.0
    LIVE_DATA["blinks"] = 0
    LIVE_DATA["yawns"] = 0

            