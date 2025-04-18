## Install Prerequisites

Get the 'board' repository, clone it at your preferred location 
(for example at the same level where you cloned this repository).
`git clone git@github.com:miguel-ambrona/board.git`.

Configure it following the instructions in its README.md.

## Install the Node js dependencies

Run:
```
npm install express
npm install mongodb
npm install bcrypt
npm install jsonwebtoken
npm install ../board  # Adjust path based on where you cloned `board`
```

## Run and Test

Start the development server with `node server.js`.
Then, open the browser at the displayed URL.