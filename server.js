'use strict';

const express = require('express');
const config = require('./config');
const log = require('./logger');

// Constants
const PORT = config.port;

// App
const app = express();
app.get('/', (req, res) => {
  res.send('Hello world\n');
});

app.listen(PORT, () => {
    log.info("Started server on port %d, PID: %d", PORT, process.pid);
});
