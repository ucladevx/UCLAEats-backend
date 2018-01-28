var express = require('express');
var routes = require('./routes');
var app = express(); 

var port = process.env.PORT || 3000;

app.use('/', routes);

app.listen(port, () => {
    console.log('App listening on port!');
});

