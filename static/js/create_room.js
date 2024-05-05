const lobbyId = '123'; // This should be dynamically determined
const gameSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/game/' + lobbyId + '/'
);

gameSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log(data.message);
};

gameSocket.onclose = function(e) {
    console.error('Game socket closed unexpectedly');
};

document.querySelector('#myButton').onclick = function(e) {
    const message = {
        message: 'Hello, this is a test message.'
    };
    gameSocket.send(JSON.stringify(message));
};
