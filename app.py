from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sys
from Functions import *


app = Flask(__name__)
CORS(app)


@app.get("/")
def index_get():
    return render_template("Main.html")


@app.post("/getResponse")
def getResponse():
    text = request.get_json()
    # response = ask_gpt(text["message"])
    response = CheckForCommand(text["message"])
    # response = Exam()
    # response = Carter_AI(text["message"])
    reply = {"answer": response}
    return jsonify(reply)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)

# http://10.242.192.9:5000
# http://127.0.0.1:5000
# http://localhost:5000
