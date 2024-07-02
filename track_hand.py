import cv2
import mediapipe as mp
from pyautogui import size,moveTo
import time

# Initialize MediaPipe Hands solution
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Set up webcam input
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Convert the BGR image to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Flip the image for a mirror effect
        image = cv2.flip(image, 1)

        # Process the image and find hands
        results = hands.process(image)

        # Convert the image color back so it can be displayed
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Draw hand annotations on the image
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2))

                for id, landmark in enumerate(hand_landmarks.landmark):
                    height, width, _ = image.shape
                    cx, cy = int(landmark.x * width), int(landmark.y * height)
                    print(f'Landmark {id}: (x: {cx}, y: {cy}, z: {landmark.z})')

                    # Optionally draw the coordinates on the image
                    cv2.putText(image, f'{id}', (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

                    # Move the mouse to the landmark position
                    if id == 8:  # Example: Move the mouse to the 9th landmark (index finger tip)
                        screen_width, screen_height = pyautogui.size()
                        if 0 <= cx < screen_width and 0 <= cy < screen_height:
                            pyautogui.moveTo(cx, cy)
                            time.sleep(0.1)  # Adding a small delay

        # Display the annotated image
        cv2.imshow('Hand Tracking', image)

        # Break the loop when 'Esc' key is pressed
        if cv2.waitKey(5) & 0xFF == 27:
            break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()
