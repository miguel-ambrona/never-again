const express = require('express');
const path = require('path');
const { connectToDb } = require('./db');
const authRoutes = require('./routes/auth');
const puzzleRoutes = require('./routes/puzzles');

const app = express();
app.use(express.json());

const port = 3141;

// Serve static files (like HTML, CSS, JS) from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// Serve static files from the 'board'
app.use('/board', express.static(path.join(__dirname, '../board/public')));
app.use('/board/node_modules', express.static(path.join(__dirname, '../board/node_modules')));
app.use('/img', express.static(path.join(__dirname, '../board/public/img')));

app.get('/', function (req, res) {
    res.sendfile('./public/index.html');
});

app.use('/api', authRoutes);
app.use('/api', puzzleRoutes);

connectToDb().then(() => {
    app.listen(port, () => console.log(`✅ Server running on http://localhost:${port}`));
});