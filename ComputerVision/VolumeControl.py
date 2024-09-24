import cv2
import mediapipe as mp
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Initialize MediaPipe hands model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize PyCaw for volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volume_range = volume.GetVolumeRange()  # Get volume range (-65.25, 0.0)
min_vol, max_vol = volume_range[0], volume_range[1]

# Start capturing video
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame for natural gesture view and convert BGR to RGB
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hand landmarks
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw landmarks and connections on the frame
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Extracting coordinates of the thumb and index finger
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            h, w, _ = frame.shape
            thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)
            index_x, index_y = int(index_tip.x * w), int(index_tip.y * h)

            # Draw circles on the thumb and index finger tips
            cv2.circle(frame, (thumb_x, thumb_y), 10, (0, 255, 0), cv2.FILLED)
            cv2.circle(frame, (index_x, index_y), 10, (0, 255, 0), cv2.FILLED)

            # Draw a line between the thumb and index finger
            cv2.line(frame, (thumb_x, thumb_y), (index_x, index_y), (255, 0, 0), 3)

            # Calculate the distance between the thumb and index finger
            distance = np.sqrt((index_x - thumb_x)**2 + (index_y - thumb_y)**2)

            # Map the distance to the system volume range
            vol = np.interp(distance, [30, 200], [min_vol, max_vol])
            volume.SetMasterVolumeLevel(vol, None)

            # Display the volume level on the screen
            vol_percent = np.interp(distance, [30, 200], [0, 100])
            cv2.putText(frame, f'Volume: {int(vol_percent)}%', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Show the processed frame
    cv2.imshow('Volume Control', frame)

    # Break the loop on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
