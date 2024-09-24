import cv2
import mediapipe as mp
import random
import time

# Initialize MediaPipe Hands model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize gesture recognition threshold values for Rock, Paper, Scissors
def get_gesture(hand_landmarks):
    # Coordinates of important landmarks
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    index_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
    middle_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
    ring_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]
    pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]

    # Gesture Logic:
    # Check if all fingers (except the thumb) are extended for "Paper"
    if (index_tip.y < index_mcp.y and middle_tip.y < middle_mcp.y and
        ring_tip.y < ring_mcp.y and pinky_tip.y < pinky_mcp.y):
        return "Paper"
    
    # Check if only index and middle fingers are extended for "Scissors"
    elif (index_tip.y < index_mcp.y and middle_tip.y < middle_mcp.y and
          ring_tip.y > ring_mcp.y and pinky_tip.y > pinky_mcp.y):
        return "Scissors"
    
    # Check if all fingers are bent (above the MCP joint) for "Rock"
    elif (index_tip.y > index_mcp.y and middle_tip.y > middle_mcp.y and
          ring_tip.y > ring_mcp.y and pinky_tip.y > pinky_mcp.y):
        return "Rock"
    
    # Default return if no gesture is detected
    return ""


# Function to get the computer's choice
def computer_choice():
    return random.choice(["Rock", "Paper", "Scissors"])

# Function to determine the winner
def determine_winner(user, computer):
    if user == computer:
        return "Draw"
    elif (user == "Rock" and computer == "Scissors") or \
         (user == "Paper" and computer == "Rock") or \
         (user == "Scissors" and computer == "Paper"):
        return "User Wins!"
    else:
        return "Computer Wins!"

# Start capturing video
cap = cv2.VideoCapture(0)
start_time = time.time()
game_duration = 5  # Play every 5 seconds
game_result = ""

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip and convert the frame for natural view
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hand landmarks
    results = hands.process(rgb_frame)

    user_gesture = ""
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw landmarks on the hand
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            user_gesture = get_gesture(hand_landmarks)

    # Display game status
    cv2.putText(frame, f"User Gesture: {user_gesture}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # If the game duration has passed, play a round
    if time.time() - start_time > game_duration:
        if user_gesture:  # Only proceed if the user has shown a gesture
            computer_move = computer_choice()
            game_result = determine_winner(user_gesture, computer_move)
            start_time = time.time()

    # Display computer's choice and the game result
    if game_result:
        cv2.putText(frame, f"Computer: {computer_move}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Result: {game_result}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Show the frame
    cv2.imshow('Rock-Paper-Scissors', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
