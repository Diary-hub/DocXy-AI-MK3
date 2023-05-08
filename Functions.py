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
import playsound as ps
import urllib.request
from pydub import AudioSegment
import time
import threading
import datetime
import socket


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
    engine.startLoop(False)
    return text


def Listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
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

    # print("ChatGPT: ", response.choices[0].text)
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
        mycursor.execute(
            "SELECT Path FROM programs where Name='" + app.lower() + "'")

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


def CreateWord(title, members):
    file = DocxTemplate("Assets\DOCX Template\AssigmentTemplate.docx")
    context = {
        "title": title,
        "members": members,
        "abstract": ask_gpt(
            "give me only  150 words  and a Abstract about (" + title + ")"
        ),
        "introduction": ask_gpt(
            "give me only  800 words  and a Introduction  about (" +
            title + ")"
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


def PrepareWord(title, members=["Diary Tariq Ibrahem"]):
    responce = talk_gpt(
        "pretend like like your jarivs, answer me this prompt like you already did write or created it"
        + ", only an answer for the sake of conversation of 10-20 words and dont use suggesting:"
        + "jarvis i have an assigmnet about "
        + title
    )
    t = threading.Thread(target=Read, args=[responce])
    t.start()

    t = threading.Thread(target=CreateWord, args=[title, members])
    t.start()
    t2 = threading.Thread(
        target=Read, args=[
            "Sir I'am Working on Preparing a Document about " + title]
    )
    t2.start()
    return "Sir I'am Working on Preparing a Document about " + title


def Carter_AI(query):
    response = requests.post(
        "https://api.carterlabs.ai/chat",
        headers={"Content-Type": "application/json"},
        data=json.dumps(
            {
                "text": query,
                "key": API_KEY_CARTER_AI,
                "playerId": "jarvis",
                "personal": True,  # THIS CAN BE ANYTHING YOU WANT!
                "speak": True,  # DEFAULT FALSE | FOR VOICE OUTPUT
            }
        ),
    )
    t = threading.Thread(target=PlaySound, args=[
                         response.json()["output"]["audio"]])
    t.start()
    return response.json()["output"]["text"]


def PlaySound(URL):
    urllib.request.urlretrieve(URL, "Assets\Audio Files\Output\Response.mp3")

    ps.playsound("Assets\Audio Files\Output\Response.mp3")
    os.remove("Assets\Audio Files\Output\Response.mp3")


def Exam():
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError

    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

    creds = Credentials.from_service_account_file(
        "Assets/Jarivs_Keys.json",
        scopes=SCOPES,
    )

    try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(
                spreadsheetId="1IBo4HxiCSglzgIdm4ALyG3wABay9SwOq8Igt_A_Lpv4",
                range="Sheet1!A1:C7",
            )
            .execute()
        )
        values = result.get("values", [])

        if not values:
            print("No data found.")
            return

        isNextExam = True
        i = 2
        while isNextExam:
            try:
                if values[i][1]:
                    subject = values[i][1].split("(", 1)[0]
                    date = values[i][0].split(" ", 1)[1]
                    dateDay = date.split("/", 2)[0]
                    dateDay = dateDay.replace(" ", "")
                    day = values[i][0].split(" ", 1)[0]

                    today = str(datetime.date.today()).split("-", 2)[2]
                    todayDateDay = ""

                    for char in range(0, len(today)):
                        if char == 0 and today[char] == "0":
                            continue
                        todayDateDay += today[char]

                    date = date.replace(" ", "")
                    date = date.replace("/", " ")
                    if int(dateDay) > int(todayDateDay):
                        responce = (
                            "The Next Exam is: " + subject + "On " + day + " " + date
                        )
                        t = threading.Thread(target=Read, args=[responce])
                        t.start()

                        return responce
                    else:
                        i += 1
                else:
                    isNextExam = False
                    responce = "Sir, You Don't Have Any Exam Scheduled"
                    return responce
            except IndexError:
                isNextExam = False
                responce = "Sir, You Don't Have Any Exam Scheduled"
                return responce

    except HttpError as err:
        print(err)


def shutdownPC(command="shutdown"):
    s = socket.socket()
    host = '0.0.0.0'
    print(host)
    port = 1234
    s.bind((host, port))
    print("")
    print("Waiting For Any Connections . . . .")
    print("")
    s.listen()
    conn, addr = s.accept()
    print("")
    print("--- ", addr, " --- Has Connected.")
    conn.send(command.encode())
    print("Command Sended")
    responce = 'Host with Address: ' + addr + " Is Turned Off"
    t = threading.Thread(target=Read, args=[responce])
    t.start()
    return responce


def CheckForCommand(QUERY, MEMBERS=["Diary Tariq Ibrahem"]):
    if "open".lower() in QUERY.lower():
        print(QUERY.lower().split("open ", 1)[1])
        SearchForPath(QUERY.lower().split("open ", 1)[1])
    elif "lunch".lower() in QUERY.lower():
        print(QUERY.lower().split("lunch ", 1)[1])
        SearchForPath(QUERY.lower().split("open ", 1)[1])
    elif " GPT ".lower() in QUERY.lower() or "GPT ".lower() in QUERY.lower():
        responce = ask_gpt(QUERY.lower().split("gpt ", 1)[1])
        t = threading.Thread(target=Read, args=[responce])
        t.start()
        return responce
    elif "jarvis play".lower() in QUERY.lower() or " play ".lower() in QUERY.lower():
        Play(QUERY.lower().split("play ", 1)[1])
        return Read("Playing " + QUERY.lower().split("play ", 1)[1])
    elif "bring it".lower() in QUERY.lower():
        Play("Mother Mother - Hayloft")
        return Read("Sir, There You Go.")
    elif "i have an assignment".lower() in QUERY.lower():
        TITLE = QUERY.lower().split("about ", 1)[1]
        return PrepareWord(TITLE, MEMBERS)
    elif "next exam".lower() in QUERY.lower() or "what exam".lower() in QUERY.lower():
        return Exam()
    elif "shutdown".lower() in QUERY.lower() or "shut down".lower() in QUERY.lower():
        return shutdownPC()
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
        responce = ask_gpt(
            "Your Jarivs from iron man, when i tell you anything, respond fast, just like jarivs: "
            + QUERY
        )
        t = threading.Thread(target=Read, args=[responce])
        t.start()
        return responce
