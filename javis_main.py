# Requires PyAudio and PySpeech.

import speech_recognition as sr
import time
import os
from gtts import gTTS
import webbrowser
from datetime import datetime
import sys
import constant
from youtube_search import YoutubeSearch
import pafy
import vlc


def speak(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='vi')
    tts.save("audio.mp3")
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
        data = r.recognize_google(audio, language='vi')
        data.lower()
        print("You said: " + data)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return data


def jarvis(data):

    if constant.MUSIC in data:
        search_youtube()

    if constant.TIME in data:
        voice = get_time()
        speak(voice)

    if constant.LOCATION in data:
        remove_text_index = data.find('ở đâu')
        location = data[0:remove_text_index]
        speak(f"Đang tìm kiếm địa điểm {location}")
        search_map(location=location)

    if constant.CLOSE in data:
        close()


# get current time
def get_time():
    now = datetime.now()
    hour = now.time().hour
    minute = now.time().minute
    answer = f"Bây giờ là {hour} giờ {minute} phút"
    return answer


# search location
def search_map(location: str):
    webbrowser.open(f"https://www.google.com/maps/place/{location}?hl=vi-VN")


def search_youtube():
    speak("Bạn muốn nghe bài hát nào")
    search_text = record_audio()
    time.sleep(2)
    if search_text:
        speak(f"Có phải bạn muốn tìm bài hát {search_text}")
        answer = record_audio()
        if constant.TRUE in answer:
            print(search_text)
            result = YoutubeSearch(search_text, max_results=10).to_dict()
            if len(result) == 0:
                speak("Không có kết quả tìm kiếm nào cho bài hát bạn đưa ra")
            else:
                speak("Tiến hành phát nhạc cho kết quả phù hợp nhất")
                link = result[0]['link']
                BASE_URL = "https://www.youtube.com"
                url = f"{BASE_URL}{link}"
                play = play_video(url)
                play.play()
                time.sleep(10)
                action_when_play_video(play)

        else:
            time.sleep(1)
            search_youtube()


def close():
    sys.exit()


def play_video(url: str):
    # get best link to play with pafy
    video = pafy.new(url)
    best = video.getbest()
    play_url = best.url

    # play video via VLC
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(play_url)
    media.get_mrl()
    player.set_media(media)
    return player


def action_when_play_video(play):
    command = record_audio()
    if constant.PAUSE in command:
        play.pause()
        action_when_play_video(play)
    elif constant.RESUME in command:
        play.pause()
        action_when_play_video(play)
    elif constant.STOP in command:
        play.stop()


# initialization
time.sleep(2)
speak("Xin chào Đức Anh, tôi có thể giúp gì cho ngài")
while 1:
    data = record_audio()
    jarvis(data)
