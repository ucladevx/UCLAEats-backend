'use strict';
const scraper = require('./scraper');
const CronJob = require('cron').CronJob;
const tz = "America/Los_Angeles";
const moment = require('moment');
const OverviewMenu = require('../db').OverviewMenu;
const DetailedMenu = require('../db').DetailedMenu;
const ActLevel = require('../db').ActLevel;
const Hour = require('../db').Hours;
const Recipe = require('../db').Recipe;
// TODO: Add error handling in all scraper functions

// activity level runs every 5 minutes from 5:00am to 10:00pm everyday
let activityLevel = new CronJob({
    cronTime: "00 00-59/2 5-23 * * *",
    onTick: function() {
        // the object containig activity level
        console.log("inside activityLevel function");
        let obj = scraper.getActivityLevel();
        console.log(moment().format("YYYY-MM-DD"));
        ActLevel.create({level: obj}).then(level => {
            console.log("finished activity level");
            console.log(level);
        }).catch(err => {
            console.log("ActLevel Create FAiled.");
            console.log(err);
        });
    },
    start: false,
    timeZone: tz
});

// overviewPage runs everyday at 0:02 am
let overViewPage = new CronJob({
    cronTime: "00 02 00 * * *",
    onTick: function() {
        for(var i = 0; i <= 6; i++) {
            insertOverviewMenu(moment().add(i,'days').format("YYYY-MM-DD"));
        }
    },
    start: false,
    timeZone: tz
});

// detail page runs everyday at 0:04 am
let detailPage = new CronJob({
    cronTime: "00 04 00 * * *",
    onTick: function() {
        for(var i = 0; i <= 6; i++) {
            insertDetailMenu(moment().add(i,'days').format("YYYY-MM-DD"));
        }
    },
    start: false,
    timeZone: tz
});

// hours runs everyday at 0:06 am
let hours = new CronJob({
    cronTime: "00 06 00 * * *",
    onTick: function() {
        for(var i = 0; i <= 6; i++) {
            insertHours(moment().add(i,'days').format("YYYY-MM-DD"));
        }
    },
    start: false,
    timeZone: tz
});

function insertHours(queryDate) {
    console.log("Inside insertHours function for " + queryDate);

    Hour.findAllByDate(queryDate).then( hour => {
        if(hour.length == 0) {
            console.log("no hours data for " + queryDate);
            let obj = JSON.stringify(scraper.getHours(queryDate));
            Hour.create({hours: obj, hourDate: queryDate}).then( err => {
                if(!err)
                    console.log("finished insertion hour for " + queryDate);
                else {
                    console.log("error in insertHours function for date " + queryDate);
                    console.log(err);
                }
            });
        }
    });
    
}

function insertOverviewMenu(queryDate) {
    console.log("Inside insertOverviewMenu function for " + queryDate);

    OverviewMenu.findAllByDate(queryDate).then(menu => {
        if(menu.length == 0) {
            let obj = JSON.stringify(scraper.getOverviewPage(queryDate));
            OverviewMenu.create({overviewMenu:obj, menuDate: queryDate}).then(err => {
                if(!err)
                    console.log("finished insertion overViewMenu for " + queryDate);
                else {
                    console.log("error in insertOverViewMenu function for date " + queryDate);
                    console.log(err);
                }
            });
        }
    });
}
function insertDetailMenu(queryDate) {
    console.log("Inside insertDetailMenu function for " + queryDate);

    DetailedMenu.findAllByDate(queryDate).then(menu => {
        if(menu.length == 0) {
            let obj = {};
            var returned_arr1 = scraper.getDetailPage(queryDate, "Breakfast"); 
            obj["breakfast"] = returned_arr1[0]["breakfast"];
            var returned_arr2 = scraper.getDetailPage(queryDate, "Lunch");
            obj["lunch"] = returned_arr2[0]["lunch"];
            var returned_arr3 = scraper.getDetailPage(queryDate, "Dinner");
            obj["dinner"] = returned_arr3[0]["dinner"];
            obj = JSON.stringify(obj);
            var recipe_nutrition_dict = Object.assign({},returned_arr1[1],returned_arr2[1],returned_arr3[1]);
            DetailedMenu.create({detailedMenu:obj, menuDate: queryDate}).then(err => {
                Object.keys(recipe_nutrition_dict).forEach(function(key){
                    Recipe.findAllByRecipeLink(key).then(recipe => {
                        if(recipe.length == 0) {
                            Recipe.create({recipe_link:key, nutrition: recipe_nutrition_dict[key]}).then(err=> {
                                if(!err) 
                                    console.log("finished insertion recipe for " + key);
                                else {
                                    console.log("error in insertDetail function for recipe " + key);
                                    console.log(err); 
                                }
                            })
                        }
                    })
                });
                if(!err)
                    console.log("finished insertion detailedMenu for " + queryDate);
                else {
                    console.log("error in insertDetail function for date " + queryDate);
                    console.log(err);
                }
            });
        }
    });
}

function startAll() {
    activityLevel.start();
    overViewPage.start();
    detailPage.start();
    hours.start();
}

module.exports = {
    startAll
};  
