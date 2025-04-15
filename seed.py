from pymongo import MongoClient

# Connect to local MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["chessdb"]
collection = db["puzzles"]

# Optional: clear old data
collection.delete_many({})

# Your puzzle data
puzzles = [
# { "fen" : 'rnb2rk1/1p3pp1/pq1ppb1p/8/4PP2/2N2Q2/PPP1N1PP/2KR1B1R w - - 4 12', "solution" : ['h2h4', [['b8c6', [['g2g4', [['f6c3', [['e2c3']]]]]]]]], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : '2r2rk1/4bppp/p2P4/3R2PQ/1p2P3/4B3/qPP3RP/2K5 b - - 0 22', "solution" : ['e7d6', [['d5d6', [['b4b3', [['h5d1', [['a2a1', [['c1d2', [['c8c2', [['d2e1', [['a1d1']]]]]]]]]]], ['h5f3', [['a2a1']]]]]]]]], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : '2r2rk1/4Pppp/p7/3R2PQ/4P3/1p2B3/qPP3RP/2K5 b - - 0 23', "solution" : ['f8e8', [['e3c5', [['a2a1', [['c1d2', [['a1b2', [['d2d3', [['e8e7']]]]]]]]]]]]], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : 'r4rk1/ppp2pb1/2np1q1p/4pPp1/P4n2/3P1N1P/BPP2PP1/R1BQ1RK1 w - - 1 14', "solution" : ['g2g3', [['f4h3', [['g1g2', [['f6f5', [['f3h2']]]]]]]]], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : 'r4rk1/ppp2p2/3p3p/5Pp1/P4pP1/3Q3P/B1P2P2/b5K1 w - - 0 20', "solution" : ['c2c3'], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : 'r1bqk1nr/pp1pppbp/6p1/1NpP4/4P3/5N2/PPP2PPP/R1BQK2R b KQkq - 0 7', "solution" : ['d8a5', [['b5c3', [['g7c3', [['b2c3', [['a5c3', [['c1d2', [['c3c4', [['d1e2', [['c4e2']]]]]]]]]]]]]]]]], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : '6k1/pp1b1rbp/1q2r1p1/2pN1p2/2P2B2/1P3Q1P/P4PP1/R3R1K1 b - - 1 20', "solution" : ['g7a1'], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : '4r2k/pp1b2bp/2q1r1p1/2pN1p2/2P2B2/1P1Q3P/P3RPP1/4R1K1 b - - 9 24', "solution" : ['e6e2', [['e1e2', [['e8e2', [['d3e2', [['c6e6']]]]]]]]], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : '8/7p/p5p1/2B1kp2/2b5/1N3P1P/Pb3KP1/8 b - - 2 41', "solution" : ['c4b3'], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : '8/7p/pb1B2p1/1k3p2/2b5/1N3P1P/P5P1/4K3 b - - 12 46', "solution" : ['c4b3', [['a2b3', [['b6c5', [['d6c5', [['b5c5']]]]]]]]], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : '8/7p/pb1B2p1/2N2p2/k1b5/5P1P/P5P1/4K3 b - - 14 47', "solution" : ['a4b5', [['c5d7', [['b6a5', [['e1d1', [['c4a2']]]]]]]]], "attempts": 0, "successes": 0, "lastSeen": None},
{ "fen" : '8/8/5Bpp/3b1p1k/5P1P/8/p7/K7 b - - 1 70', "solution" : ['h5g4', [['a1b2', [['g4f4', [['f6c3', [['f4e4']]], ['f6g7', [['f4e4']]]]]]], ['h4h5', [['g6h5', [['a1b2', [['h5h4']]], ['f6e5', [['h5h4']]]]]]]]], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : '8/8/5B1p/3b1pPk/5P2/8/p7/K7 b - - 0 71', "solution" : ['h5g6', [['f6d4', [['h6h5', [['d4f2', [['d5c4']]]]]]], ['f6c3', [['h6h5', [['c3d2', [['h5h4']]]]]]]]], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : 'r1bq1rk1/pp2ppbp/5np1/2p5/2P5/2N3P1/PPP2PBP/R1BQ1RK1 b - - 0 11', "solution" : ['c8e6'], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : '4r1k1/p2R1pbp/1p4p1/2p5/5B2/2P2BP1/bP3P1P/6K1 b - - 3 22', "solution" : ['e8e1', [['g1g2', [['h7h5', [['d7a7', [['a2c4']]]]]]]]], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : '4B3/7p/1p3p2/2p1k1pP/6P1/2P1PK2/1P6/5b2 b - - 0 34', "solution" : ['f1d3', [['e8c6', [['f6f5', [['g4f5', [['e5f5']]]]]]]]], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : 'r1b1k2r/1pqnbpp1/2n1p2p/p2pP3/8/1NPBBN2/PP2RPPP/R2Q2K1 w kq - 4 14', "solution" : ['e3f4', [['g7g5', [['f4g3']]]]], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : 'rqb2rk1/1p4p1/2nbpn1p/3p4/p2B4/2PB1NN1/PP2RPPP/2RQ2K1 w - - 4 20', "solution" : ['d4f6'], "attempts": 0, "successes": 0, "lastSeen": None},
{ "fen" : 'rqb2rk1/1p4p1/2nb3p/3p4/p2Np1n1/2P1B1N1/PP2RPPP/1BRQ2K1 w - - 2 23', "solution" : ['d4b5', [['c8e6', [['b5d6', [['b8d6', [['b1e4']]]]]]]]], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : 'rqb2rk1/6p1/2pb3p/3p4/p3p1n1/2P1B1N1/PP2RPPP/1BRQ2K1 w - - 0 24', "solution" : ['e3d4', [['c8e6', [['c3c4', [['c6c5', [['c4d5', [['c5d4', [['d5e6', [['d4d3', [['b1d3']]]]]]]]]]]]]]]]], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : 'r6k/6p1/5r1p/5N2/p3Q3/4P3/Pq4PP/1B3RK1 w - - 2 32', "solution" : ['e4a8', [['f6f8', [['a8f8', [['h8h7', [['f5e7', [['b2b1', [['f8g8']]], ['b2c2', [['f8g8']]]]]]]]]]], ['b2b8', [['a8b8', [['f6f8', [['b8f8']]], ['h8h7', [['f5e7', [['g7g6', [['b8g8']]], ['f6f5', [['b8g8']]]]]]]]]]]]], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : '4kb1r/p1qn1p1p/1p2p1p1/3pP3/3P1P2/2r5/PP1Q2PP/RB3NK1 w k - 0 19', "solution" : ['b2c3'], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : '7r/p2nkp1p/1p2p1p1/1B1pP3/3P1P2/2b5/P5PP/3R1NK1 w - - 2 24', "solution" : ['f1g3', [['a7a6', [['b5a6', [['h8a8', [['a6b5', [['a8a2', [['g3e2']]]]]]]]]]]]], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : '8/4kp2/4p1p1/3pP2p/1b1P1PP1/pB1K4/7P/8 w - - 0 41', "solution" : ['g4h5'], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : '2rq1r2/3bppkp/3p2p1/p2n3P/1p2P3/1B3P2/PPPQ2P1/2KR3R w - - 0 17', "solution" : ['h5g6'], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : 'rnb2rk1/p1q1npbp/1pp1p1p1/3p4/P1BPPP2/2N1BN2/1PP1Q1PP/R4RK1 w - - 0 11', "solution" : ['c4d3', [['d5e4', [['c3e4']]]]], "attempts": 0, "successes": 0, "lastSeen": None},
{ "fen" : 'rnb2rk1/p4pbp/1pp1p1p1/8/P2PNq2/5N2/BPP1Q1PP/4RRK1 w - - 0 15', "solution" : ['f3g5', [['g7d4', [['g1h1']]]]], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : 'rnb2r1k/p4pbp/1pp1pNpq/8/P2PN3/6P1/BPP1Q2P/4RRK1 w - - 1 19', "solution" : ['e4d6', [['c8a6', [['c2c4']]]]], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : '1rb2r1k/p2n1pbp/1pp1p1p1/7q/P2PN1N1/2P2QP1/BP5P/4RRK1 w - - 3 22', "solution" : ['e4d6', [['f7f5', [['a2e6', [['h5g4', [['f3g4']]], ['d7f6', [['g4f6', [['h5f3', [['f1f3', [['c8e6', [['f3e3']]]]]]]]]]]]]]]]], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : '1r3r1k/pb3pbp/1p6/3PpQ2/P4p2/2P3P1/BP5P/4R1K1 w - - 2 30', "solution" : ['a2b1'], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : 'r1bq1r1k/5ppp/p2pPb2/1p1Nn2Q/3NP3/7B/PPP4P/1K1R1R2 b - - 8 19', "solution" : ['g7g6'], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : 'r1bq1r1k/6pp/p2pBb2/1p1Nn2Q/3NP3/8/PPP4P/1K1R1R2 b - - 0 20', "solution" : ['g7g6', [['h5e2', [['f6g7', [['e6c8', [['f8f1', [['d1f1', [['a8c8']]]]]]]]]]], ['h5h3', [['f6g7', [['f1f8', [['g7f8']]]]]]]]], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : 'r2qkb1r/p2n1ppp/bpn1p3/2ppP3/3P4/2P5/PPBNNPPP/R1BQK2R w KQkq - 2 9', "solution" : ['d2f3'], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : 'rnbqkbnr/1p3ppp/p2p4/4p3/2PNP3/8/PP3PPP/RNBQKB1R w KQkq - 0 6', "solution" : ['d4c2'], "attempts": 0, "successes": 0, "lastSeen": None},
{ "fen" : '2Rr4/1p1P1pk1/p4bpp/4p3/8/1P3B2/P5PP/7K w - - 2 30', "solution" : ['c8c7'], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : '8/3P4/1b6/7p/1P1kppp1/7P/B3K1P1/8 w - - 0 45', "solution" : ['h3g4'], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : '8/3P1B2/1b6/8/1P1kp2p/5p1P/8/5K2 w - - 0 48', "solution" : ['f1e1', [['e4e3', [['f7b3']]], ['d4e3', [['f7c4', [['e3f4', [['c4f1']]]]]]]]], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : '8/3P4/1b6/7B/1P2pk1p/5p1P/8/4K3 w - - 4 50', "solution" : ['h5g6'], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : '1r1r2k1/4q1bp/N3ppp1/1p1pn3/4P3/1P2B2P/P2Q1PP1/2RR2K1 b - - 0 25', "solution" : ['d5e4', [['a6b8', [['d8d2', [['d1d2', [['h7h5']]]]]]]]], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : 'r2r2k1/2N1q1bp/4ppp1/1p1pn3/4P3/1P2B2P/P2Q1PP1/2RR2K1 b - - 2 26', "solution" : ['a8c8'], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : 'r5k1/2N1q1bp/4ppp1/1p2n3/4p3/1P2B2P/P4PP1/2RQ2K1 b - - 0 28', "solution" : ['a8d8', [['d1e2', [['e5d3', [['c1c2', [['b5b4']]], ['c1c6', [['e7d7']]]]]]], ['d1f1', [['e5d3']]]]], "attempts": 0, "successes": 0, "lastSeen": None},
{ "fen" : 'q5k1/6bp/4ppp1/2n5/1P1Np3/7P/5PP1/3Q2K1 b - - 0 34', "solution" : ['c5d3', [['d4e6', [['a8a2', [['e6c5', [['a2f2']]]]]]]]], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : '6k1/2P4p/4p1p1/3q1p2/4p3/7P/5KP1/3Q4 b - - 0 38', "solution" : ['d5c5', [['f2f1', [['c5c7', [['f1g1', [['g8g7']]], ['d1d4', [['c7f4']]]]]]]]], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : '8/7Q/4pkp1/5p2/4p3/6KP/3q2P1/8 b - - 2 42', "solution" : ['d2d6', [['g3f2', [['f5f4', [['h7a7', [['d6d1']]], ['h7h4', [['f6g7', [['g2g4', [['f4g3', [['f2e2', [['d6d3', [['e2e1', [['d3e3']]]]]]]]]]]]]]], ['h7g8', [['e4e3']]]]]]]]], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : '8/7Q/4pkp1/5p2/4pq2/7P/6P1/6K1 b - - 6 44', "solution" : ['f4c1'], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : 'r1bq1rk1/pp2npbp/4p1p1/1B1p4/3pPP2/3P1N2/PPP1Q1PP/R1B1R1K1 b - - 1 11', "solution" : ['d8a5', [['a2a4', [['a7a6', [['c1d2', [['a5c7']]]]]]], ['c2c4', [['d4c3', [['d3d4', [['d5e4']]]]]]]]], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : '2r2r1k/1b4bp/p1q1B1p1/1p3pN1/3p1P2/P2PnQP1/1PPB3P/R3R1K1 b - - 2 23', "solution" : ['c6f3', [['g5f3', [['c8c2', [['d2e3', [['d4e3']]]]]]]]], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : 'r1r3k1/3bppbp/p2p1np1/qp2n3/3NP1PP/1BN1BP2/PPPQ4/1K1R3R w - - 1 15', "solution" : ['h4h5'], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : '2r3k1/4ppb1/3pb1p1/Np6/r3P1P1/5P2/PPPQ4/1K5R w - - 1 25', "solution" : ['a2a3', [['b5b4', [['a3b4']]]]], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : 'r5k1/4ppb1/3p2p1/1p6/4P1P1/1PP2P2/1PKQ4/7r w - - 0 29', "solution" : ['b3b4', [['a8a1', [['c2b3', [['g7e5', [['f3f4']]]]]]], ['h1f1', [['f3f4', [['a8a1', [['c2b3']]]]]]]]], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : 'rnb1kb1r/pp1ppp1p/1q3np1/4P3/8/8/RBPP1PPP/1N1QKBNR b Kkq - 2 7', "solution" : ['f6d5'], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : 'r1b1k2r/pp2ppbp/2n1P1p1/3Q1qN1/2P3n1/8/RB3PPP/1N2KB1R b Kkq - 0 14', "solution" : ['f5f2', [['e1d1', [['g4e3', [['d1c1', [['f2c2']]]]]]]]], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : 'r1b1k2r/pp2ppbp/2n1P1p1/6N1/2P3n1/8/RB3PPP/1q1QKB1R b Kkq - 1 15', "solution" : ['b1a2', [['e6f7', [['e8f8', [['b2g7', [['f8g7']]]]]]]]], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : 'r2qk1nr/pp2ppbp/2n3p1/2pp1b2/P7/2PP1NP1/1P1NPPBP/R1BQK2R b KQkq - 3 7', "solution" : ['g8f6'], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : 'r1q1k1nr/pp2ppbp/2n3p1/2pp1b2/P7/2PP1NPP/1P1NPPB1/R1BQK2R b KQkq - 0 8', "solution" : ['g8f6'], "attempts": 0, "successes": 0, "lastSeen": None},
# { "fen" : 'r1q1k1nr/pp1bppb1/2n3p1/2p3Np/P3P3/1QP3PP/1P1N1PB1/R1B1K2R b KQkq - 4 12', "solution" : ['g8h6', [['d2c4', [['f7f6']]]]], "attempts": 0, "successes": 0, "lastSeen": None},
]

# Insert into MongoDB
result = collection.insert_many(puzzles)
print(f"✅ Inserted {len(result.inserted_ids)} puzzles")