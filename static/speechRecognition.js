var speechRecognition = window.webkitSpeechRecognition;

var recognition = new speechRecognition();

var text = $("#text");
var wake = $("#wake");
var content = "";
var boxes = $(".warning-container");
var isWake = false;

recognition.continuous = true;

recognition.onstart = function () {
  text.text("Listening");
  console.log("listening");
};

recognition.onspeechend = function () {
  text.text("No Activity");
  content = "";
  recognition.continuous = false;
  recognition.stop();
};
recognition.onend = function () {
  
  if(!isWake){
    console.log("Starting Again");
    recognition.start();
  }else{
    recognition.abort()
  }
  
  
};
recognition.onerror = function () {
  text.text("Error Try Again");
  content = "";
  console.log("Error");
  recognition.stop();
};

recognition.onresult = function (event) {
  var current = event.resultIndex;

  var transcript = event.results[current][0].transcript;
  content = transcript;
  console.log(content);
  gg = content.toLowerCase()
  console.log(gg);
  if ( gg.includes('wake up')) {
    console.log('hi')
    var recognition2 = new speechRecognition();

    recognition.continuous = false;
    recognition2.continuous = true;
  
    isWake = true;
    recognition.stop()
    recognition2.start()

    recognition2.onstart = function () {
      text.text("Listening");
      console.log("listening 2 ");
    };

    recognition2.onspeechend = function () {
      text.text("No Activity 2");
      content = "";
      recognition2.continuous = false;
      recognition2.stop();
    };
    recognition2.onend = function () {
      console.log("Starting Again");
      recognition.continuous = true;

      recognition.start();
    };
    recognition2.onerror = function () {
      text.text("Error Try Again");
      content = "";
      console.log("Error");
      recognition2.stop();
    };

    recognition2.onresult = function (event) {
      var current = event.resultIndex;

      var transcript = event.results[current][0].transcript;
      content = transcript;
      console.log(content);

      getResponce(content);
      content = "";
    };
  }
  //   getResponce(content);
  content = "";
};

if (content.length) {
  content += "";
}
recognition.start();

$(document).ready(function () {
  boxes = document.querySelector(".warning-container");
  wake = document.querySelector("#wake");
});

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
      createWidget(r.answer);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

function createWidget(response) {
  var html = "";

  html +=
    '<div class="warning-box"><h2>Jarvis</h2><p>' + response + "</p></div>";
  boxes.innerHTML = html;
}
