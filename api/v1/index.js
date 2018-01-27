const express = require('express');
let router = express.Router();
router.use('/menu-api', require('./menu-api'));

module.exports = {
    router
};
