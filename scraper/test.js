'use strict';
const scraper = require('./scraper');
const CronJob = require('cron').CronJob;
const tz = "America/Los_Angeles";
const moment = require('moment');
const OverviewMenu = require('../db').OverviewMenu;
const DetailedMenu = require('../db').DetailedMenu;
const ActLevel = require('../db').ActLevel;
const app = require('express')();

app.set('port', (process.env.PORT || 5000))
app.listen(app.get('port'), function() {
    console.log('running on port', app.get('port'))
});

app.get("/", function(req, res) {
    DetailedMenu.findAllByDate("2018-02-14").then(menu => {
        if(menu.length != 0) {
            res.send(menu[0].getDetailedMenu());
        }
        else 
            console.log("nh");
    });
});

// console.log(OverviewMenu.findAllByDate("2018-02-11").then(menu => {
//     if(menu.length != 0) {
//         console.log(menu[0].getOverviewMenu());
//         console.log("fsjfljsklfjsldkfjsdlk");
//     }
//     else 
//         console.log("nh");
// }));

// console.log(DetailedMenu.findAllByDate("2018-02-14").then(menu => {
//     if(menu.length != 0) {
//         console.log("here");
//         console.log(menu[0].getDetailedMenu());
//         console.log("fsjfljsklfjsldkfjsdlk");
//     }
//     else 
//         console.log("nh");
// }));