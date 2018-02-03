var express = require('express');
var routes = require('./routes');
var app = express(); 

var port = process.env.PORT || 3000;

app.use('/', routes);

app.listen(port, (err) => {
    if(err){
	console.log("error !", err);
    }
    
    console.log('App listening on port!');
});

