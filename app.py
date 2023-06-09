from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sys
from Functions import *


app = Flask(__name__)
CORS(app)


@app.get("/")
def index_get():
    return render_template("Main.html")


previous_questions_and_answers = []


@app.post("/getResponse")
def getResponse():
    text = request.get_json()
    # response = ask_gpt(text["message"])
    new_question = text["message"]
    allResponse = CheckForCommand(
        QUERY=new_question,
        previous_questions_and_answers=previous_questions_and_answers,
    )
    response = allResponse

    previous_questions_and_answers.append((new_question, response))
    print(previous_questions_and_answers, response)
    # response = Exam()
    # response = Carter_AI(text["message"])
    reply = {"answer": response}
    return jsonify(reply)


@app.route("/WhoIsIt", methods=["GET", "POST"])
def getfaces():
    text = request.get_json()
    response = Recognize(text["message"])
    reply = {"answer": response}
    return jsonify(reply)


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=False)

# http://10.242.192.9:5000
# http://127.0.0.1:5000
# http://localhost:5000
