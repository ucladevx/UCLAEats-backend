var express = require('express');
var app = 
var routes = express.Router();

var file = require('../json-file-here.json');

routes.get('/menu', (req, res) => {
    res.send(file);
});

module.exports = routes;
