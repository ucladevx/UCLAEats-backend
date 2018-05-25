const express = require('express');
const router = express.Router();

// router.use('/user', require('./user').router);
router.use('/menu', require('./menu').router);
      

module.exports = { router };
