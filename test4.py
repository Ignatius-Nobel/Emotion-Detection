import cv2
from deepface import DeepFace
import pyttsx3
import time
import pymongo

client = pymongo.MongoClient()
mydb = client["Datas"]
mycol = mydb["peoples"]


def most_frequent(List):
    counter = 0
    num = List[0]
    for i in List:
        curr_frequency = List.count(i)
        if (curr_frequency > counter):
            counter = curr_frequency
            num = i
    return num


while True:
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot Open WebCam")
    a = []
    t_end = time.time() + 10
    while time.time() < t_end:
        ret, frame = cap.read()
        predictions = DeepFace.analyze(frame, actions=['emotion', 'gender', 'age'], enforce_detection=False)

        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # PRINT(face.Cascade.empty())
        faces = faceCascade.detectMultiScale(gray, 1.1, 5)
        print(len(faces))
        if (len(faces) == 0):
            continue
        # Draw a rectangle around face

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,
                    predictions['dominant_emotion'],
                    (50, 50),
                    font, 4,
                    (0, 0, 255),
                    2,
                    cv2.LINE_4)

        if (predictions['dominant_emotion'] == 'neutral'):
            continue
        a.append([predictions['dominant_emotion']])

        cv2.imshow('Emotion detector', frame)
        #    cv2.imshow('gray',gray)

        if cv2.waitKey(2) & 0xFF == ord('q'):
            break
    cap.release()
    speaker = pyttsx3.init()
    age = predictions['age']
    gender = predictions['gender']
    time1 = time.localtime().tm_hour
    print(a)
    if(len(a)==0):
    #    speaker.say("Sorry, I could not recognise your emotion please try again")
        continue
    emotion = most_frequent(a)
    print(age)
    print(gender)
    print(emotion)
    data = {'age': age, 'gender': gender, 'emotion':emotion[0],'time':time1}
    mycol.insert_one(data)
    if (emotion[0] == 'happy'):
        speaker.say("Hey, you look so happy")
    elif (emotion[0] == 'sad'):
        speaker.say("Hey don't be sad you will be all right")
    elif (emotion[0] == 'fear'):
        speaker.say("Hey don't be scared, be strong")
    elif (emotion[0] == 'angry'):
        speaker.say("Hey, what makes you so angry?")
    elif (emotion[0] == 'surprise'):
        speaker.say("Anything special? you looks so surprised!!!")
    elif (emotion[0] == 'disgust'):
        speaker.say("Why are you Disgusted?")
    # speaker.say(most_frequent(a))
    speaker.runAndWait()
    time.sleep(1)
    cv2.destroyAllWindows()