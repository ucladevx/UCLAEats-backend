const express = require('express');
const app = express();
const router = express.Router();
const moment = require('moment');
const OverviewMenu = require('../../../db').OverviewMenu;
const DetailedMenu = require('../../../db').DetailedMenu;
const ActLevel = require('../../../db').ActLevel;
const Hours = require('../../../db').Hours;
const Recipe = require('../../../db').Recipe;

const path = require("path");

router.use(express.static(__dirname + '/public'));

router.get('/nutritionfacts', (req, res) => {
    res.sendFile(path.join(__dirname + '/public/nutritionfacts.html'));
});

// to query nutrition, for recipe link like http://menu.dining.ucla.edu/Recipes/075000/1,
// extract 075000/1 and then do /nutrition?recipe_link=075000/1
router.get('/nutrition', (req, res) => {
    Recipe.findAllByRecipeLink(req.query.recipe_link).then(recipes => {
        res.json({recipes});

        if (recipes.length >= 1) {
            var recipe = recipes[0];
            if (!("nutrition" in Object.keys(recipe)) || (Object.keys(recipe["nutrition"].length == 0)))
                res.render("<h1>Item does not have nutrition information</h1>");
            else {
                var context = {};
                populate_context(recipe,context);
                res.render(path.join(__dirname + '/public/nutritionfacts.html'),context);
            }
        }
        else
            res.render("<h1>Item not found</h1>");
    })
});

// Get overview menu from today til the next 7 days
router.get('/OverviewMenu', (req, res) => {
    let startDate = moment().format("YYYY-MM-DD");
    let endDate = moment().add(7, 'days').format("YYYY-MM-DD");
    OverviewMenu.findAllByDateRange(startDate,endDate).then(menus => {
        res.json({ menus });
    });
    // OverviewMenu.findAllByDate(endDate).then(menus => {
    //     res.json({menus});
    // });
});

router.get('/DetailedMenu', (req, res) => {
    let startDate = moment().startOf('day').toDate();
    let endDate = moment().startOf('day').add(7, 'days').toDate();
    DetailedMenu.findAllByDateRange(startDate,endDate).then(menus => {
        res.json({ menus });
    });
});

router.get('/ActivityLevels', (req, res) => {
    ActLevel.findLast().then(level => {
        res.json({ level });
    });
});

router.get('/Hours', (req, res) => {
    let startDate = moment().startOf('day').toDate();
    let endDate = moment().startOf('day').add(7, 'days').toDate();

    Hours.findByAllDateRange(startDate,endDate).then(hours => {
        res.json({hours});
    });
});

// Test functions, for functionality
router.get('/test', (req, res) => {
    // let json_obj = {
    //     "test1": "Hello World",
    //     "test2": "Hi",
    // };
    // let date = moment().add(7, 'days').format("YYYY-MM-DD");
    // OverviewMenu.create({overviewMenu: json_obj, menuDate:date}).then(new_menu => {
    //     console.log(new_menu.getOverviewMenu());
    // });
    // let predate = moment().subtract(1,'hours');
    // OverviewMenu.findAllByDateRange(predate.toDate(), moment().toDate()).then(menus => {
    //     console.log(menus);
    // });
    OverviewMenu.findByID(1).then(new_menu => {
        console.log(new_menu.getOverviewMenu());
    });
});

