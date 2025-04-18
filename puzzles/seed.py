import sys
import chess.pgn

from pymongo import MongoClient

# Connect to local MongoDB
client = MongoClient("mongodb://chasolver.org:35114")
db = client["chess"]
collection = db["puzzles"]

# Optional: clear old data
# collection.delete_many({})
# result = collection.delete_many({"userId": "680279e12c6df85939bd7217"})
# print(result)

documents = db["users"].find()

# Print each document
for doc in documents:
    print(doc)

def parse_variation(game, depth):
    res = []
    for v in game.variations:
        next_var = parse_variation(v, depth + 1)
        if next_var == []:
            if depth % 2 == 0:
                res.append([str(v.move)])
        else:
            res.append([str(v.move), next_var])
    return res

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 %s USERNAME" % sys.argv[0])
        exit(0)

    username = sys.argv[1]

    puzzles = []
    cnt = 0
    with open(username + '.txt', 'r') as f:
        for line in f.readlines():
            cnt += 1
            if cnt > 100:
                continue
            (fen, line) = line.strip().split(": ")
            if len(line) < 3:
                continue

            with open('/tmp/foo.pgn', 'w') as pgn:
                pgn.write('[FEN "' + fen + '"]\n\n' + line)
            pgn = open('/tmp/foo.pgn')
            game = chess.pgn.read_game(pgn)
            variations = parse_variation(game, 0)[0]

            puzzles.append({
                "fen" : fen,
                "solution" : variations, 
                "attempts": 0,
                "successes": 0, 
                "streak": 0,
                "lastSeen": None,
                "userId": "6802783ee5cbab90672646cb"
            })

    # Insert into MongoDB
    result = collection.insert_many(puzzles)
    print(f"✅ Inserted {len(result.inserted_ids)} puzzles")
