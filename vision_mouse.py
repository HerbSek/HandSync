import cv2
import mediapipe as mp
import pyautogui
import time

def landmarks_close(lm1, lm2, threshold=0.05):
    return abs(lm1.x - lm2.x) < threshold and abs(lm1.y - lm2.y) < threshold and abs(lm1.z - lm2.z) < threshold


# Initialize MediaPipe Hands solution
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

time.sleep(5)

screen_width, screen_height = pyautogui.size()

# Set up webcam input
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
        model_complexity=1,
        min_detection_confidence=0.8,
        min_tracking_confidence=0.8) as hands:
    
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Convert the BGR image to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Flip the image for a mirror effect
        image = cv2.flip(image, 1)

        copy_image = image.copy()
        copy_image = cv2.resize(copy_image, (screen_width//5, screen_height//5), interpolation = cv2.INTER_AREA)

        image = cv2.resize(image, (int(screen_width * 1.2), int(screen_height * 1.2)), interpolation = cv2.INTER_AREA)

        

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
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
                    )
            

                for id, landmark in enumerate(hand_landmarks.landmark):
                    height, width, _ = image.shape
                    cx, cy = int(landmark.x * width), int(landmark.y * height)
                    # print(f'Landmark {id}: (x: {cx}, y: {cy}, z: {landmark.z})')

                    # Optionally draw the coordinates on the image
                    # cv2.putText(image, f'{id}', (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

                    # Move the mouse to the landmark position
                    if id == 8:  # Example: Move the mouse to the 9th landmark (index finger tip)
                        cv2.circle(copy_image, (cx//5,cy//5), 1, (255, 0, 0), 3)
                        pyautogui.moveTo(cx, cy)
                            # time.sleep(0.1)  # Adding a small delay
                        if landmarks_close(hand_landmarks.landmark[4], hand_landmarks.landmark[8]):
                        # if hand_landmarks.landmark[4] ==  hand_landmarks.landmark[8]:
                            pyautogui.dragTo(cx, cy)
                            print(f'User is dragging !!!')
                    
                   
                    


        # Display the annotated image
        # cv2.imshow('Hand Tracking', image)
        cv2.imshow('Hand Tracking', copy_image)

        # Break the loop when 'Esc' key is pressed
        if cv2.waitKey(5) & 0xFF == 27:
            break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()
