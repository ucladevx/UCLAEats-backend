'use strict';
const scraper = require('./scraper');
const CronJob = require('cron').CronJob;
const tz = "America/Los_Angeles";
const moment = require('moment');
const OverviewMenu = require('../db').OverviewMenu;
const DetailedMenu = require('../db').DetailedMenu;
const ActLevel = require('../db').ActLevel;
// TODO: detailedMenu and ActLevel
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
        // the object containig activity level
        // TODO: Add 7 days in advacne to scrape
        let dateString = moment().add(7,'days').format("YYYY-MM-DD");
        let obj = scraper.getOverviewPage(dateString);
        // obj["date"] = dateString;
        /*
        OverviewMenu.create({menu: obj}).then(err => {
            console.log(err);
        })*/
        // TODO: stringify and send it to database;

    },
    start: false,
    timeZone: tz
});

overViewPage.start();

// detail page runs everyday at 0:06 am
let detailPage = new CronJob({
    cronTime: "00 06 00 * * *",
    onTick: function() {
        // the object containig activity level
        let obj = {};
        let dateString = moment().add(7,'days').format("YYYY-MM-DD");
        obj["breakfast"] = (scraper.getDetailPage(dateString, "Breakfast"))["breakfast"];
        obj["lunch"] = scraper.getDetailPage(dateString, "Lunch")["lunch"];
        obj["dinner"] = scraper.getDetailPage(dateString, "Dinner")["dinner"];
        obj["date"] = dateString;
        // TODO: stringify and send it to database
        /*
        DetailedMenu.create({menu: obj}).then(err => {
            console.log(err);
        });
        */

    },
    start: false,
    timeZone: tz
});

detailPage.start();

// hours runs everyday at 0:07 am
let hours = new CronJob({
    cronTime: "00 07 00 * * *",
    onTick: function() {
        // the object containig activity level
        let dateString = moment().add(7,'days').format("YYYY-MM-DD");
        let obj = scraper.getHours(dateString);
        obj["date"] = dateString;
        // TODO: stringify and send it to database
        console.log(obj);

    },
    start: false,
    timeZone: tz
});
hours.start();
