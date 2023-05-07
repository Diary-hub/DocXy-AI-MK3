var speechRecognition = window.webkitSpeechRecognition

var recognition = new speechRecognition()

var text = $("#text")
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
    recognition.continuous = false
    recognition.stop()

}
recognition.onend = function () {
    console.log('Starting Again')

    recognition.start()
}
recognition.onerror = function () {
    text.text("Error Try Again")
    content = ''
    console.log('Error');

}

recognition.onresult = function (event) {
    var current = event.resultIndex

    var transcript = event.results[current][0].transcript
    content = transcript
    console.log(content)

    getResponce(content)
    content = ''
}

if (content.length) {
    content += ''
}
recognition.start()

$(document).ready(function () {

    boxes = document.querySelector(".warning-container")

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