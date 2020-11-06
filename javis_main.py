# Requires PyAudio and PySpeech.

import speech_recognition as sr
import time
import os
from gtts import gTTS
import webbrowser
import sys
import constant
from youtube_search import YoutubeSearch
import pafy
import vlc
import webbrowser
import datetime
from time import ctime
import requests
import base64

# def speak(audioString):
#     print(audioString)
#     tts = gTTS(text=audioString, lang='en')
#     tts.save("audio.mp3")
#     os.system("mpg321 audio.mp3")

def speak(text):
    API_KEY = 'AIzaSyAN8LcZhriwuNa94u4L4ZE4NJbVglUm5uM'
    API_URL = f'https://texttospeech.googleapis.com/v1/text:synthesize?key={API_KEY}'
    data = {
        "input": {
            "text": text
        },
        "audioConfig": {
            "audioEncoding": "MP3"
        },
        "voice": {
            # "languageCode": "en-US"
            "languageCode": "en-US"
        }
    }

    res = requests.post(API_URL, json=data)
    audio_b64 = res.json()['audioContent']
    audio_byte = base64.b64decode(audio_b64)
    with open("audio.mp3", mode='wb') as f:
        f.write(audio_byte)
        os.system("mpg321 audio.mp3")


def record_audio():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=2)
        print("Hãy đưa ra yêu cầu")
        audio = r.listen(source)

    # Speech recognition using Google Speech Recognition
    data = ""
    try:
        # Uses the default API key
        # To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        data = r.recognize_google(audio, language='en-in')
        data.lower()
        print("You said: " + data)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return data


def jarvis(data):

    if constant.MUSIC in data:
        play_favorite_music()

    if constant.WORkPLACE in data:
        check_workplace()
    if constant.TIME in data:
        get_time()
    if constant.WEATHER in data:
        get_weather()
    if constant.THANKS in data:
        only_jarvis_reply()
    if constant.TIRED in data:
        jarvis_system()
    if constant.CLOSE in data:
        close()


# get current time
def get_time():
    now = datetime.datetime.now()
    hour = now.time().hour
    minute = now.time().minute
    speak(ctime())
    work_hour = 11 - hour
    if work_hour > 0:
        work_minutes = 30 + 60 - minute
        if work_minutes < 60:
            speak(f"You have {work_hour} hour and {work_minutes} minutes to go to work")
        else:
            add_hour = int(work_minutes/60)
            add_minutes = work_minutes - add_hour * 60
            speak(f"You have {add_hour} hour and {add_minutes} minutes to go to work")
    else:
        speak("Sir, you are late for work")


def get_weather():
    BASE_URL = 'https://api.openweathermap.org/data/2.5/weather?'
    CITY = "Ha Noi"
    API_KEY = "c60040519c58a816da13786300c3511a"
    URL = BASE_URL + "q=" + CITY + "&appid=" + API_KEY
    res = requests.get(URL)
    if res.status_code == 200:
        data = res.json()
        temp = data['main']['temp']
        C_temp = temp - 273.15
        speak(f"The weather outside is {C_temp} degrees Celsius")


def close():
    sys.exit()


def play_video():
    # get best link to play with pafy
    url = 'https://www.youtube.com/playlist?list=LL'
    video = pafy.new(url)
    best = video.getbest()
    play_url = best.url

    # play video via VLC
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(play_url)
    media.get_mrl()
    player.set_media(media)
    player.play()


def play_favorite_music():
    speak("Would you like this?")
    url = 'https://www.youtube.com/watch?v=eKP1Agud-GQ&list=PL4kx4v8kuHgcLNRA6lGsvuzPT5_ZqDXm0'
    webbrowser.open(url)


def check_workplace():
    speak("Opening workplace")
    url = 'https://ecomedic.workplace.com/chat/'
    webbrowser.open(url)


def greeting():
    time.sleep(2)
    speak("Good morning sir, it's time to wake up")


def only_jarvis_reply():
    speak("No problem, sir")


def jarvis_system():
    speak("I know, sir")
    speak("You let the system up and running for the whole night")


def main():
    greeting()
    while 1:
        data = record_audio()
        jarvis(data)


if __name__ == '__main__':
    main()
