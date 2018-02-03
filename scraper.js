'use strict';
var _ = require('underscore')
var express = require('express')
var bodyParser = require('body-parser')
var request = require('request')
var util = require('util')
var cheerio = require('cheerio')
var tabletojson = require('tabletojson');
var fs = require('fs');
var apicache = require('apicache');
var sync_request = require('sync-request');

var cache = apicache.middleware;
var app = express()

/*
    If date is specified: Year-Month-Day (such as 2017-06-23 for June 23, 2017)

    To test with local file:
    var html = fs.readFileSync("html/test.html");
    parseMenus(res, html);

    Top of the HTML file MUST contain <!DOCTYPE html> in order to work!
*/

let hoursUrl = 'http://menu.dining.ucla.edu/Hours/%s'; // yyyy-mm-dd
let overviewUrl = 'http://menu.dining.ucla.edu/Menus/%s';
let BCafeUrl = 'http://menu.dining.ucla.edu/Menus/BruinCafe';
let Cafe1919Url = 'http://menu.dining.ucla.edu/Menus/Cafe1919';
let RendezvousUrl = 'http://menu.dining.ucla.edu/Menus/Rendezvous';
let DeNeveGrabNGoUrl = 'http://menu.dining.ucla.edu/Menus/DeNeveGrabNGo';
let HedrickStudyUrl = 'http://menu.dining.ucla.edu/Menus/HedrickStudy';

let cafes_url = {
    'bcafe': BCafeUrl,
    'cafe1919': Cafe1919Url,
    'rendezvous': RendezvousUrl,
    'deneve_grab_n_go': DeNeveGrabNGoUrl,
    'hedricks_study': HedrickStudyUrl
};


// URLs to test during summer development when websites are change
// const bcafeUrl = 'http://web.archive.org/web/20170416221050/http://menu.dining.ucla.edu/Menus/BruinCafe';
// const hedrickUrl = 'https://web.archive.org/web/20170616202351/http://menu.dining.ucla.edu/Menus/HedrickStudy';
// const deneveGrabUrl = 'https://web.archive.org/web/20170617043018/http://menu.dining.ucla.edu/Menus/DeNeveGrabNGo';
// const bplateGrabUrl = 'https://web.archive.org/web/20170616210053/http://menu.dining.ucla.edu/Menus/BruinPlateGrabNGoBreakfast';
// const deneveLateUrl = 'https://web.archive.org/web/20170617043009/http://menu.dining.ucla.edu/Menus/DeNeveLateNight';
// const bcafeUrl = 'http://menu.dining.ucla.edu/Menus/BruinCafe'
// const hedrickUrl = 'http://menu.dining.ucla.edu/Menus/HedrickStudy'
// const deNeveGrabHTML = 'http://menu.dining.ucla.edu/Menus/DeNeveGrabNGo'
// const bplateGrabUrl = 'http://menu.dining.ucla.edu/Menus/BruinPlateGrabNGoBreakfast'
// const deNeveLateHTML = 'http://menu.dining.ucla.edu/Menus/DeNeveLateNight'
// const rendezHTML = 'http://menu.dining.ucla.edu/Menus/Rendezvous'

//TODO: this url has changed let overviewUrl = 'http://menu.ha.ucla.edu/foodpro/default.asp?date=%d%%2F%d%%2F%d'
// const calendarUrl = 'http://www.registrar.ucla.edu/Calendars/Annual-Academic-Calendar'

let hallTitlesHours = [
    'Covel',
    'De Neve',
    'FEAST at Rieber',
    'Bruin Plate',
    'Bruin Café',
    'Café 1919',
    'Rendezvous',
    'De Neve Grab \'n\' Go',
    'The Study at Hedrick'
]

let breakfast_key = 'breakfast'
let lunch_key = 'lunch'
let dinner_key = 'dinner'
let late_night_key = 'late_night'
let limited_key = 'limited_menu'

app.set('port', (process.env.PORT || 5000))
app.use(bodyParser.urlencoded({extended: false}))
app.use(bodyParser.json())
app.use(express.static('website'))
app.use(express.static(__dirname + '/images'));

// Cache all routes. By default, the cache TTL is one hour
app.use(cache())
// Spin up the server
app.listen(app.get('port'), function() {
    console.log('running on port', app.get('port'))
})

