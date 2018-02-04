const express = require('express');
const config = require('./config');
const log = require('./logger');
const router = express('router');
const api = require('./api');

const app = express();
// Constants
const PORT = config.port;

app.use('/api', api.router);

app.listen(PORT, () => {
    log.info("Started server on port %d, PID: %d", PORT, process.pid);
});
