import cv2
import mediapipe as mp
import pyautogui
import time
import streamlit as st
from streamlit_webrtc import VideoProcessorBase, webrtc_streamer
import av

with open('track.css') as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html = True)
    
def landmarks_close(lm1, lm2, threshold=0.09):
    return abs(lm1.x - lm2.x) < threshold and abs(lm1.y - lm2.y) < threshold and abs(lm1.z - lm2.z) < threshold

pyautogui.FAILSAFE = False
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

screen_width, screen_height = pyautogui.size()


st.title("HandSync 🙌")
st.subheader("Control your mouse with hand gestures.")


class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.hands = mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.9,
            min_tracking_confidence=0.9
        )

    def recv(self, frame):
        image = frame.to_ndarray(format="bgr24")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)  


        copy_image = image.copy()
        copy_image = cv2.cvtColor(copy_image, cv2.COLOR_RGB2BGR)
        copy_image = cv2.resize(copy_image, (screen_width // 5, screen_height // 5), interpolation=cv2.INTER_AREA)
        image = cv2.resize(image, (int(screen_width * 1.2), int(screen_height * 1.2)), interpolation=cv2.INTER_AREA)

        results = self.hands.process(image)

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

                  
                    if not landmarks_close(hand_landmarks.landmark[4], hand_landmarks.landmark[8]):
                        if id == 8:
                            cv2.circle(copy_image, (cx // 5, cy // 5), 1, (255, 0, 0), 3)
                            pyautogui.moveTo(cx, cy)
                            print('Moving Mouse!')

                    elif landmarks_close(hand_landmarks.landmark[4], hand_landmarks.landmark[8]) and id == 8:
                        pyautogui.dragTo(cx, cy)  
                        print('Dragging!')

        return av.VideoFrame.from_ndarray(copy_image, format="bgr24")


webrtc_streamer(key="hand-tracking", video_processor_factory=VideoProcessor)

st.write("Move the mouse with your index finger and click/drag by pinching your thumb and index finger together.")




st.markdown('---')

st.write('Developed by Herbert Sekpey with ❤️')