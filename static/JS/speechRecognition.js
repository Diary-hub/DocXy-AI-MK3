var speechRecognition = window.webkitSpeechRecognition;

var recognition = new speechRecognition();

var text = $("#text");
var wake = $("#wake");
var content = "";
var prevContent = "";
var boxes = $(".warning-container");
var isWake = false;
var ListenEnded = false;
var isDiary;
wake = document.querySelector("#wake");
$(document).ready(function() {
    boxes = document.querySelector(".warning-container");
    wake = document.querySelector("#wake");

});

recognition.continuous = true;

recognition.onstart = function() {
    text.text("Listening");
    console.log("Waiting for Activation");
    wake.classList.add('active')

};

recognition.onspeechend = function() {
    text.text("No Activity for Activation");
    content = "";
    recognition.continuous = false;
    recognition.stop();
    wake.classList.add('active')

};
recognition.onend = function() {

    if (!isWake) {
        console.log("Starting Again: Waiting for Activation");
        wake.classList.add('active')

        recognition.start();
    } else {
        recognition.abort()
    }

};
recognition.onerror = function() {
    text.text("Error Try Again");
    content = "";
    console.log("Error");
    recognition.stop();
};

recognition.onresult = function(event) {
    if (isDiary) {
        var current = event.resultIndex;

        var transcript = event.results[current][0].transcript;
        content = transcript;
        console.log(content);
        gg = content.toLowerCase()
        if (gg.includes('wake up')) {
            console.log(getResponce("wake up"))
            var recognition2 = new speechRecognition();

            recognition.continuous = false;
            recognition2.continuous = true;

            isWake = true;
            wake.classList.add('active')
            recognition.stop()
            recognition2.start()

            recognition2.onstart = function() {
                text.text("Listening");
                console.log("listening...");
                wake.classList.add('active')
            };

            recognition2.onspeechend = function() {
                text.text("No Activity to Listen to");
                content = "";
                recognition2.continuous = false;
                recognition2.stop();
            };
            recognition2.onend = function() {
                console.log("Starting Again to Listen");
                recognition.continuous = true;

                recognition.start();
                isWake = false;
                wake.classList.add('unactive')
            };
            recognition2.onerror = function() {
                text.text("Error Try Again");
                content = "";
                console.log("Error");
                recognition2.stop();
            };

            recognition2.onresult = function(event) {
                if (!ListenEnded && isDiary) {
                    var current = event.resultIndex;

                    var transcript = event.results[current][0].transcript;
                    if (transcript.length > 5) {
                        ListenEnded = true;
                        content = transcript;
                        // if (prevContent.length > 5) {
                        //   content += ' ,check if your previous answer was related or not, then answer:  ' + prevContent;
                        // }
                        console.log(content);

                        getResponce(content);
                        content = "";
                    }
                } else if (!isDiary) {
                    createWidget("Your Not Authorized..!");
                }

            };
        }
        //   getResponce(content);
        content = "";
    } else {
        createWidget("Your Not Authorized...!");
    }
};

if (content.length) {
    content += "";
}
recognition.start();

this.messages = [];

function getResponce(query) {
    let msg = { message: query };
    this.messages.push(msg);

    fetch("http://127.0.0.1:5000/getResponse", {
            method: "POST",
            body: JSON.stringify({ message: query }),
            mode: "cors",
            headers: {
                "Content-Type": "application/json",
            },
        })
        .then((r) => r.json())
        .then((r) => {
            let msg2 = { message: r.answer };
            this.messages.push(msg2);
            prevContent = r.answer;
            createWidget(r.answer);
        })
        .catch((error) => {
            console.error("Error:", error);
        });
}

async function createWidget(response) {
    var html = "";

    html +=
        '<div class="warning-box " id="wake"><h2>Jarvis</h2><p>' + response + "</p></div>";
    boxes.innerHTML = html;
    ListenEnded = false;
}