var util = require("util");
var net = require("net");

var jsonBufers = {};

//TODO this will need to be a buffer whee
function readData(data) {
    console.log('chunk');
    console.log(data);
    if (json_buffer == undefined) {
        json_buffer = data
    } else {
        json_buffer = json_buffer + data
    }

    parse_json();
};

function parse_json() {
    if (json_buffer != undefined) {
        try {
            var request = JSON.parse(json_buffer);
            processRequest(request);
            //clear the buffer or clear this buffer, probably will need one per client
        } catch (e) {
            console.log('no well formed JSON in this buffer');
            console.log(json_buffer);
        }
    };
};

function processRequest() {
};

function isRegistered() {
};



var server = net.createServer(function (socket) {
    socket.setEncoding('utf8');

    //jsonBufers[] = socket
    socket.write('hello\r\n');
    socket.pipe(socket);

    socket.on('data', readData); 

    
    console.log(socket.fd);
});

server.listen(8124, 'localhost');
