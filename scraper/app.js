'use strict';
const scraper = require('scraper');
const CronJob = require('cron').CronJob;
const tz = "America/Los_Angeles";
const moment = require('moment');
const OverviewMenu = require('../db').OverviewMenu;
const DetailedMenu = require('../db').DetailedMenu;
const ActLevel = require('../db').ActLevel;
const Hour = require('../db').Hours;
// TODO: Add error handling in all scraper functions

// activity level runs every 5 minutes from 5:00am to 10:00pm everyday
let activityLevel = new CronJob({
    cronTime: "00-59/5 * 5-22 * * *",
    onTick: function() {
        // the object containig activity level
        let obj = scraper.getActivityLevel();
        ActLevel.create({level: obj}).then(err => {
            console.log(err);
        });
    },
    start: false,
    timeZone: tz
});

activityLevel.start();

// overviewPage runs everyday at 0:05 am
let overViewPage = new CronJob({
    cronTime: "00 05 00 * * *",
    onTick: function() {
        for(var i = 0; i <= 7; i++) {
            insertOverviewMenu(moment().add(i,'days').format("YYYY-MM-DD"));
        }
    },
    start: false,
    timeZone: tz
});

overViewPage.start();

// detail page runs everyday at 0:07 am
let detailPage = new CronJob({
    cronTime: "00 07 00 * * *",
    onTick: function() {
        for(var i = 0; i <= 7; i++) {
            insertDetailMenu(moment().add(i,'days').format("YYYY-MM-DD"));
        }
    },
    start: false,
    timeZone: tz
});

detailPage.start();


// hours runs everyday at 0:09 am
let hours = new CronJob({
    cronTime: "00 09 00 * * *",
    onTick: function() {
        for(var i = 0; i <= 7; i++) {
            insertHours(moment().add(i,'days').format("YYYY-MM-DD"));
        }
    },
    start: false,
    timeZone: tz
});

hours.start();

function insertHours(queryDate) {
    console.log(queryDate);

    Hour.findAllByDate(queryDate).then( hour => {
        if(hour.length == 0) {
            let obj = JSON.stringify(scraper.getHours(queryDate));
            Hour.create({hours: obj, hourDate: queryDate}).then( err => {
                if(!err)
                    console.log(queryDate.concat(" finished insertion"));
                else
                    console.log(err);
            });
        }
    });
    
}

function insertOverviewMenu(queryDate) {
    console.log(queryDate);
    OverviewMenu.findAllByDate(queryDate).then(menu => {
        if(menu.length == 0) {
            let obj = JSON.stringify(scraper.getOverviewPage(queryDate));
            OverviewMenu.create({overviewMenu:obj, menuDate: queryDate}).then(err => {
                if(!err)
                    console.log(queryDate.concat(" finished insertion"));
                else
                    console.log(err);
            });
        }
    });
}
function insertDetailMenu(queryDate) {
    console.log(queryDate);
    DetailedMenu.findAllByDate(queryDate).then(menu => {
        if(menu.length == 0) {
            let obj = {};
            obj["breakfast"] = scraper.getDetailPage(queryDate, "Breakfast")["breakfast"];
            obj["lunch"] = scraper.getDetailPage(queryDate, "Lunch")["lunch"];
            obj["dinner"] = scraper.getDetailPage(queryDate, "Dinner")["dinner"];
            obj = JSON.stringify(obj);
            DetailedMenu.create({detailedMenu:obj, menuDate: queryDate}).then(err => {
                if(!err)
                    console.log(queryDate.concat(" finished insertion"));
                else
                    console.log(err);
            });
        }
    });
}

