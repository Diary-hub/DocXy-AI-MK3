// The width and height of the captured photo. We will set the
// width to the value defined here, but the height will be
// calculated based on the aspect ratio of the input stream.

var width = 770; // We will scale the photo width to this
var height = 900; // This will be computed based on the input stream

// |streaming| indicates whether or not we're currently streaming
// video from the camera. Obviously, we start at false.

var streaming = false;

// The various HTML elements we need to configure or control. These
// will be set by the startup() function.

var video = null;
var canvas = null;
var photo = null;
faceName = null;
// var startbutton = null;

function setName(aa) {
    if (aa == null) {
        faceName.innerHTML = "No Faces Detected";

    } else if (aa != null & aa.toLowerCase() != "nainasm") {
        faceName.innerHTML = "Your Name Is: " + aa;

    } else {
        faceName.innerHTML = "Sorry, I Don't Know You";

    }

}

function startup() {
    video = document.getElementById('video');
    canvas = document.getElementById('canvas');
    photo = document.getElementById('photo');
    faceName = document.getElementById('faceName');
    // startbutton = document.getElementById('startbutton');

    navigator.mediaDevices.getUserMedia({
        video: true,
        audio: false
    })
        .then(function (stream) {
            video.srcObject = stream;
            video.play();
        })
        .catch(function (err) {
            console.log("An error occurred: " + err);
        });

    video.addEventListener('canplay', function (ev) {
        if (!streaming) {
            height = video.videoHeight / (video.videoWidth / width);

            // Firefox currently has a bug where the height can't be read from
            // the video, so we will make assumptions if this happens.

            if (isNaN(height)) {
                height = width / (4 / 3);
            }

            video.setAttribute('width', 340);
            video.setAttribute('height', 300);
            canvas.setAttribute('width', width);
            canvas.setAttribute('height', height);
            streaming = true;
        }
    }, false);

    // startbutton.addEventListener('click', function (ev) {
    //     takepicture();
    //     clearphoto();

    //     ev.preventDefault();
    // }, false);

    clearphoto();

    function every(x) {
        let last = new Date().getTime();

        (function loop() {
            const now = new Date().getTime(),
                delta = now - last;

            if (delta >= x) {
                takepicture()
                last = now;

            }

            window.requestAnimationFrame(loop);
        })();

    }
    every(1000)

}

// Fill the photo with an indication that none has been
// captured.

function clearphoto() {
    var context = canvas.getContext('2d');
    context.fillStyle = "#AAA";
    context.fillRect(0, 0, canvas.width, canvas.height);

    var data = canvas.toDataURL('image/png');
}

function takepicture() {
    var context = canvas.getContext('2d');
    if (width && height) {
        canvas.width = width;
        canvas.height = height;
        context.drawImage(video, 0, 0, width, height);

        var data = canvas.toDataURL('image/jpeg');
        let msg = {
            message: data
        };
        this.messages.push(msg);

        fetch("http://127.0.0.1:5000/WhoIsIt", {
            method: "POST",
            body: JSON.stringify({
                message: data
            }),
            mode: "cors",
            headers: {
                "Content-Type": "application/json",
            },
        })
            .then((r) => r.json())
            .then((r) => {
                let msg2 = {
                    message: r.answer
                };
                this.messages.push(msg2);
                setName(msg2['message']);

            })
            .catch((error) => {
                console.error("Error:", error);
            });

    } else {
        clearphoto();
    }
}

// once loading is complete.
window.addEventListener('load', startup, false);