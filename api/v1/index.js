const express = require('express');
const router = express.Router();
//var mongo0p = require("../../db/index.js");
const Menu = require('../../db').Menu;

router.use('/user', require('./user').router);
// router.use('/menu', require('./menu').router);
      
router.get('/menu', (req, res) => {
    res.send(file);
});

router.get('/test', (req, res) => {
    json_obj = {
        "test1": "Hello World",
        "test2": "Hi",
    };
    // Menu.create({menu: json_obj}).then(new_menu => {
    //     // console.log(Menu.findByID(new_menu.id).getMenu());
    // });
    Menu.findByID(4).then((menu) => {
        console.log(menu.getMenu());
    });
    res.send("Menu Creation Successful!");
});

	 
	   
/*
//use router.route if want to use POST as well (cuts redundancy)
router.get('/menu', (req, res) => {
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

module.exports = { router };
