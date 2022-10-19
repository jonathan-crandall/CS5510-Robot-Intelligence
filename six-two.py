import sys
import os

# Must set flags before importing tensorflow
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import cv2
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
from fer import FER
from fer.utils import draw_annotations

path = 0
if len(sys.argv) >= 2 and os.path.exists(sys.argv[1]):
    path = sys.argv[1]

print(path)
detector = FER()
cap = cv2.VideoCapture(path)

vid_data = []

if not cap.isOpened():
    print("Cannot open camera / video file")
    exit()

print(f"Reading from {'camera' if path == 0 else path}")
print("Press q to exit the camera and print results")

# Read from video feed
while True:
    ret, frame = cap.read()

    if not ret:
        print("Stream closed...")
        break

    frame = cv2.flip(frame, 1)
    emotions = detector.detect_emotions(frame)
    frame = draw_annotations(frame, emotions)

    if emotions:
        emo = emotions[0]["emotions"]
        vid_data.append(emo)
        print(" ".join([f"{k}: {v}" for k, v in emo.items()]) + "\t\t\t", end="\r")
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) == ord("q"):
        break

# Calculate stats
vid_df = pd.DataFrame(vid_data)
angry = sum(vid_df.angry)
disgust = sum(vid_df.disgust)
fear = sum(vid_df.fear)
happy = sum(vid_df.happy)
sad = sum(vid_df.sad)
surprise = sum(vid_df.surprise)
neutral = sum(vid_df.neutral)
print()
emotions = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]
emotions_values = [angry, disgust, fear, happy, sad, surprise, neutral]
score_comparisons = pd.DataFrame(emotions, columns=["Human Emotions"])
score_comparisons["Emotion Value from the Video"] = emotions_values

vid_df.plot()
print(tabulate(score_comparisons, headers="keys", tablefmt="psql"))

plt.show()
cap.release()
cv2.destroyAllWindows()