// // this is useless for our app
// // app.get('/',function(req,res){
// //   res.sendFile(path.join(__dirname+'/index.html'));
// //   //__dirname : It will resolve to your project folder.
// // });
//
// // gives back the json for overview for each dinning hall
// /* Parameters:
//     Date (optional)
// */
// // to get the overview, call API like /overview?date=2018-01-28
// app.get('/hall/overview', function (req, res) {
//     var dateString = getDate(req, res)
//
//     var url = util.format(overviewUrl, dateString)
//     request(url, function(error, response, body) {
//         if (error) {
//             sendError(res, error)
//         } else {
//             parseOverviewPage(res, body)
//         }
//     })
// })
//
// // to get the detail page, call API like: /datail/Dinner?date=2018-01-28
// app.get('/hall/detail/:meal', function (req, res) {
//     var dateString = getDate(req, res)
//     var meal = req.params.meal.trim();
//
//     var url = util.format(overviewUrl, dateString) + '/' + meal;
//     request(url, function(error, response, body) {
//         if (error) {
//             sendError(res, error)
//         } else {
//             parseDetailPage(res, body)
//         }
//     });
//
//
// });
//
// /* Parameters:
//     Date (optional)
// */
// // to get the hours, call API like: /hours?date=2018-01-28
// app.get('/hours', function (req, res) {
//     var dateString = getDate(req, res)
//     var url = util.format(hoursUrl, dateString)
//     request(url, function(error, response, body) {
//         if (error) {
//             sendError(res, error)
//         } else {
//             parseHours(res, body)
//         }
//     })
// })
//
// app.get('/cafe/bcafe', function (req,res) {
//     var url = BCafeUrl;
//
//     request(url, function (error, response, body) {
//         if(error) {
//             sendError(res,error);
//         }
//         else {
//             parseCafe(res, body);
//         }
//     });
// });
//
// app.get('/cafe/cafe1919', function (req,res) {
//     var url = Cafe1919Url;
//
//     request(url, function (error, response, body) {
//         if(error) {
//             sendError(res,error);
//         }
//         else {
//             parseCafe(res, body);
//         }
//     });
// });
//
// app.get('/cafe/rendezvous', function (req,res) {
//     var url = RendezvousUrl;
//
//     request(url, function (error, response, body) {
//         if(error) {
//             sendError(res,error);
//         }
//         else {
//             parseCafe(res, body);
//         }
//     });
// });
//
// app.get('/cafe/denevegrabngo', function (req,res) {
//     var url = DeNeveGrabNGoUrl;
//
//     request(url, function (error, response, body) {
//         if(error) {
//             sendError(res,error);
//         }
//         else {
//             parseCafe(res, body);
//         }
//     });
// });
//
// app.get('/cafe/hedrickstudy', function (req,res) {
//     var url = HedrickStudyUrl;
//
//     request(url, function (error, response, body) {
//         if(error) {
//             sendError(res,error);
//         }
//         else {
//             parseCafe(res, body);
//         }
//     });
// });

// app.get('/calendarYear', function(req, res){
//     // TODO: get the calendar years for several
//     var url = util.format(calendarUrl);
//     request(url, function(error, response, body)
//     {
//         if (error)
//         {
//             sendError(res, error)
//         }
//         else{
//             res.send('TODO')
//         }
//     })
//     res.send('TODO');
// })

app.get('/testing', function(req,res) {
    var obj = getCafe('bcafe');
    res.send(obj);
})

function getActivityLevel() {
    var activity_level = {};
    var url = 'http://menu.dining.ucla.edu/Menus/';

    var $ = cheerio.load(sync_request('GET',url).getBody());

    var currElem = $(".meal-detail-link").first().next();
    while(currElem.hasClass('menu-block')) {
        var name = currElem.find("h3[class='col-header']").text().trim();
        var act = currElem.find(".activity-level-wrapper");
        if (act.length == 1) {
            activity_level[name] = act.parent().text().trim().replace(' ','').split(":").slice(-1)[0].trim();
        }
        else {
            activity_level[name] = "-1%";
        }

        currElem = currElem.next();
    }

    return JSON.stringify(activity_level);
}

function getOverviewPage(date) {
    var obj = {};
    var url = util.format(overviewUrl,date);

    var body = sync_request('GET',url).getBody();

    obj['breakfast'] = parseMealPeriod(body, 0);
    obj['brunch'] = parseMealPeriod(body,1);
    obj['lunch'] = parseMealPeriod(body, 2);
    obj['dinner'] = parseMealPeriod(body, 3);

    return JSON.stringify(obj);
}

