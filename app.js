const express = require('express');
const config = require('./config');
const log = require('./logger');
const router = express('router');
const api = require('./api');

const app = express();
// Constants
const PORT = config.port;
const HOST = config.host;

app.use('/api', api.router);

app.listen(PORT, HOST, () => {
    log.info("Started on server %s on port %d, PID: %d", HOST, PORT, process.pid);
});
