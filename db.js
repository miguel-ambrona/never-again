const { MongoClient } = require('mongodb');

const uri = 'mongodb://localhost:27017';
const client = new MongoClient(uri);

let db;

async function connectToDb() {
    await client.connect();
    db = client.db('chess');

    const users = await db.collection('users').find().toArray(); // Find all users
    console.log(users);  // List all users with their userIds
}

function getDb() {
    return db;
}

function getCollection(name) {
    return db.collection(name);
}

module.exports = { connectToDb, getDb, getCollection };