function getDetailPage(date,meal) {
    var obj = {};
    var url = util.format(overviewUrl, date) + '/' + meal;

    var body = sync_request('GET',url).getBody();

    obj['breakfast'] = parseDetail(body, 0);
    obj['brunch'] = parseDetail(body,1);
    obj['lunch'] = parseDetail(body, 2);
    obj['dinner'] = parseDetail(body, 3);

    return JSON.stringify(obj);
}

function getHours(date) {
    var obj = {};
    var url = util.format(hoursUrl,date);

    var body = sync_request('GET',url).getBody();

    return parseHour(body);
}

function getCafe(cafe_name) {
    var obj = {};
    var url = cafes_url[cafe_name];

    var body = sync_request('GET',url).getBody();

    return parseCafe(body);
}

function parseOverviewPage(res, body) {
    var obj = {}

    obj['breakfast'] = parseMealPeriod(body, 0);
    obj['brunch'] = parseMealPeriod(body,1);
    obj['lunch'] = parseMealPeriod(body, 2);
    obj['dinner'] = parseMealPeriod(body, 3);

    obj = JSON.stringify(obj);

    res.send(obj)
}

function parseDetailPage(res, body) {
    var obj = {}

    obj['breakfast'] = parseDetail(body, 0);
    obj['brunch'] = parseDetail(body,1);
    obj['lunch'] = parseDetail(body, 2);
    obj['dinner'] = parseDetail(body, 3);

    obj = JSON.stringify(obj);

    res.send(obj);
}

function parseDetail(body, mealNumber) {
    var result = {}

    // load the html body
    var $ = cheerio.load(body)

    // this is for breakfast, lunch and dinner
    $("h2[id='page-header']").each(function(index, element){
        var text = $(this).text().trim()
        if (mealNumber == 0) {
            if (text.indexOf('Breakfast') == -1) {
                return
            }
        }
        else if (mealNumber == 1) {
            if (text.indexOf('Brunch') == -1) {
                return
            }
        }
        else if (mealNumber == 2) {
            if (text.indexOf('Lunch') == -1) {
                return
            }
        }
        else if (mealNumber == 3) {
            if (text.indexOf('Dinner') == -1) {
                return
            }
        }

        // go to the div with class menu-block and half-col
        // this is each dinning hall
        var currElem = $(this).next()
        // loop through all dinning halls
        while (currElem.hasClass('menu-block')){
            // the name for the dinning hall
            var name = currElem.find('h3')
            var sections = {}
            // find all subsections within each dinning hall
            var sectionNames = currElem.find('.sect-item')

            //scrape activity level
            // var act = currElem.find(".activity-level-wrapper");
            // if (act.length == 1) {
            //     sections['activity_level'] = act.parent().text().trim().replace(' ','').split(":").slice(-1)[0].trim();
            // }
            // else {
            //     sections['activity_level'] = "-1%";
            // }

            for (var h = 0; h < sectionNames.length; h++){
                // extract every subsections's name in each dinning hall
                var sectionName = sectionNames.eq(h).text()

                // find the name of subsection
                var ul_text = sectionNames.eq(h).find('.item-list').text();
                var ul_index = sectionName.indexOf(ul_text);

                // This is the name for each subsection in each dinning hall
                var match = sectionName.substring(0,ul_index).trim();
                // find the list of food within each subsection
                var itemList = sectionNames.eq(h).find('.menu-item')
                var items = []
                // loop through all food items
                for (var i = 0; i < itemList.length; i++){
                    // get the current subsection's food
                    var currItem = itemList.eq(i)
                    // get the food name
                    var itemName = currItem.find('.recipelink').text().trim()
                    // get the food hyperlink that contains all nutrition
                    var itemRecipe = currItem.find('.recipelink').attr('href')

                    var itemNames = {}
                    var itemCodesArr = {}
                    itemNames['name'] = itemName
                    itemNames['recipelink'] = itemRecipe
                    //get the code for important gradients (wheat, vegan, fish...)
                    var itemCodes = currItem.find('.tt-prodwebcode').find('img')
                    var itemCodesText = currItem.find('.tt-prodwebcode');
                    for (var j = 0; j < itemCodes.length; j++){
                        itemCodesArr[itemCodes.eq(j).attr('alt')] = (itemCodesText.eq(j).text().trim().split(' ')).join('_');
                    }
                    itemNames['itemcodes'] = itemCodesArr

                    //scrape nutrition
                    var nutritions = {};
                    parseNutrition(itemRecipe,nutritions);

                    itemNames['nutrition'] = nutritions;
                    items[i] = itemNames
                }

                // assign menu to each subsection
                sections[match] = items
            }

            // assign menu to each dinning hall
            result[name.text().trim()] = sections
            currElem = currElem.next()
        }
    })
    return result
}

