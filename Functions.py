import os
import subprocess
import openai
import pyttsx3
import json
import random
import requests
import mysql.connector
import tkinter as tk
from tkinter import filedialog
import pywhatkit
from pytube import YouTube
from API_Secrets import *
import webbrowser
from docxtpl import DocxTemplate
import speech_recognition as sr


def Read(text):
    # Initialize the Text-to-speech engine
    engine = pyttsx3.init()

    # Set the properties of the voice
    engine.setProperty("rate", 180)  # Speed in words per minute
    engine.setProperty("volume", 0.7)  # Volume between 0 and 1
    engine.setProperty(
        "voice",
        "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0",
    )  # Change the language or accent as needed
    print(text)
    # Convert text to speech
    engine.say(text)
    engine.runAndWait()


def Listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Waiting For Activating...")
        # adjust for ambient noise, if any
        r.adjust_for_ambient_noise(source)
        # listen for audio and store it in an AudioData object
        audio = r.listen(source, 0, 8)

    try:
        mySpeech = r.recognize_google(audio)
        print("You said: " + mySpeech)
        return mySpeech
    except sr.UnknownValueError:
        print("Sorry Sir, I Could Not Understand")
        return ""

    except sr.RequestError:
        print("Sorry, my speech recognition service is down")
        return ""


openai.api_key = API_KEY_CHATGPT_AI  # Replace with your API key


def ask_gpt(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=1024,
        n=1,
        stop=None,
    )

    print("ChatGPT: ", response.choices[0].text)
    return response.choices[0].text


def talk_gpt(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=25,
        n=1,
        stop=None,
    )
    return response.choices[0].text


def OpenApp(app, path):
    Read("Opening " + app)
    # subprocess.call([path])
    os.startfile(path)


def addProgram(app, path):
    try:
        # establish a connection to the database
        mydb = mysql.connector.connect(
            host=DB_SERVER, user=DB_USERNAME, password=DB_PASSWORD, database=DB_NAME
        )

        # create a cursor object
        mycursor = mydb.cursor()

        # SQL QUERY to insert a new value into a column
        sql = "INSERT INTO programs (`Name`, `Path`) VALUES (%s,%s)"

        # value to be inserted into the column
        val = (app, path)

        # execute the SQL QUERY with the value
        mycursor.execute(sql, val)

        # commit the changes to the database
        mydb.commit()

        # print the ID of the last inserted row
        print("1 record inserted, ID: ", mycursor.lastrowid)
        OpenApp(app, path)
        Read("1 record inserted")

    except mysql.connector.Error as error:
        Read("Failed to retrieve data from MySQL table: {}".format(error))
        Read("Failed to retrieve data from MySQL table: {}".format(error))


def setPath(app):
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()
    addProgram(app, file_path)


def SearchForPath(app):
    try:
        # establish a connection to the database
        mydb = mysql.connector.connect(
            host=DB_SERVER, user=DB_USERNAME, password=DB_PASSWORD, database=DB_NAME
        )

        # create a cursor object to execute queries
        mycursor = mydb.cursor()

        # execute a SELECT QUERY to retrieve data from a specific column
        mycursor.execute("SELECT Path FROM programs where Name='" + app.lower() + "'")

        # retrieve the results of the QUERY
        results = mycursor.fetchall()
        if not results:
            Read(
                "Sir, There is no Application named "
                + app
                + " In The data base, Please Provide a Path to that Application."
            )
            setPath(app)

        # print the results to the console
        for result in results:
            print(result[0])
            OpenApp(app, result[0])

    except mysql.connector.Error as error:
        print("Failed to retrieve data from MySQL table: {}".format(error))


def Play(name):
    # search for the song on YouTube
    pywhatkit.playonyt(name)


def PrepareWord(title, members=["Diary Tariq Ibrahem"]):
    Read(
        talk_gpt(
            "pretend like like your jarivs, answer me this prompt like you already did write or created it"
            + ", only an answer for the sake of conversation of 10-20 words and dont use suggesting:"
            + "jarvis i have an assigmnet about "
            + title
        )
    )
    Read("Sir I'am Working on Preparing a Document about " + title)
    file = DocxTemplate("Assets\DOCX Template\AssigmentTemplate.docx")
    context = {
        "title": title,
        "members": members,
        "abstract": ask_gpt(
            "give me only  150 words  and a Abstract about (" + title + ")"
        ),
        "introduction": ask_gpt(
            "give me only  800 words  and a Introduction  about (" + title + ")"
        ),
        "reference": ask_gpt(
            "give me only 5 refrences in a list about "
            + title
            + " in this format, Author name,” Title of the paper”, title of the journal, vol. , No., pp , year"
        ),
    }
    file.render(context)
    file.save("Assets\Generated Files\\" + title + ".docx")
    Read("Sir, The Document is Ready I Will Open it!")
    OpenApp(title, "Assets\Generated Files\\" + title + ".docx")


def CheckForCommand(QUERY, MEMBERS=["Diary Tariq Ibrahem"]):
    if "open".lower() in QUERY.lower():
        print(QUERY.lower().split("open ", 1)[1])
        SearchForPath(QUERY.lower().split("open ", 1)[1])
    elif "lunch".lower() in QUERY.lower():
        print(QUERY.lower().split("lunch ", 1)[1])
        SearchForPath(QUERY.lower().split("open ", 1)[1])
    elif " GPT ".lower() in QUERY.lower() or "GPT ".lower() in QUERY.lower():
        Read(ask_gpt(QUERY.lower().split("gpt ", 1)[1]))
    elif "jarvis play".lower() in QUERY.lower() or " play ".lower() in QUERY.lower():
        Read("Playing " + QUERY.lower().split("play ", 1)[1])
        Play(QUERY.lower().split("play ", 1)[1])
    elif "bring it".lower() in QUERY.lower():
        Play("Mother Mother - Hayloft")
    elif "i have an assignment".lower() in QUERY.lower():
        TITLE = QUERY.lower().split("about ", 1)[1]
        PrepareWord(TITLE, MEMBERS)
    elif "bye".lower() in QUERY.lower():
        Read(
            random.choice(
                [
                    "Sir, Jarvis is Out of Service",
                    "I'm Shutting Down",
                    "It Seems I'm No Longer Required",
                ]
            )
        )
        exit()
    else:
        Read(
            ask_gpt(
                "Your Jarivs from iron man, when i tell you anything, respond fast and short, just like jarivs: "
                + QUERY
            )
        )


def Carter_AI(query):
    response = requests.post(
        "https://api.carterlabs.ai/chat",
        headers={"Content-Type": "application/json"},
        data=json.dumps(
            {
                "text": query,
                "key": API_KEY_CARTER_AI,
                "playerId": "jarvis",  # THIS CAN BE ANYTHING YOU WANT!
                "speak": True,  # DEFAULT FALSE | FOR VOICE OUTPUT
            }
        ),
    )
    import playsound as ps
    import urllib.request
    from pydub import AudioSegment
    from pydub.playback import play

    urllib.request.urlretrieve(
        response.json()["output"]["audio"], "Assets\Audio Files\Output\Response.mp3"
    )

    ps.playsound("Assets\Audio Files\Output\Response.mp3")
