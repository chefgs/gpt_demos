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