const express = require('express');
const path = require('path');
const { MongoClient } = require('mongodb');
const { ObjectId } = require('mongodb');

const app = express();
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

// MongoDB URI (you can use .env for this)
const uri = 'mongodb://localhost:27017';
const client = new MongoClient(uri);
const dbName = 'chessdb'; // your database name
const collectionName = 'puzzles'; // your collection name


// Connect and define the API
async function startServer() {
    try {
        await client.connect();
        console.log('✅ Connected to MongoDB');

        const db = client.db(dbName);
        const puzzles = db.collection(collectionName);

        // GET /api/puzzle — return a random puzzle
        app.get('/api/puzzle', async (req, res) => {
            try {
                const puzzlesArray = await puzzles.find().toArray();
                const now = Date.now();

                const weighted = puzzlesArray.map(p => {
                    const attempts = p.attempts || 0;
                    const successes = p.successes || 0;
                    const lastSeen = new Date(p.lastSeen || 0).getTime();

                    const failureRate = (attempts - successes) / (attempts || 1);
                    const rarityBoost = 1 / (1 + attempts);
                    const daysSinceSeen = (now - lastSeen) / (1000 * 60 * 60 * 24); // days
                    const recencyBoost = daysSinceSeen / 30; // Normalize (e.g. max boost after 30 days)

                    const weight = 5 * failureRate + rarityBoost + recencyBoost;

                    return { puzzle: p, weight };
                });

                // Normalize and pick one randomly
                const totalWeight = weighted.reduce((sum, p) => sum + p.weight, 0);
                let r = Math.random() * totalWeight;

                let puzzle = weighted[0].puzzle;

                for (let i = 0; i < weighted.length; i++) {
                    r -= weighted[i].weight;
                    if (r <= 0) {
                        puzzle = weighted[i].puzzle;
                        break;
                    }
                }

                console.log(puzzle);

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
            } catch (err) {
                console.error(err);
                res.status(500).json({ error: 'Failed to fetch puzzle' });
            }
        });

        // POST - update puzzle stats
        app.post('/api/puzzle/:id/result', express.json(), async (req, res) => {
            const { id } = req.params;
            const { correct } = req.body;

            if (typeof correct !== 'boolean') {
                return res.status(400).json({ error: "'correct' must be a boolean" });
            }

            let objectId;
            try {
                console.log(id);
                objectId = new ObjectId(id);
            } catch (e) {
                return res.status(400).json({ error: 'Invalid puzzle ID' });
            }

            try {
                const update = {
                    $inc: {
                        attempts: 1,
                        ...(correct ? { successes: 1 } : {})
                    },
                    $set: {
                        lastSeen: new Date()
                    }
                };

                console.log("🔍 Updating puzzle:", objectId.toHexString(), update);

                const result = await puzzles.updateOne({ _id: objectId }, update);
                console.log("🔁 Update result:", result);

                if (result.matchedCount === 0) {
                    return res.status(404).json({ error: 'Puzzle not found' });
                }

                res.json({ success: true, updated: result.modifiedCount });
            } catch (err) {
                console.error('❌ Update error:', err);
                res.status(500).json({ error: 'Failed to update puzzle result' });
            }
        });


        app.listen(port, () => {
            console.log(`🚀 API listening at http://localhost:${port}`);
        });

    } catch (err) {
        console.error('❌ MongoDB connection error:', err);
    }
}

startServer();