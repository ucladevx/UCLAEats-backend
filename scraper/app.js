'use strict';
let scraper = require('./scraper');
let CronJob = require('cron').CronJob;
let tz = "America/Los_Angeles";
let moment = require('moment');
const Menu = require('../db').Menu;

// activity level runs every 5 minutes from 5:00am to 10:00pm everyday
let activityLevel = new CronJob({
    cronTime: "00 00-59/5 5-22 * * *",
    onTick: function() {
        // the object containig activity level
        let obj = scraper.getActivityLevel();
        // TODO: stringify and send it to database
        // console.log(obj);

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
        Menu.create({menu:obj}).then(new_menu => {
            console.log(new_menu.getDate());
        });
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
