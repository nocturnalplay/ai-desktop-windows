var socket = new WebSocket("ws://localhost:3333/ws");

socket.onopen = function (e) {
  socket.onmessage = function (event) {
    console.log(event);
  };
};

function Hand() {
  socket.send(JSON.stringify({ event: "hand", data: "eye access" }));
}

function Eye() {
  socket.send(JSON.stringify({ event: "eye", data: "eye access" }));
}

function Voice() {
  socket.send(JSON.stringify({ event: "voice", data: "eye access" }));
}