function parseNutrition(nutrition_url, nutritions) {
    //scrape nutrition
    var $nutrition = cheerio.load(sync_request('GET',nutrition_url).getBody());

    // get the calory
    var currNur = $nutrition('.nfbox').find('.nfcal');
    var cal_arr = currNur.text().trim().split(' ');
    nutritions[cal_arr[0]] = parseInt(cal_arr[1]);
    nutritions[cal_arr[2]+'_'+cal_arr[3]] = parseInt(cal_arr[4]);

    // get all nutrition category
    var child = $nutrition(".nfbox p[class='nfnutrient']");

    for(var j = 0; j < child.length; j++) {
        var text = child.eq(j).text().trim().split(' ');

        var index = 0;
        for(var p = 0; p < text.length; p++) {
            if((text[p][0] >= '0' && text[p][0] <= '9') || text[p][0] == '-') {
                index = p;
                break;
            }
        }

        // get nutrition name
        var nutrition_name = text.slice(0,index).join('_');
        nutritions[nutrition_name] = ['-1g','-1%'];
        // if there is a percentage field
        if(text.length - index > 1) {
            if(('-'.indexOf(text[-1]) == -1) && ('-'.indexOf(text[-2]) == -1))
                nutritions[nutrition_name][0] = text[index];
                nutritions[nutrition_name][1] = text[index+1];
        }
        else {
            if('-'.indexOf(text[-1]) == -1)
                nutritions[nutrition_name][0] = text[index];
        }

    }

    // get Viatamin
    child = $nutrition('.nfvit span');
    for(var j = 0; j < child.length; j++) {
        if('nfvitname'.indexOf(child.eq(j).attr('class')) != -1) {
            var vit_name = child.eq(j).text().trim();
            j++;
            nutritions[vit_name] = child.eq(j).text().trim();
        }
    }

    // get ingredients
    child = $nutrition('.ingred_allergen p');
    if(child.length >= 1) {
        nutritions['ingredients'] = child.eq(0).text().trim().split(":").slice(-1)[0].trim();
    }
    else {
        nutritions['ingredients'] = '';
    }
}

function parseMealPeriod(body, mealNumber) {
    var result = {}

    // load the html body
    var $ = cheerio.load(body)

    // this is for breakfast, lunch and dinner
    $('.meal-detail-link').each(function(index, element){
        var text = $(this).text().trim()
        if (mealNumber == 0) {
            if (text.indexOf('Breakfast') == -1) {
                return
            }
        }
        else if (mealNumber == 1) {
            if (text.indexOf('Brunch') == -1) {
                return
            }
        }
        else if (mealNumber == 2) {
            if (text.indexOf('Lunch') == -1) {
                return
            }
        }
        else if (mealNumber == 3) {
            if (text.indexOf('Dinner') == -1) {
                return
            }
        }

        // go to the div with class menu-block and half-col
        // this is each dinning hall
        var currElem = $(this).next()
        // loop through all dinning halls
        while (currElem.hasClass('menu-block')){
            // the name for the dinning hall
            var name = currElem.find('h3')
            var sections = {}
            // find all subsections within each dinning hall
            var sectionNames = currElem.find('.sect-item')

            //scrape activity level
            // var act = currElem.find(".activity-level-wrapper");
            // if (act.length == 1) {
            //     sections['activity_level'] = act.parent().text().trim().replace(' ','').split(":").slice(-1)[0].trim();
            // }
            // else {
            //     sections['activity_level'] = "-1%";
            // }

            for (var h = 0; h < sectionNames.length; h++){
                // This is the text of div of a subsection
                var sectionName = sectionNames.eq(h).text()

                // find the name of subsection
                var ul_text = sectionNames.eq(h).find('.item-list').text();
                var ul_index = sectionName.indexOf(ul_text);

                // This is the name for each subsection in each dinning hall
                var match = sectionName.substring(0,ul_index).trim();
                // find the list of food within each subsection
                var itemList = sectionNames.eq(h).find('.menu-item')
                var items = []
                // loop through all food items
                for (var i = 0; i < itemList.length; i++){
                    // get the current subsection's food
                    var currItem = itemList.eq(i)
                    // get the food name
                    var itemName = currItem.find('.recipelink').text().trim()
                    // get the food hyperlink that contains all nutrition
                    var itemRecipe = currItem.find('.recipelink').attr('href')

                    var itemNames = {}
                    var itemCodesArr = {}
                    itemNames['name'] = itemName
                    itemNames['recipelink'] = itemRecipe
                    //get the code for important gradients (wheat, vegan, fish...)
                    var itemCodes = currItem.find('.tt-prodwebcode').find('img')
                    var itemCodesText = currItem.find('.tt-prodwebcode');
                    for (var j = 0; j < itemCodes.length; j++){
                        itemCodesArr[itemCodes.eq(j).attr('alt')] = (itemCodesText.eq(j).text().trim().split(' ')).join('_');
                        //console.log(currItem.find('.tt-prodwebcode').text().trim());
                    }
                    itemNames['itemcodes'] = itemCodesArr

                    //scrape nutrition
                    var nutritions = {};
                    parseNutrition(itemRecipe,nutritions);

                    itemNames['nutrition'] = nutritions;
                    items[i] = itemNames
                }

                // assign menu to each subsection
                sections[match] = items
            }

            // assign menu to each dinning hall
            result[name.text().trim()] = sections
            currElem = currElem.next()
        }
    })
    return result
}

