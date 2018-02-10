const Sequelize = require('sequelize');

const logger = require('../logger');
const error = require('../error');
const config = require('../config');

const db = new Sequelize(
    config.database.name, 
    config.database.user, 
    config.database.password, 
    {
        dialect: config.database.dialect,
        host: config.database.host,
        logging: config.isDevelopment ? logger.debug : false,
    }
);

// detailed_menu, overview_menu, activity level, hours

const OverviewMenu = require('./models/overview_menu') (db, Sequelize);
const DetailedMenu = require('./models/detailedmenu') (db, Sequelize);
const ActLevel = require('./models/activitylevel') (db, Sequelize);

/**
 * Handles database errors (separate from the general error handler and the 404 error handler)
 *
 * Specifically, it intercepts validation errors and presents them to the user in a readable
 * manner. All other errors it lets fall through to the general error handler middleware.
 */
const errorHandler = (err, req, res, next) => {
    if (!err || !(err instanceof Sequelize.Error))
        return next(err);
    if (err instanceof Sequelize.ValidationError) {
        const message = `Validation Error: ${err.errors.map(e => e.message).join('; ')}`;
        return next(new error.HTTPError(err.name, 422, message))
    }
    return next(new error.HTTPError(err.name, 500, err.message));
};

module.exports = { db, OverviewMenu, errorHandler, ActLevel };
