const express = require('express');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const { JWT_SECRET, JWT_EXPIRES_IN } = require('../config');
const { getCollection } = require('../db');

const router = express.Router();
const users = () => getCollection('users');

router.post('/signup', async (req, res) => {
    const { username, password } = req.body;
    const existing = await users().findOne({ username });
    if (existing) return res.status(400).json({ error: 'Username taken' });

    const passwordHash = await bcrypt.hash(password, 10);
    const result = await users().insertOne({ username, passwordHash });
    const userId = result.insertedId.toHexString();
    const token = jwt.sign({ userId, username }, JWT_SECRET, { expiresIn: JWT_EXPIRES_IN });
    res.json({ token });
});

router.post('/login', async (req, res) => {
    const { username, password } = req.body;
    const user = await users().findOne({ username });
    if (!user || !(await bcrypt.compare(password, user.passwordHash))) {
        return res.status(400).json({ error: 'Invalid credentials' });
    }
    const token = jwt.sign({ userId: user._id.toHexString(), username }, JWT_SECRET, { expiresIn: JWT_EXPIRES_IN });
    res.json({ token });
});

module.exports = router;