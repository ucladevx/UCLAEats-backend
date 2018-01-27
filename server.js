var express = require('express');
var app = express();
let router = express.Router();
var menu = require('menu-scraper');

var port = process.env.PORT || 8080;

//for use with POST
/*
var bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
*/

app.get('handle-fe', (req, res) => {
    res.sendfile(/*JSON*/);
});

//LISTENER
var listener = app.listen(port, function(){
    console.log('Express server listening on port');
});

//ERROR HANDLING
app.use((err, req, res, next) => {
   res.status(500).send('Something broke!');
})



