const express = require('express');
const config = require('./config');
console.log(config);
const log = require('./logger');
const db = require('./db');
const router = express('router');
const api = require('./api');
const scraper = require('./scraper');
scraper.startAll();

const app = express();
// Constants
const PORT = config.port;
const HOST = config.host;

app.use('/api', api.router);

app.get('/test', (req, res) => {
    res.send("Hello World!");
});

db.setup();
app.listen(PORT, HOST, () => {
    log.info("Started on server %s on port %d, PID: %d", HOST, PORT, process.pid);
});
