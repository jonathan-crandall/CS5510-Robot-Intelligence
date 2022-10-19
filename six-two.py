import sys
import os
import cv2
import pandas as pd
from fer import FER
from fer.utils import draw_annotations


# def df_process(in_data: list, video: Video):
#     vid_df = video.to_pandas(in_data)
#     vid_df = video.get_first_face(vid_df)
#     vid_df = video.get_emotions(vid_df)

#     display(vid_df.plot(figsize=(20, 8), fontsize=16).get_figure())

#     angry = sum(vid_df.angry)
#     disgust = sum(vid_df.disgust)
#     fear = sum(vid_df.fear)
#     happy = sum(vid_df.happy)
#     sad = sum(vid_df.sad)
#     surprise = sum(vid_df.surprise)
#     neutral = sum(vid_df.neutral)

#     emotions = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]
#     emotions_values = [angry, disgust, fear, happy, sad, surprise, neutral]

#     score_comparisons = pd.DataFrame(emotions, columns=["Human Emotions"])
#     score_comparisons["Emotion Value from the Video"] = emotions_values
#     display(score_comparisons)


path = 0
if len(sys.argv) > 2 and os.path.exists(sys.argv[1]):
    path = sys.argv[1]

detector = FER()
cap = cv2.VideoCapture(0)

vid_df = pd.DataFrame()

if not cap.isOpened():
    print("Cannot open camera / video file")
    exit()

print("Reading from camera...")
while True:
    ret, frame = cap.read()

    if not ret:
        print("Stream closed...")
        break

    frame = cv2.flip(frame, 1)
    emotions = detector.detect_emotions(frame)
    frame = draw_annotations(frame, emotions)

    if emotions:
        print(emotions)
        vid_df.append(emotions["emotions"])
        print(vid_df.style)
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

[
    {
        "box": array([446, 134, 55, 55]),
        "emotions": {
            "angry": 0.03,
            "disgust": 0.0,
            "fear": 0.04,
            "happy": 0.81,
            "sad": 0.1,
            "surprise": 0.0,
            "neutral": 0.02,
        },
    }
]
