const fs = require('fs');
const env = process.env.NODE_ENV || "development";
const config = require('./.config.json');

module.exports = {
  isProduction: env === 'production',
  isDevelopment: env === 'development',

  host: process.env.HOST || '0.0.0.0',
  port: process.env.PORT || 5000,

  numCPUs: process.env.NUM_WORKERS || require('os').cpus().length,

    // database: config.database,
    // database_url: process.env.DATABASE_URL,
  database: {
	dialect: process.env.DB_DIALECT,
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    pass: process.env.DB_PASS,
    db: process.env.DB_NAME,
    devSetup: true,
  },

  // session: {
  //   secret: fs.readFileSync('app/config/SESSION_SECRET', 'utf-8'),
  // },

  logging: {
    level: 'debug',
    dbLevel: 'info',
  },
};
// module.exports = {
//     isProduction: (config.env == "production"),
//     isStaging: (config.env == "staging"),
//     isDevelopment: (config.env == "development"),

//     host: config.host,
//     port: config.port,

//     numCPUs: process.env.NUM_WORKERS || require("os").cpus().length,

//     database: config.database,
//     database_url: process.env.DATABASE_URL,

//     pepper: config.pepper,
//     logging: config.logging,
// }
