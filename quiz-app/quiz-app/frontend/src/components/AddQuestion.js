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
      await axios.post('http://localhost:6000/api/quiz/add', newQuestion);
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
