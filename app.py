from flask import Flask, render_template, request, jsonify
from Functions import *

app = Flask(__name__)


@app.get("/")
def index_get():
    return render_template("Main.html")


@app.post("/getResponse")
def getResponse():
    text = request.get_json()
    # response = ask_gpt(text["message"])
    response = CheckForCommand(text["message"])
    reply = {"answer": response}
    return jsonify(reply)


if __name__ == "__main__":
    app.run(debug=True)
