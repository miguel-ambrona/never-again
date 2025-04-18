const fs = require('fs');
const https = require('https');
const express = require('express');
const path = require('path');
const { connectToDb } = require('./db');
const authRoutes = require('./routes/auth');
const puzzleRoutes = require('./routes/puzzles');

const app = express();
app.use(express.json());

const port = 3141;

// const credentials = {
// key: fs.readFileSync('/etc/letsencrypt/live/chasolver.org/privkey.pem', 'utf8'),
// cert: fs.readFileSync('/etc/letsencrypt/live/chasolver.org/fullchain.pem', 'utf8')
// }

// Serve static files (like HTML, CSS, JS) from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// Serve static files from the 'board'
app.use('/board', express.static(path.join(__dirname, '../board/public')));
app.use('/board/node_modules', express.static(path.join(__dirname, '../board/node_modules')));
app.use('/img', express.static(path.join(__dirname, '../board/public/img')));
app.use('/audio', express.static(path.join(__dirname, '../board/public/audio')));

app.get('/', function (req, res) {
    res.sendfile('./public/index.html');
});

app.use('/api', authRoutes);
app.use('/api', puzzleRoutes);

connectToDb().then(() => {
    // https.createServer(credentials, app).listen(port, () => {
    app.listen(port, () => {
        console.log(`✅ Server running on http://localhost:${port}`);
    });
});