// this is used for function getHours
function parseHour(body) {
    var response = []
    var obj = {}

    var $ = cheerio.load(body)
    $('.hours-location, .hours-range, .hours-closed, .hours-closed-allday').each(function(index, element){
        var text = $(this).text().trim()
        if (hallTitlesHours.indexOf(text) != -1){
            if (!_.isEmpty(obj)){
                response.push(obj)
            }
            obj = {}
            obj['hall_name'] = text
            return
        }
        if (dinner_key in obj) {
            obj[late_night_key] = text
        } else if (lunch_key in obj) {
            obj[dinner_key] = text
        } else if (breakfast_key in obj) {
            obj[lunch_key] = text
        } else {
            obj[breakfast_key] = text
        }
    })

    response.push(obj)

    return JSON.stringify(response);
}

// function parseHours(res, body) {
//     var response = []
//     var obj = {}
//
//     var $ = cheerio.load(body)
//     $('.hours-location, .hours-range, .hours-closed, .hours-closed-allday').each(function(index, element){
//         var text = $(this).text().trim()
//         if (hallTitlesHours.indexOf(text) != -1){
//             if (!_.isEmpty(obj)){
//                 response.push(obj)
//             }
//             obj = {}
//             obj['hall_name'] = text
//             return
//         }
//         if (dinner_key in obj) {
//             obj[late_night_key] = text
//         } else if (lunch_key in obj) {
//             obj[dinner_key] = text
//         } else if (breakfast_key in obj) {
//             obj[lunch_key] = text
//         } else {
//             obj[breakfast_key] = text
//         }
//     })
//
//     response.push(obj)
//
//     response = JSON.stringify(response);
//
//     res.send(response)
// }

function parseCafe(body) {
    var response = {};
    var $ = cheerio.load(body);

    // get the name of navigation button
    $('.page-nav-button').each(function(index, element) {
        response[$(this).text()] = [];
    });

    // each swiper slide is the content for a navigation bar
    $('.swiper-slide').each(function(index, element) {
        var arr = [];
        var items = $(this).find('.menu-item');
        for (var i = 0; i < items.length; i++) {
            var itemInfo = {};
            if (items.eq(i).find('.recipelink').length == 0)
                continue;
            // name
            itemInfo['name'] = items.eq(i).find('.recipelink').text().trim();
            // recipelink
            itemInfo['recipelink'] = items.eq(i).find('.recipelink').attr('href');
            var itemRecipe = itemInfo['recipelink'];
            // description
            var itemDescript = items.eq(i).find('.menu-item-description').text().trim();
            if (itemDescript != '')
                itemInfo['itemDescription'] = itemDescript;
            else
                itemInfo['itemDescription'] = "No description provided";
            // web-code
            var itemCodesArr = []
            var itemCodes = items.eq(i).find('.webcode');
            for (var j = 0; j < itemCodes.length; j++){
                itemCodesArr[j] = itemCodes.eq(j).attr('alt');
            }
            itemInfo['itemCodes'] = itemCodesArr;
            // cost
            var itemCost = items.eq(i).find('.menu-item-price').text().trim();
            if (itemCost != '')
                itemInfo['itemCost'] = itemCost;
            else
                itemInfo['itemCost'] = "No cost provided";

            //scrape nutrition
            var nutritions = {};
            parseNutrition(itemRecipe, nutritions);

            itemInfo['nutrition'] = nutritions;
            arr.push(itemInfo);
        }

        response[Object.keys(response)[index]] = arr;
    });

    return JSON.stringify(response);
}

