import ctypes
import sys
import time
import webbrowser
import googlescrap as googlescrap
import pyttsx3
import pywhatkit
import speech_recognition as sr
import datetime
import wikipedia
import os
import smtplib
import pyjokes
import subprocess
import winshell

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[len(voices) - 1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning Sir !")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Sir !")
    else:
        speak("Good Evening Sir !")
    assname = ("kera")
    speak("I am your Assistant")
    speak(assname)

def username():
    speak("What should i call you sir")
    uname = takeCommand()
    speak("Welcome Mister")
    speak(uname)
    speak("How can i Help you, Sir")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        recordedaudio = r.listen(source)
        r.pause_threshold = 50
        print('Done Recording..!')

    try:
        print("Recognizing...")
        query = r.recognize_google(recordedaudio, language='en-us')
        print(f"User said: {query}\n")

    except Exception as e:
        speak("Say that again please...")
        return "None"
    return query

if __name__ == "__main__":
    wishMe()
    username()
    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(results)

        elif 'open youtube' in query:
            speak("opening youtube")
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            speak("opening google")
            webbrowser.open("google.com")

        elif 'open stack overflow' in query:
            speak("opening stackoverflow")
            webbrowser.open("stackoverflow.com")

        elif 'play music' in query:
            speak("playing music")
            music_dir = 'E:\\music'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'jokes' in query:
            speak(pyjokes.get_joke())

        elif 'how are you' in query:
            speak("i am fine. Thank you")
            print("i am fine Thank you")
            speak("how are you sir")

        elif 'good' in query:
            speak("its good to know that you are fine")

        elif 'who are you' in query:
            speak("i am your personal assistant")

        elif 'google search' in query:
            query = query.replace("google search", " ")
            query = query.replace("google", " ")
            speak("This are the results of the following search")
            pywhatkit.search(query)
            try:
                pywhatkit.search(query)
                result = googlescrap.summary(query, 3)
                speak(result)
            except:
                speak(" ")

        elif 'open gmail' in query:
            speak('opening gmail')
            webbrowser.open('www.gmail.com')


        elif 'clear recycle bin' in query:
            winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
            speak("Recycle Bin Recycled")

        elif 'lock window' in query:
            speak("locking the device")
            ctypes.windll.user32.LockWorkStation()

        elif "hibernate" in query or "sleep" in query:
            speak("Hibernating")
            subprocess.call("shutdown / h")

        elif "log off" in query or "sign out" in query:
            speak("Make sure all the application are closed before sign-out")
            time.sleep(5)
            subprocess.call(["shutdown", "/l"])

        elif 'shutdown system' in query:
            speak("Hold On a Sec ! Your system is on its way to shut down")
            subprocess.call('shutdown / p /f')

        elif 'quit' in query or 'stop' in query or 'bye' in query:
            speak('okay.....!Bye Sir, have a good day.')
            sys.exit()


