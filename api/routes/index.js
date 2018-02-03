var express = require('express');
var routes = express.Router();
var mongo0p = require("../db/index.js");

//use routes.route if want to use POST as well (cuts redundancy)
routes.get('/menu', (req, res) => {
    var response = {};
    mongo0p.find({}, function(err, data){
	if(err){
	    response = {"error" : true,
			"message" : "Error fetching data"};
	}
	else{
	    response = {"error" : false,
			"message" : data};
	}
	res.json(response);
    });
});

module.exports = routes;
