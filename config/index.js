const fs = require('fs');
const env = process.env.NODE_ENV || "development";
const config = require('./.config.json');

module.exports = {
    isProduction: (config.env == "production"),
    isStaging: (config.env == "staging"),
    isDevelopment: (config.env == "development"),

    host: process.env.HOST,
    port: config.port,

    numCPUs: process.env.NUM_WORKERS || require("os").cpus().length,

    database: config.database,
    pepper: config.pepper,
    logging: config.logging,
}
