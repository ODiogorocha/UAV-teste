import cv2
import mediapipe as mp
import time
from camera import open_cam  

# Function to count raised fingers
def count_fingers(landmarks):
    fingers = 0

    # Conditions to detect if fingers are raised (individual fingers)
    if landmarks[4].y < landmarks[3].y:  # Thumb
        fingers += 1
    if landmarks[8].y < landmarks[6].y:  # Index
        fingers += 1
    if landmarks[12].y < landmarks[10].y:  # Middle
        fingers += 1
    if landmarks[16].y < landmarks[14].y:  # Ring
        fingers += 1
    if landmarks[20].y < landmarks[18].y:  # Pinky
        fingers += 1

    return fingers

# Main function to process camera feed
def process_camera():
    camera = open_cam()  # Open the camera using open_cam from camera.py
    if not camera.isOpened():
        print("Error accessing the camera.")
        return

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    mp_drawing = mp.solutions.drawing_utils

    tic = 0
    tac = 0

    while True:
        success, image = camera.read()
        if not success:
            print("Error reading image from camera.")
            break

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Count raised fingers
                fingers = count_fingers(hand_landmarks.landmark)
                cv2.putText(image, f'Fingers: {fingers}', (10, 130), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        # FPS Calculation
        tac = time.time()
        fps = 1 / (tac - tic)
        tic = tac
        cv2.putText(image, f'FPS: {int(fps)}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

        # Show the image
        cv2.imshow("Camera", image)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
            break

    camera.release()
    cv2.destroyAllWindows()

# Call the main function
process_camera()
