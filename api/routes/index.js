const express = require('express');
const routes = express.Router();
//var mongo0p = require("../../db/index.js");
const Menu = require('../../db');
      
routes.get('/menu', (req, res) => {
    res.send(file);
});

routes.get('/test', (req, res) => {
    json_obj = {
        "test1": "Hello World",
        "test2": "Hi",
    };
    console.log(Menu);
    Menu.create({menu: json_obj}).then(new_menu => {
        console.log(new_menu);
    });
});

	 
	   
/*
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
*/

module.exports = routes;
