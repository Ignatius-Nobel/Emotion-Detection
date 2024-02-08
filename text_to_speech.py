from gtts import gTTS
import os

myText = "You look so Happy! Chap"

language = 'en'

output = gTTS(text=myText,lang = language,slow=False)

output.save("output.mp3")

os.system("start output.mp3")