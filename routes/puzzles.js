const express = require('express');
const { ObjectId } = require('mongodb');
const requireAuth = require('../middleware/requireAuth');
const { getCollection } = require('../db');

const router = express.Router();
const puzzles = () => getCollection('puzzles');
const users = () => getCollection('users');

router.post('/streak', requireAuth, async (req, res) => {
    const user = await users().findOne({ _id: new ObjectId(req.userId) });
    let streak = user.streak || 0;

    const userToday = new Date(req.body.localDate);
    const userYesterday = yesterday_if_valid(userToday);

    if (!userYesterday) {
        return res.status(404).json({ error: 'Do not try to trick me, that cannot be your local date' });
    }

    if (user.lastActiveDate !== userToday.toDateString() && user.lastActiveDate !== userYesterday.toDateString()) {
        streak = 0;
    }

    res.json({ username: user.username, streak });
});

router.get('/puzzle', requireAuth, async (req, res) => {
    const userId = req.userId;
    const now = Date.now();
    const puzzleList = await puzzles().find({ userId }).toArray();

    const weighted = puzzleList.map(p => {
        const attempts = p.attempts || 0;
        const successes = p.successes || 0;
        const streak = p.streak || 0;
        const hoursSinceSeen = (now - new Date(p.lastSeen || 0)) / (1000 * 3600);

        const successRate = attempts > 0 ? successes / attempts : 0;
        const rarityBoost = 1 / (1 + attempts);

        let weight = (1 - successRate) + 3 * rarityBoost;

        if (hoursSinceSeen < fib(streak)) {
            weight *= 0.000001;
        }

        return { puzzle: p, weight };
    });

    let puzzle = weighted[0].puzzle;

    const totalWeight = weighted.reduce((sum, p) => sum + p.weight, 0);
    let r = Math.random() * totalWeight;
    for (let i = 0; i < weighted.length; i++) {
        r -= weighted[i].weight;
        if (r <= 0) {
            puzzle = weighted[i].puzzle;
            break;
        }
    }

    // Choose a random variation for the selected puzzle
    let moves = puzzle.solution;
    let solution = [];
    while (moves.length > 1) {
        solution.push(moves[0]);
        moves = moves[1];
        let i = Math.floor(Math.random() * moves.length);
        moves = moves[i];
    }
    solution.push(moves[0]);
    puzzle.solution = solution;

    res.json(puzzle);
});

router.post('/puzzle/:id/result', requireAuth, async (req, res) => {
    const puzzleId = req.params.id;
    const { correct } = req.body;
    const userId = req.userId;

    const puzzle = await puzzles().findOne({ _id: new ObjectId(puzzleId), userId });

    if (!puzzle) {
        return res.status(404).json({ error: 'Puzzle not found for this user' });
    }

    const newPuzzleStreak = correct ? (puzzle.streak || 0) + 1 : 0;

    // Update the puzzle
    const update = {
        $inc: {
            attempts: 1,
            successes: correct ? 1 : 0
        },
        $set: { lastSeen: new Date(), streak: newPuzzleStreak }
    };

    await puzzles().updateOne({ _id: new ObjectId(puzzleId), userId }, update);

    // Update the user streak
    const userToday = new Date(req.body.localDate);
    const userYesterday = yesterday_if_valid(userToday);

    if (!userYesterday) {
        return res.status(404).json({ error: 'Do not try to trick me, that cannot be your local date' });
    }

    const user = await users().findOne({ _id: new ObjectId(userId) });
    const lastActive = user.lastActiveDate || userYesterday.toDateString();

    let newStreak = user.streak || 0;

    if (lastActive !== userToday.toDateString() && correct) {
        newStreak += 1;
        if (lastActive !== userToday.toDateString()) {
            newStreak = 1;
        }

        await users().updateOne(
            { _id: new ObjectId(userId) },
            { $set: { lastActiveDate: userToday.toDateString(), streak: newStreak } }
        );

    }

    res.json({ success: true });


});

function yesterday_if_valid(localDate) {
    const today = new Date(localDate);
    const yesterday = new Date(today - 24 * 3600 * 1000);

    const nowUTC = new Date();
    const lower_bound = new Date(nowUTC.getTime() - 12 * 3600 * 1000);
    const upper_bound = new Date(nowUTC.getTime() + 14 * 3600 * 1000);

    if (lower_bound <= today && today <= upper_bound) {
        return yesterday;
    }
}

function fib(n) {
    const sqrt5 = Math.sqrt(5);
    const phi = (1 + sqrt5) / 2;
    return Math.round((Math.pow(phi, n)) / sqrt5);
}

module.exports = router;
