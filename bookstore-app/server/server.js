const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const morgan = require('morgan');
const promClient = require('prom-client');

const app = express();
const port = process.env.PORT || 5000;

// Prometheus metrics
const collectDefaultMetrics = promClient.collectDefaultMetrics;
collectDefaultMetrics({ timeout: 5000 });

// Create a Counter metric
const requestCounter = new promClient.Counter({
  name: 'bookstore_requests_total',
  help: 'Total number of requests',
  labelNames: ['method']
});

app.use(bodyParser.json());
app.use(morgan('tiny'));

// MongoDB connection
mongoose.connect('mongodb://localhost:27017/bookstore', { useNewUrlParser: true, useUnifiedTopology: true });

// Middleware to count requests
app.use((req, res, next) => {
  requestCounter.inc({ method: req.method });
  next();
});

// Routes
app.use('/books', require('./routes/books'));

// Prometheus metrics endpoint
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', promClient.register.contentType);
  res.end(await promClient.register.metrics());
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});