var speechRecognition = window.webkitSpeechRecognition

var recognition = new speechRecognition()

var text = $("#start-btn")
var textarea = $("#text")
var content = ''
var boxes = $("#boxes")

recognition.continuous = true

recognition.onstart = function () {
    text.text("Listening")
}

recognition.onspeechend = function () {
    text.text("No Activity")
}
recognition.onerror = function () {
    text.text("Error Try Again")
}

recognition.onresult = function (event) {
    var current = event.resultIndex

    var transcript = event.results[current][0].transcript
    content = transcript
    getResponce(content)
}

$(document).ready(function () {
    if (content.length) {
        content += ''
    }

    boxes = document.querySelector("#boxes")

    recognition.start()
})

this.messages = [];

function getResponce(query) {
    let msg = { message: query }
    this.messages.push(msg)

    fetch('http://127.0.0.1:5000/getResponse', {
        method: 'POST',
        body: JSON.stringify({ message: query }),
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json'
        },
    })
        .then(r => r.json())
        .then(r => {
            let msg2 = { message: r.answer };
            this.messages.push(msg2);
            createWidget(r.answer)
        }).catch((error) => {
            console.error('Error:', error);
        })

}

function createWidget(response) {
    var html = '';

    html += '<div class="warning-box"><h2>Warning</h2><p>' + response + '</p></div>'
    boxes.innerHTML = html;
    console.log(html)
}