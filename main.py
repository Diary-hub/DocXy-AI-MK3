import speech_recognition as sr
from Functions import *

# initialize the recognizer
r = sr.Recognizer()
isActive = False

while True:
    # use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Waiting For Activating...")
        # adjust for ambient noise, if any
        r.adjust_for_ambient_noise(source)
        # listen for audio and store it in an AudioData object
        audio = r.listen(source, 0, 5)

    # recognize speech using Google Speech Recognition
    try:
        mySpeech = r.recognize_google(audio)
        if "Jarvis Wake Up".lower() in mySpeech.lower() and not isActive:
            isActive = True
            CheckForCommand(mySpeech)
            while isActive:
                with sr.Microphone() as source:
                    print("Listining...")
                    # adjust for ambient noise, if any
                    r.adjust_for_ambient_noise(source)

                    # listen for audio and store it in an AudioData object
                    audio = r.listen(source, 0, 5)
                try:
                    mySpeech = r.recognize_google(audio)
                    print("You said: " + mySpeech)
                    if "jarvis deactivate" in mySpeech.lower():
                        isActive = False
                        Read("Deactivating Sir")
                        break
                    CheckForCommand(mySpeech)
                except sr.UnknownValueError:
                    print("Sorry Sir, I Could Not Understand")
                    continue
                except sr.RequestError:
                    print("Sorry, my speech recognition service is down")
                    continue

    except sr.UnknownValueError:
        print("No Wake Command Found")
        continue
    except sr.RequestError:
        print("Sorry, my speech recognition service is down")
        continue
