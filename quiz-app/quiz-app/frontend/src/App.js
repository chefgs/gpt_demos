import React from 'react';
import AddQuestion from './components/AddQuestion';
import QuizView from './components/QuizView';

function App() {
  return (
    <div>
      <h1>Quiz App</h1>
      <AddQuestion />
      <QuizView />
    </div>
  );
}

export default App;
