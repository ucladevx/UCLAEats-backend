var routes = require('express').Router();
var file = require('../json-file-here.json');

routes.get('/', (req, res) => {
    res.send(file);
});

module.exports = routes;


