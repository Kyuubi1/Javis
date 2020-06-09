# Requires PyAudio and PySpeech.

import speech_recognition as sr
from time import ctime
import time
import os
from gtts import gTTS
import webbrowser


def speak(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='vi')
    tts.save("audio.mp3")
    os.system("mpg321 audio.mp3")


def recordAudio():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Đang tiến hành lọc nhiễu, vui lòng chờ trong giây lát")
        r.adjust_for_ambient_noise(source, duration=2)
        print("Hãy đưa ra yêu cầu")
        audio = r.listen(source)

    # Speech recognition using Google Speech Recognition
    data = ""
    try:
        # Uses the default API key
        # To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        data = r.recognize_google(audio, language='vi')
        print("You said: " + data)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return data


def jarvis(data):
    if "Tìm kiếm nhạc" in data:
        speak("Bạn muốn nghe bài hát nào")

    if ("Em đâu biết" or "em") in data:
        data = data.split(" ")
        song_name = data[2]
        speak("Vui lòng chờ, Tôi đang tìm kiếm bài hát " + song_name + " cho bạn")
        webbrowser.open('https://www.youtube.com/watch?v=psIUhGjjv7w')


# initialization
time.sleep(2)
speak("Xin chào Đức Anh, tôi có thể giúp gì cho ngài")
while 1:
    data = recordAudio()
    jarvis(data)
