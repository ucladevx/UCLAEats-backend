const express = require('express');
const config = require('./config');
console.log(config);
const log = require('./logger');
const db = require('./db');
const router = express('router');
const api = require('./api');
const scraper = require('./scraper/app');
const exphbs  = require('express-handlebars');
const RateLimit = require('express-rate-limit');

scraper.startAll();

const app = express();
app.enable('trust proxy'); //for reverse proxy e.g. AWS

// Constants
const PORT = config.port;
const HOST = config.host;

app.engine('handlebars', exphbs({defaultLayout: 'main'}));
app.set('view engine', 'handlebars');

app.get('/test', (req, res) => {
    res.send("Hello World!");
});

app.use('/api', api.router);

db.setup();
app.listen(PORT, HOST, () => {
    log.info("Started on server %s on port %d, PID: %d", HOST, PORT, process.pid);
});


const apiLimiter = new RateLimit({
    windowMs: 15*60*1000, // 15 minutes
    max: 1000,
    delayMs: 0, // disabled
    delayAfter: 0
});

app.use('/public/', apiLimiter);
app.use('/public/', api.router);
