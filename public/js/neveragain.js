import { ChessBoard } from "../board/index.js";

let puzzle = null;
let correct = true;
let nb_failures = 0;

let board = ChessBoard('board',
    {
        fen: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -',
        gain_backwards_castling: false,
        retracting: false,
        afterMove: function () { setTimeout(validate, 50); },
    });

window.addEventListener('keydown', keyPress, false);

function keyPress(event) {
    // Left
    if (event.keyCode === 37) {
        board.undo();
    }

    // Right
    else if (event.keyCode === 39) {
        board.redo();
    }
};

function validate() {
    let move = board.last_move();
    let expected = puzzle.solution[0];

    if (move != expected) {
        correct = false;
        nb_failures += 1;
        board.highlight_squares([move.substring(2, 4)], 'red', 300);
        setTimeout(function () { board.pop() }, 300);

        if (nb_failures >= 3) {
            board.highlight_squares([expected.substring(0, 2)], 'green', 300);
        }

        return;
    }

    nb_failures = 0;
    board.highlight_squares([expected.substring(0, 2), expected.substring(2, 4)], 'green', 300);

    puzzle.solution.shift();
    let answer = puzzle.solution.shift();

    if (!answer) {
        sendResult(puzzle._id, correct);
        setTimeout(getPuzzle, 300);
        return;
    }

    setTimeout(function () { board.move(answer) }, 300);
};

function loadPuzzle() {
    board.orientation(puzzle.fen.includes(" w ") ? "white" : "black");
    board.set_fen(puzzle.fen);
    correct = true;
}

async function sendResult(puzzleId, wasCorrect) {
    const token = localStorage.getItem('token');
    const response = await fetch(`/api/puzzle/${puzzleId}/result`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ correct: wasCorrect, localDate: Date() })
    });
    await response.json();
}

async function getPuzzle() {
    const token = localStorage.getItem('token');
    const res = await fetch('/api/puzzle', {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
    puzzle = await res.json();
    loadPuzzle();
    getStreak();
}

async function getStreak() {
    const token = localStorage.getItem('token');
    const res = await fetch('/api/streak', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ localDate: Date() })
    });
    const data = await res.json();
    document.querySelector('#streak-counter').innerText = `🔥 ${data.streak}`;
    document.querySelector('#username').innerText = `${data.username}`;
}

const checkBoardLoaded = setInterval(() => {
    if (board) {
        clearInterval(checkBoardLoaded); // Stop checking
        getPuzzle();
    }
}, 500);
