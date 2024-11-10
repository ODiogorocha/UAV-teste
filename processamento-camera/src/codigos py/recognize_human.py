import cv2
import mediapipe as mp
from camera import open_cam  # Assuming open_cam is in camera.py

# Initialize mediapipe for pose detection
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Function to draw a box around the detected person
def draw_person_box(image, landmarks):
    height, width, _ = image.shape

    # Get the x and y coordinates of the body points
    x_min = int(min(landmark.x for landmark in landmarks) * width)
    x_max = int(max(landmark.x for landmark in landmarks) * width)
    y_min = int(min(landmark.y for landmark in landmarks) * height)
    y_max = int(max(landmark.y for landmark in landmarks) * height)

    # Draw the box around the detected person
    cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)  # Green color (BGR)

# Function to process the camera feed and detect human poses
def process_camera():
    camera = open_cam() 
    print("Processing human detection...")

    while True:
        ret, frame = camera.read()
        if not ret:
            print("Error accessing the camera feed.")
            break

        # Convert the frame to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # Copy the frame to draw the box around the person
            frame_with_box = frame.copy()
            draw_person_box(frame_with_box, landmarks)

            # Show the frame with the bounding box
            cv2.imshow('Camera with Bounding Box Around Person', frame_with_box)

        if cv2.waitKey(1) & 0xFF == ord('e'):  # Exit the loop when 'e' is pressed
            break

    camera.release()
    cv2.destroyAllWindows()

# Run the program
process_camera()
