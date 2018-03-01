const Sequelize = require('sequelize');

const logger = require('../logger');
const error = require('../error');
const config = require('../config');

const db = new Sequelize(
    config.database.db, 
    config.database.user, 
    config.database.pass, 
    {
        dialect: config.database.dialect,
        host: config.database.host,
        // logging: config.isDevelopment ? logger.debug : false,
    }
);
// console.log(db);

// const db = new Sequelize(config.database_url, {
//     dialect: config.database.dialect,
// });


// detailed_menu, overview_menu, activity level, hours

const OverviewMenu = require('./models/overviewmenu') (db, Sequelize);
const DetailedMenu = require('./models/detailedmenu') (db, Sequelize);
const ActLevel = require('./models/activitylevel') (db, Sequelize);
const Hours = require('./models/hours') (db, Sequelize);
const Recipe = require('./models/recipe') (db, Sequelize);

// Setup function
const setup = (force) => {
  const p = db.sync({ force }).catch(err => {
    logger.error(err);
    process.exit(1);
  });
};

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

module.exports = { db, setup, errorHandler, 
    DetailedMenu, OverviewMenu, ActLevel, Hours, Recipe, };
