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