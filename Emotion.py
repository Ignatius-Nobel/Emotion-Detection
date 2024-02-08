import cv2
from array import *
from deepface import DeepFace
import pyttsx3
import time


def most_frequent(List):
    counter = 0
    num = List[0]
    for i in List:
        curr_frequency = List.count(i)
        if (curr_frequency > counter):
            counter = curr_frequency
            num = i
    return num


faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(1)
if not cap.isOpened():
    cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise IOError("Cannot Open WebCam")
a = []
for i in range(50):
    ret, frame = cap.read()
    predictions = DeepFace.analyze(frame, actions=['emotion','age','gender'], enforce_detection=False)
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # PRINT(face.Cascade.empty())
    faces = faceCascade.detectMultiScale(gray, 1.1, 4)
    # print(faces)
    # Draw a rectangle around face
    while faces:
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    #font = cv2.FONT_HERSHEY_SIMPLEX
    # cv2.putText(frame,
    #             predictions['dominant_emotion'],
    #             (50, 50),
    #             font, 4,
    #             (0, 0, 255),
    #             2,
    #             cv2.LINE_4)

    a.append([predictions['dominant_emotion']])

    cv2.imshow('Emotion detector', frame)
    #    cv2.imshow('gray',gray)

    if cv2.waitKey(2) & 0xFF == ord('q'):
        break
cap.release()
speaker = pyttsx3.init()
speaker.say(most_frequent(a))
speaker.runAndWait()
time.sleep(1)
print()
cv2.destroyAllWindows()