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