// function parseCafe(res, body) {
//     var response = {};
//     var $ = cheerio.load(body);
//
//     // get the name of navigation button
//     $('.page-nav-button').each(function(index, element) {
//         response[$(this).text()] = [];
//     });
//
//     // each swiper slide is the content for a navigation bar
//     $('.swiper-slide').each(function(index, element) {
//         var arr = [];
//         var items = $(this).find('.menu-item');
//         for (var i = 0; i < items.length; i++) {
//             var itemInfo = {};
//             if (items.eq(i).find('.recipelink').length == 0)
//                 continue;
//             // name
//             itemInfo['name'] = items.eq(i).find('.recipelink').text().trim();
//             // recipelink
//             itemInfo['recipelink'] = items.eq(i).find('.recipelink').attr('href');
//             var itemRecipe = itemInfo['recipelink'];
//             // description
//             var itemDescript = items.eq(i).find('.menu-item-description').text().trim();
//             if (itemDescript != '')
//                 itemInfo['itemDescription'] = itemDescript;
//             else
//                 itemInfo['itemDescription'] = "No description provided";
//             // web-code
//             var itemCodesArr = []
//             var itemCodes = items.eq(i).find('.webcode');
//             for (var j = 0; j < itemCodes.length; j++){
//                 itemCodesArr[j] = itemCodes.eq(j).attr('alt');
//             }
//             itemInfo['itemCodes'] = itemCodesArr;
//             // cost
//             var itemCost = items.eq(i).find('.menu-item-price').text().trim();
//             if (itemCost != '')
//                 itemInfo['itemCost'] = itemCost;
//             else
//                 itemInfo['itemCost'] = "No cost provided";
//
//             //scrape nutrition
//             var nutritions = {};
//             parseNutrition(itemRecipe, nutritions);
//
//             itemInfo['nutrition'] = nutritions;
//             arr.push(itemInfo);
//         }
//
//         response[Object.keys(response)[index]] = arr;
//     });
//
//     response = JSON.stringify(response);
//
//     return res.send(response);
// }

//
// app.get('/cafes', function (req, res){
//     var deNeveGrabHTML = fs.readFileSync("html/denevegrabngo.html")
//     var hedrickStudyHTML = fs.readFileSync("html/hedrickstudy.html")
//     var cf1919HTML = fs.readFileSync("html/1919.html")
//     var bcafeHTML = fs.readFileSync("html/bcafe.html")
//     var bplateGrabHTML = fs.readFileSync("html/bplategrabngobreakfast.html")
//     var deNeveLateHTML = fs.readFileSync("html/denevelatenight.html")
//     var rendezHTML = fs.readFileSync("html/rendezvous.html")
//
//     var resp = {}
//     resp['Cafe-1919'] = parseCafe(cf1919HTML)
//     resp['DeNeve-GrabNGo'] = parseCafe(deNeveGrabHTML)
//     resp['DeNeve-LateNight'] = parseCafe(deNeveLateHTML)
//     resp['Bruin-Cafe'] = parseCafe(bcafeHTML)
//     resp['BruinPlate-GrabNGoBreakfast'] = parseCafe(bplateGrabHTML)
//     resp['Hedrick-Study'] = parseCafe(hedrickStudyHTML)
//     resp['Rendezvous'] = parseCafe(rendezHTML)
//     res.send(resp)
// })

function sendError(res, error) {
    console.log(error)
    res.send(error)
}

function getDate(req, res) {
    let dateText = req.query['date']
    if (dateText) {
        return dateText //new Date(dateText)
        // TODO: Catch invalid dateText format and send appropriate error message on incorrect format
    }
    let date = new Date()
    let month = date.getMonth() + 1 //getMonth returns 0 based month
    let day = date.getDate()
    let year = date.getFullYear()
    return '' + year + '-' + minTwoDigits(month) + '-' + minTwoDigits(day)
}

function minTwoDigits(n) {
  return (n < 10 ? '0' : '') + n;
}

// TODO: Have a job that runs every hour that refreshes all the menus
// TODO: Store about a week's worth of menu info
