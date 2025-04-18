import os
import sys
import chess
import chess.engine
import chess.pgn
import json

from datetime import datetime
from time import sleep
from pymongo import MongoClient

STOCKFISH_PATH = '../../Stockfish/src/stockfish'

NUM_THREADS = 16
TABLE_SIZE_IN_MB = 4096

SECONDS_PER_GAME_MOVE = 0.1
SECONDS_PER_CANDIDATE_MOVE = 5
NB_VARIATIONS = 3

ENGINE = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
ENGINE.configure({"Threads": NUM_THREADS})
ENGINE.configure({"Hash": TABLE_SIZE_IN_MB})

MAX_SCORE = 100_000

def best_moves_with_score(board, time_limit, nb_variations):
    global ENGINE

    output = []

    for line in ENGINE.analyse(board, time_limit, multipv = nb_variations):
        move = line['pv'][0]
        score = line['score'].relative.score(mate_score = MAX_SCORE)
        output.append({'move': move, 'score': score})

    return output

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

def analyze(game, depth, force):

    board = game.board()

    if board.is_game_over():
        return

    is_our_turn = (depth % 2 == 0)

    seconds_per_move = SECONDS_PER_CANDIDATE_MOVE / (1 if is_our_turn else 5)
    time_limit = chess.engine.Limit(time = seconds_per_move)
    nb_variations = 2 if is_our_turn else NB_VARIATIONS

    moves = best_moves_with_score(board, time_limit, nb_variations)

    diff = MAX_SCORE
    if len(moves) > 1:
        diff = moves[0]['score'] - moves[1]['score']

    print(" " * depth, moves[0]['move'], diff)

    # Continue the search if:
    #   - The 1st move is significantly better than the 2nd.
    #   - We are mating and only 1 move leads to the fastest mate.
    #   - Not our turn and the sequence is still short.
    #   - Not our turn and we are mating in 4 moves or less.
    if diff > 40 or force \
      or (is_our_turn and moves[0]['score'] > MAX_SCORE - 1000 and diff > 0) \
      or (not is_our_turn and depth <= 3) \
      or (not is_our_turn and moves[0]['score'] <= -MAX_SCORE + 4):

        if is_our_turn:
            node = game.add_variation(moves[0]['move'])
            analyze(node, depth + 1, False)

        else:
            for i in range(len(moves)):
                diff = moves[0]['score'] - moves[i]['score']
                if diff == 0 or (moves[0]['score'] > -MAX_SCORE + 1000 and diff < 20):
                    node = game.add_variation(moves[i]['move'])
                    analyze(node, depth + 1, False)

                    if len(node.variations) == 0:
                        game.remove_variation(moves[i]['move'])


def analyze_game(db_collection, f, game, lichess_username, analyzed_fens, userID):
    we_are_white = game.headers['White'] == lichess_username

    board = game.board()
    for move in game.mainline_moves():
        if we_are_white != board.turn:
            board.push(move)
            continue

        if board.fen() in analyzed_fens:
            continue

        time_limit = chess.engine.Limit(time = SECONDS_PER_GAME_MOVE)
        moves = best_moves_with_score(board, time_limit, 2)

        diff = MAX_SCORE
        if len(moves) > 1:
            diff = moves[0]['score'] - moves[1]['score']

        both_are_very_winning = len(moves) > 1 and moves[1]['score'] > 500 and diff < 200

        if diff > 40 and move != moves[0]['move'] and not both_are_very_winning:
            fen = board.fen()
            print("Analyzing %s from %s" % (fen, lichess_username))
            b = chess.Board(fen)
            g = chess.pgn.Game().from_board(b)
            analyze(g, 0, False)
            line = str(g).split("\n")[-1]
            print(line)

            if line != "*":
                line = line.replace(" )", ")").replace("( ", "(").replace(" *", "")
                f.write("%s: %s\n" % (fen, line))

                with open('/tmp/foo.pgn', 'w') as pgn:
                    pgn.write('[FEN "' + fen + '"]\n\n' + line)
                pgn = open('/tmp/foo.pgn')
                game = chess.pgn.read_game(pgn)
                variations = parse_variation(game, 0)[0]

                puzzle = {
                    "fen" : fen,
                    "solution" : variations, 
                    "attempts": 0,
                    "successes": 0, 
                    "streak": 0,
                    "lastSeen": None,
                    "userId": userID
                }
                result = db_collection.insert_one(puzzle)
                print(f"✅ Inserted a puzzle", result)
    
        board.push(move)

if __name__ == '__main__':

    # Connect to local MongoDB
    client = MongoClient("mongodb://chasolver.org:27017")
    db = client["chess"]
    db_collection = db["puzzles"]

    USERS = {
        # Local usernames
        # ("ambrona", "ambrona", "67fff5a84cf364b0d865a0ed"),
        # ("shosei-jutsu", "ambrona", "67fff5a84cf364b0d865a0ed")
        ("ambrona", "ambrona", "6802783ee5cbab90672646cb"),
        ("shosei-jutsu", "ambrona", "6802783ee5cbab90672646cb"),
        ("pierre_nodoyuna", "iquerejeta", "680278799e625bcc5fbf48aa"),
        ("HardradaII", "nevado", "680278ad183bfeac9bb875fb"),
        ("vonaka", "vonaka", "680279e12c6df85939bd7217"),
        ("elenagutiv", "elenagutiv", "68028e5298d3f076a5afdffe"),
        ("golvi", "golvi", "6802909898d3f076a5afdfff"),
        ("palladio777", "nappa", "6802964398d3f076a5afe000")
    }    

    USER_PUZZLES = {}
    for (lichess_username, db_username, userID) in USERS:
        user_fens = set()
        with open(db_username + '.txt', 'r') as f:
            for line in f.readlines():
                fen = line.strip().split(":")[0]
                user_fens.add(fen)
        USER_PUZZLES[db_username] = user_fens

    ANALYZED_GAMES = set()

    while True:
        for (lichess_username, db_username, userID) in USERS:

            if db_username == "nevado" or db_username == "nappa":
                month = datetime.now().strftime("%Y/%m")
                os.system('curl https://api.chess.com/pub/player/%s/games/%s > /tmp/games.pgn' % (lichess_username.lower(), month))
                with open('/tmp/games.pgn', 'r') as file:
                    data = json.load(file)

                with open('/tmp/games.pgn', 'w') as file:
                    for game in data["games"][-10:]:
                        file.write(game["pgn"])

            else:
                os.system('curl "https://lichess.org/api/games/user/%s?max=10&perfType=bullet,blitz,rapid,classical" > /tmp/games.pgn' % lichess_username)

            pgn = open("/tmp/games.pgn")

            with open(db_username + '.txt', 'a') as f:

                game = chess.pgn.read_game(pgn) 
                while game:
                    game_id = game.headers['Site']
                    if game_id not in ANALYZED_GAMES:
                        analyze_game(db_collection, f, game, lichess_username, USER_PUZZLES[db_username], userID)
                    
                    ANALYZED_GAMES.add(game_id)
                    game = chess.pgn.read_game(pgn)

            print("Analyzed all games of %s" % lichess_username)
        sleep(60)
