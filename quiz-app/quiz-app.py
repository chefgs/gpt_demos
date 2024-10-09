import os

# Define the folder structure for the quiz app
folder_structure = {
    'quiz-app': {
        'backend': {
            'routes': {
                'quizRoutes.js': '''\
const express = require('express');
const Quiz = require('../models/quizModel');
const router = express.Router();

router.post('/add', async (req, res) => {
  try {
    const { question, answers, correctAnswer, category, difficulty } = req.body;

    if (!question || !answers || !correctAnswer || !category || !difficulty) {
      return res.status(400).json({ message: 'All fields are required' });

    if (!answers.includes(correctAnswer)) {
      return res.status(400).json({ message: 'Correct answer must be one of the provided answers' });
    }

    const newQuiz = new Quiz({
      question,
      answers,
      correctAnswer,
      category,
      difficulty,
    });

    await newQuiz.save();
    res.status(201).json({ message: 'Quiz question added successfully' });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Server error' });
  }
});

module.exports = router;
''',
            },
            'models': {
                'quizModel.js': '''\
const mongoose = require('mongoose');

const quizSchema = new mongoose.Schema({
  question: {
    type: String,
    required: true,
  },
  answers: {
    type: [String],
    required: true,
  },
  correctAnswer: {
    type: String,
    required: true,
  },
  category: {
    type: String,
    required: true,
  },
  difficulty: {
    type: String,
    enum: ['easy', 'medium', 'hard'],
    required: true,
  },
}, { timestamps: true });

module.exports = mongoose.model('Quiz', quizSchema);
''',
            },
            'server.js': '''\
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
require('dotenv').config();

const quizRoutes = require('./routes/quizRoutes');

const app = express();
app.use(cors());
app.use(express.json());

// MongoDB connection
mongoose.connect(process.env.MONGO_URI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log('MongoDB connected'))
  .catch(err => console.log(err));

app.use('/api/quiz', quizRoutes);

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
''',
            },
            '.env': '''\
MONGO_URI=mongodb://localhost:27017/quizAppDB
''',
            'package.json': '''\
{
  "name": "quiz-backend",
  "version": "1.0.0",
  "main": "server.js",
  "scripts": {
    "start": "node server.js"
  },
  "dependencies": {
    "express": "^4.17.1",
    "mongoose": "^5.12.3",
    "cors": "^2.8.5",
    "dotenv": "^8.2.0"
  }
}
'''
        },
        'frontend': {
            'src': {
                'components': {
                    'AddQuestion.js': '''\
import React, { useState } from 'react';
import axios from 'axios';

const AddQuestion = () => {
  const [question, setQuestion] = useState('');
  const [answers, setAnswers] = useState(['', '', '', '']);
  const [correctAnswer, setCorrectAnswer] = useState('');
  const [category, setCategory] = useState('');
  const [difficulty, setDifficulty] = useState('');

  const handleAnswerChange = (index, value) => {
    const newAnswers = [...answers];
    newAnswers[index] = value;
    setAnswers(newAnswers);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newQuestion = {
      question,
      answers,
      correctAnswer,
      category,
      difficulty,
    };

    try {
      await axios.post('http://localhost:5000/api/quiz/add', newQuestion);
      alert('Question added successfully');
    } catch (error) {
      alert('Failed to add question');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Question</label>
        <input type="text" value={question} onChange={(e) => setQuestion(e.target.value)} required />
      </div>
      <div>
        <label>Answers</label>
        {answers.map((answer, index) => (
          <input
            key={index}
            type="text"
            value={answer}
            onChange={(e) => handleAnswerChange(index, e.target.value)}
            required
          />
        ))}
      </div>
      <div>
        <label>Correct Answer</label>
        <input type="text" value={correctAnswer} onChange={(e) => setCorrectAnswer(e.target.value)} required />
      </div>
      <div>
        <label>Category</label>
        <input type="text" value={category} onChange={(e) => setCategory(e.target.value)} required />
      </div>
      <div>
        <label>Difficulty</label>
        <select value={difficulty} onChange={(e) => setDifficulty(e.target.value)} required>
          <option value="">Select Difficulty</option>
          <option value="easy">Easy</option>
          <option value="medium">Medium</option>
          <option value="hard">Hard</option>
        </select>
      </div>
      <button type="submit">Add Question</button>
    </form>
  );
};

export default AddQuestion;
''',
                },
                'App.js': '''\
import React from 'react';
import AddQuestion from './components/AddQuestion';

function App() {
  return (
    <div>
      <h1>Quiz App</h1>
      <AddQuestion />
    </div>
  );
}

export default App;
'''
            },
            'package.json': '''\
{
  "name": "quiz-frontend",
  "version": "1.0.0",
  "scripts": {
    "start": "react-scripts start"
  },
  "dependencies": {
    "axios": "^0.21.1",
    "react": "^17.0.2",
    "react-dom": "^17.0.2",
    "react-scripts": "4.0.3"
  }
}
'''
        }
  }


def create_project_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_project_structure(path, content)
        else:
            with open(path, 'w') as f:
                f.write(content)

if __name__ == '__main__':
    base_path = os.getcwd()
    create_project_structure(base_path, folder_structure)
    print(f"Quiz app structure generated at {base_path}")
