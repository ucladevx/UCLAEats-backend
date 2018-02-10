const express = require('express');
const router = express.Router();
//var mongo0p = require("../../db/index.js");
const OverviewMenu = require('../../db').OverviewMenu;
const moment = require('moment');

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
    // OverviewMenu.create({overviewMenu: json_obj}).then(new_menu => {
    //     console.log(new_menu.getOverviewMenu());
    // });
    // Menu.findByID(4).then((menu) => {
    //     console.log(menu.getMenu());
    // });
    // Menu.Delete(16).then(deleted_menu => {
    //     console.log(deleted_menu);
   // });
    let predate = moment().subtract(1,'hours');
    OverviewMenu.findByDateRange(predate.toDate(), moment().toDate()).then(menus => {
        console.log(menus);
    });
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
