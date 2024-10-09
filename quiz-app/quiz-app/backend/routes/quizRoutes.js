const express = require('express');
const Quiz = require('../models/quizModel');
const router = express.Router();

router.post('/add', async (req, res) => {
  try {
    const { question, answers, correctAnswer, category, difficulty } = req.body;

    if (!question || !answers || !correctAnswer || !category || !difficulty) {
      return res.status(400).json({ message: 'All fields are required' });
    }
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

// Route to get all quiz questions
router.get('/questions', async (req, res) => {
  try {
    const questions = await Quiz.find();
    res.json(questions);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Server error' });
  }
});

// Route to submit an answer
router.post('/answer', async (req, res) => {
  try {
    const { questionId, selectedAnswer } = req.body;
    const question = await Quiz.findById(questionId);

    if (!question) {
      return res.status(404).json({ message: 'Question not found' });
    }

    const isCorrect = question.correctAnswer === selectedAnswer;
    res.json({ isCorrect });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Server error' });
  }
});

module.exports = router;
