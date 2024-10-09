// src/components/QuizView.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const QuizView = () => {
  const [questions, setQuestions] = useState([]);
  const [selectedAnswer, setSelectedAnswer] = useState({});
  const [result, setResult] = useState(null);

  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        const response = await axios.get('/api/quiz/questions');
        setQuestions(response.data);
      } catch (error) {
        console.error('Error fetching questions:', error);
      }
    };

    fetchQuestions();
  }, []);

  const handleAnswerChange = (questionId, answer) => {
    setSelectedAnswer({ ...selectedAnswer, [questionId]: answer });
  };

  const handleSubmit = async (questionId) => {
    try {
      const response = await axios.post('/api/quiz/answer', {
        questionId,
        selectedAnswer: selectedAnswer[questionId],
      });
      setResult({ ...result, [questionId]: response.data.isCorrect });
    } catch (error) {
      console.error('Error submitting answer:', error);
    }
  };

  return (
    <div>
      <h1>Quiz Questions</h1>
      {questions.map((question) => (
        <div key={question._id}>
          <h2>{question.question}</h2>
          {question.answers.map((answer) => (
            <div key={answer}>
              <label>
                <input
                  type="radio"
                  name={question._id}
                  value={answer}
                  checked={selectedAnswer[question._id] === answer}
                  onChange={() => handleAnswerChange(question._id, answer)}
                />
                {answer}
              </label>
            </div>
          ))}
          <button onClick={() => handleSubmit(question._id)}>Submit Answer</button>
          {result && result[question._id] !== undefined && (
            <p>{result[question._id] ? 'Correct!' : 'Incorrect!'}</p>
          )}
        </div>
      ))}
    </div>
  );
};

export default QuizView;