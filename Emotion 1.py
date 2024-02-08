import cv2
from deepface import DeepFace
import mysql.connector
db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "root",
    database = "testdatabase"
)
mycursor = db.cursor()
mycursor.execute("Create Table Emotion (personId int PRIMARY KEY, Emotion VARCHAR(20)")
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(1)
if not cap.isOpened():
    cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise IOError("Cannot Open WebCam")
while True:
    ret,frame = cap.read()
    predictions = DeepFace.analyze(frame, actions = ['emotion','age','gender'])
    gray = cv2.cvtColor(frame, cv2.COLOR_RB2GRAY)
#PRINT(face.Cascade.empty())
    faces = faceCascade.detectMultiScale(gray,1.1,4)
#Draw a rectangle around face
    for(x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w,y+h),(0,255,0),2)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame,
                   predictions['dominant_emotion'],
                   (50,50),
                   font, 4,
                   (0,0,255),
                    2,
                       cv2.LINE_4) ;
    cv2.imshow('Demo Video',frame)
    if cv2.waitKey(2) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()