function populate_context(recipe, context) {
    var recipe_keys = Object.keys(recipe);

    if("serving_size" in recipe_keys)
        context["serving_size"] = recipe["serving_size"];
    else
        context["serving_size"] = "--";
    
    if("Calories" in recipe_keys)
        context["Calories"] = recipe["Calories"];
    else
        context["Calories"] = "--";

    if("Fat_Cal." in recipe_keys)
        context["Fat_Cal."] = recipe["Fat_Cal."];
    else
        context["Fat_Cal."] = "--";

    if("Total_Fat" in recipe_keys) {
        context["Total_Fat_g"] = (recipe["Total_Fat"][0][0] == "-" ? "--" : recipe["Total_Fat"][0]);
        context["Total_Fat_p"] = (recipe["Total_Fat"][1][0] == "-" ? "--" : recipe["Total_Fat"][1]);
    }
    else {
        context["Total_Fat_g"] = "--";
        context["Total_Fat_p"] = "--";
    }

    if("Saturated_Fat" in recipe_keys) {
        context["Saturated_Fat_g"] = (recipe["Saturated_Fat"][0][0] == "-" ? "--" : recipe["Saturated_Fat"][0]);
        context["Saturated_Fat_p"] = (recipe["Saturated_Fat"][1][0] == "-" ? "--" : recipe["Saturated_Fat"][1]);
    }
    else {
        context["Saturated_Fat_g"] = "--";
        context["Saturated_Fat_p"] = "--";
    }

    if("Trans_Fat" in recipe_keys) {
        context["Trans_Fat_g"] = (recipe["Trans_Fat"][0][0] == "-" ? "--" : recipe["Trans_Fat"][0]);
    }
    else {
        context["Trans_Fat_g"] = "--";
    }

    if("Cholesterol" in recipe_keys) {
        context["Cholesterol_g"] = (recipe["Cholesterol"][0][0] == "-" ? "--" : recipe["Cholesterol"][0]);
        context["Cholesterol_p"] = (recipe["Cholesterol"][1][0] == "-" ? "--" : recipe["Cholesterol"][1]);
    }
    else {
        context["Cholesterol_g"] = "--";
        context["Cholesterol_p"] = "--";
    }

    if("Sodium" in recipe_keys) {
        context["Sodium_g"] = (recipe["Sodium"][0][0] == "-" ? "--" : recipe["Sodium"][0]);
        context["Sodium_p"] = (recipe["Sodium"][1][0] == "-" ? "--" : recipe["Sodium"][1]);
    }
    else {
        context["Sodium_g"] = "--";
        context["Sodium_p"] = "--";
    }

    if("Total_Carbohydrate" in recipe_keys) {
        context["Total_Carbohydrate_g"] = (recipe["Total_Carbohydrate"][0][0] == "-" ? "--" : recipe["Total_Carbohydrate"][0]);
        context["Total_Carbohydrate_p"] = (recipe["Total_Carbohydrate"][1][0] == "-" ? "--" : recipe["Total_Carbohydrate"][1]);
    }
    else {
        context["Total_Carbohydrate_g"] = "--";
        context["Total_Carbohydrate_p"] = "--";
    }

    if("Dietary_Fiber" in recipe_keys) {
        context["Dietary_Fiber_g"] = (recipe["Dietary_Fiber"][0][0] == "-" ? "--" : recipe["Dietary_Fiber"][0]);
        context["Dietary_Fiber_p"] = (recipe["Dietary_Fiber"][1][0] == "-" ? "--" : recipe["Dietary_Fiber"][1]);
    }
    else {
        context["Dietary_Fiber_g"] = "--";
        context["Dietary_Fiber_p"] = "--";
    }

    if("Sugars" in recipe_keys) {
        context["Sugars_g"] = (recipe["Sugars"][0][0] == "-" ? "--" : recipe["Sugars"][0]);
    }
    else {
        context["Sugars_g"] = "--";
    }

    if("Protein" in recipe_keys) {
        context["Protein_g"] = (recipe["Protein"][0][0] == "-" ? "--" : recipe["Protein"][0]);
    }
    else {
        context["Protein_g"] = "--";
    }

    if("Vitamin A" in recipe_keys)
        context["VA_p"] = (recipe["Vitamin A"][0] == "-" ? "--" : recipe["Vitamin A"]);
    else
        context["VA_p"] = "--";

    if("Vitamin C" in recipe_keys)
        context["VC_p"] = (recipe["Vitamin C"][0] == "-" ? "--" : recipe["Vitamin C"]);
    else
        context["VC_p"] = "--";

    if("Calcium" in recipe_keys)
        context["Cal_p"] = (recipe["Calcium"][0] == "-" ? "--" : recipe["Calcium"]);
    else
        context["Cal_p"] = "--";

    if("Iron" in recipe_keys)
        context["Iron"] = (recipe["Iron"][0] == "-" ? "--" : recipe["Iron"]);
    else
        context["Iron"] = "--";

    if("ingredients" in recipe_keys)
        context["ingredients"] = recipe["ingredients"].trim();
    else
        context["ingredients"] = "--";

    if("allergens" in recipe_keys)
        context["allergens"] = recipe["allergens"].trim();
    else
        context["allergens"] = "--";

}

module.exports = { router };
