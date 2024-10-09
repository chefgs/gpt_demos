const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
require('dotenv').config();

const quizRoutes = require('./routes/quizRoutes');

const app = express();
app.use(cors());
app.use(express.json());

const uri = process.env.DATABASE_URL;
if (!uri) {
    throw new Error('DATABASE_URL environment variable is not defined');
}

// MongoDB connection
mongoose.connect(uri, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log('MongoDB connected'))
  .catch(err => console.log(err));

app.use('/api/quiz', quizRoutes);

const PORT = process.env.PORT || 6000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
