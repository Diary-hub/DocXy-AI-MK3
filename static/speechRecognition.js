var speechRecognition = window.webkitSpeechRecognition

var recognition = new speechRecognition()

var text = $("#start-btn")
var textarea = $("#text")
var content = ''
var boxes = $(".warning-container")

recognition.continuous = true

recognition.onstart = function () {
    text.text("Listening")
    console.log('listening')
}

recognition.onspeechend = function () {
    text.text("No Activity")
    content = ''
    location.reload()

}
recognition.onerror = function () {
    text.text("Error Try Again")
    content = ''
    location.reload()

}

recognition.onresult = function (event) {
    var current = event.resultIndex

    var transcript = event.results[current][0].transcript
    content = transcript
    console.log(content)

    getResponce(content)
    content = ''
}

$(document).ready(function () {
    if (content.length) {
        content += ''
    }

    boxes = document.querySelector(".warning-container")

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

    html += '<div class="warning-box"><h2>Jarvis</h2><p>' + response + '</p></div>'
    boxes.innerHTML = html;

}