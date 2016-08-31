var thrift = require('node-thrift');

var Publish = require('./gen-nodejs/Publish.js'),
    ttypes = require('./gen-nodejs/bot_types.js');

var usuarios = [];

var server = thrift.createServer(Publish, {
  save: function(Qt, success) {
    console.log("El usuario :"+ Qt.user+ " con id: "+Qt.id);
    usuarios.push(Qt);
    console.log("y su pregunta: "+Qt.question);
    success();
  },

});

server.listen(9090);
