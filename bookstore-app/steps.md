# This code and document has been created using ChatGPT 4o
# The bookstore application using the MERN stack (MongoDB, Express, React, Node.js) and set up monitoring with Prometheus and Grafana.

### Step 1: Set Up the Backend (Express and MongoDB)

#### Initialize the Project

1. Create a new directory for your project and navigate into it.
   ```sh
   mkdir bookstore
   cd bookstore
   ```

2. Initialize a new Node.js project.
   ```sh
   npm init -y
   ```

3. Install the necessary dependencies.
   ```sh
   npm install express mongoose body-parser morgan
   ```

#### Create the Backend Code

1. Create the following folder structure:
   ```
   bookstore/
   ├── server/
   │   ├── models/
   │   │   └── book.js
   │   ├── routes/
   │   │   └── books.js
   │   └── server.js
   └── package.json
   ```

2. Create the `Book` model in `server/models/book.js`:
   ```javascript
   const mongoose = require('mongoose');

   const bookSchema = new mongoose.Schema({
     title: String,
     author: String,
     price: Number
   });

   const Book = mongoose.model('Book', bookSchema);
   module.exports = Book;
   ```

3. Create the `books` routes in `server/routes/books.js`:
   ```javascript
   const express = require('express');
   const Book = require('../models/book');
   const router = express.Router();

   // Get all books
   router.get('/', async (req, res) => {
     const books = await Book.find();
     res.json(books);
   });

   // Add a new book
   router.post('/', async (req, res) => {
     const book = new Book(req.body);
     await book.save();
     res.status(201).json(book);
   });

   module.exports = router;
   ```

4. Create the main server file `server/server.js`:
   ```javascript
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
   ```

### Step 2: Set Up the Frontend (React)

#### Create the Frontend Code

1. Create a new React application inside your project directory.
   ```sh
   npx create-react-app client
   ```

2. Navigate into the React application directory.
   ```sh
   cd client
   ```

3. Install Axios for making HTTP requests.
   ```sh
   npm install axios
   ```

4. Create a simple UI to display and add books.

**App.js:**
```javascript
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const App = () => {
  const [books, setBooks] = useState([]);
  const [title, setTitle] = useState('');
  const [author, setAuthor] = useState('');
  const [price, setPrice] = useState('');

  useEffect(() => {
    axios.get('/books')
      .then(response => setBooks(response.data))
      .catch(error => console.error(error));
  }, []);

  const addBook = () => {
    axios.post('/books', { title, author, price })
      .then(response => setBooks([...books, response.data]))
      .catch(error => console.error(error));
  };

  return (
    <div>
      <h1>Bookstore</h1>
      <div>
        <input
          type="text"
          placeholder="Title"
          value={title}
          onChange={e => setTitle(e.target.value)}
        />
        <input
          type="text"
          placeholder="Author"
          value={author}
          onChange={e => setAuthor(e.target.value)}
        />
        <input
          type="number"
          placeholder="Price"
          value={price}
          onChange={e => setPrice(e.target.value)}
        />
        <button onClick={addBook}>Add Book</button>
      </div>
      <ul>
        {books.map(book => (
          <li key={book._id}>{book.title} by {book.author} - ${book.price}</li>
        ))}
      </ul>
    </div>
  );
};

export default App;
```

5. Update `package.json` to proxy API requests to the backend:
   ```json
   {
     "name": "client",
     "version": "0.1.0",
     "private": true,
     "dependencies": {
       "axios": "^0.21.1",
       "react": "^17.0.2",
       "react-dom": "^17.0.2",
       "react-scripts": "4.0.3"
     },
     "scripts": {
       "start": "react-scripts start",
       "build": "react-scripts build",
       "test": "react-scripts test",
       "eject": "react-scripts eject"
     },
     "proxy": "http://localhost:5000"
   }
   ```

6. Start the React application:
   ```sh
   npm start
   ```

### Step 3: Set Up Prometheus

1. Install Prometheus on your system. Follow the instructions on the [Prometheus download page](https://prometheus.io/download/).

2. Create a Prometheus configuration file `prometheus.yml`:
   ```yaml
   global:
     scrape_interval: 15s

   scrape_configs:
     - job_name: 'bookstore-backend'
       static_configs:
         - targets: ['localhost:5000']

     - job_name: 'mongodb-exporter'
       static_configs:
         - targets: ['localhost:9216']
   ```

3. Start Prometheus with the configuration file:
   ```sh
   ./prometheus --config.file=prometheus.yml
   ```

### Step 4: Set Up MongoDB Exporter

1. Download and run the MongoDB Exporter:
   ```sh
   wget https://github.com/percona/mongodb_exporter/releases/latest/download/mongodb_exporter-<version>.tar.gz
   tar xvfz mongodb_exporter-<version>.tar.gz
   ./mongodb_exporter --mongodb.uri mongodb://localhost:27017
   ```

### Step 5: Set Up Grafana

1. Install Grafana on your system. Follow the instructions on the [Grafana download page](https://grafana.com/get).

2. Start Grafana:
   ```sh
   ./bin/grafana-server
   ```

3. Open Grafana in your browser (`http://localhost:3000`), log in, and add Prometheus as a data source:
   - Go to **Configuration** > **Data Sources** > **Add data source**.
   - Select **Prometheus** and enter the Prometheus server URL (`http://localhost:9090`).
   - Click **Save & Test**.

4. Create a dashboard to visualize your metrics:
   - Click on **Create** > **Dashboard** > **Add new panel**.
   - Select the Prometheus data source and add queries for the metrics you want to visualize.

### Example Queries for Grafana

**Backend Metrics:**
```prometheus
rate(bookstore_requests_total[1m])
```

**Database Metrics:**
```prometheus
rate(mongodb_opcounters_insert_total[1m])
```

### Conclusion

This setup includes a MERN stack application with Prometheus and Grafana for monitoring. It covers setting up the backend with Express and MongoDB, the frontend with React, and the necessary configuration for Prometheus and Grafana to collect and visualize metrics. This approach helps in monitoring the performance and health of your bookstore application.