const express = require('express');
const app = express();
const router = express.Router();
const moment = require('moment');
const OverviewMenu = require('../../../db').OverviewMenu;
const DetailedMenu = require('../../../db').DetailedMenu;
const ActLevel = require('../../../db').ActLevel;
const Hours = require('../../../db').Hours;

const path = require("path");

router.use(express.static(__dirname + '/public'));

router.get('/nutritionfacts', (req, res) => {
    res.sendFile(path.join(__dirname + '/public/nutritionfacts.html'));
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

module.exports = { router };
