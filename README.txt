# 🎮 Tic Tac Toe — Python GUI Game

Fully functional Tic Tac Toe with a stylish dark-theme GUI built using Python's built-in `tkinter` library.

---

## ✅ Features

| Feature | Detail |
|---|---|
| 👤 Human vs Human | Two players take turns on the same PC |
| 🤖 Human vs Bot | Play against an AI with 3 difficulty levels |
| 🧠 Bot Difficulty | Easy / Medium / Hard (Minimax AI) |
| 🏆 Score Tracking | Scores for X, O, and Draws |
| ✨ Win Highlight | Winning line highlighted in gold |
| ↺ New Game | Reset board without losing scores |
| ← Menu | Go back to main menu anytime |

---

## ▶️ HOW TO RUN

### Requirements
- **Python 3.x** (tkinter is included by default)
- No extra libraries needed!

### Step 1 — Check Python is installed
Open Terminal / Command Prompt and type:
```
python --version
```
or
```
python3 --version
```
You should see something like `Python 3.11.x`

### Step 2 — Run the game

**Windows:**
```
python tictactoe.py
```

**Mac / Linux:**
```
python3 tictactoe.py
```

Or just **double-click** `tictactoe.py` if Python is associated with .py files.

---

## 🎮 How to Play

1. Main Menu opens — choose your mode:
   - **Human vs Human** → two players take turns clicking
   - **Human vs Bot** → pick Easy / Medium / Hard, then play as X
2. Click any cell to place your mark
3. First to get 3 in a row (horizontal, vertical, diagonal) wins!
4. Click **↺ New Game** to replay (scores are kept)
5. Click **← Menu** to go back to the main menu

---

## 🤖 Bot Difficulty

| Level | Behavior |
|---|---|
| Easy | Plays randomly |
| Medium | 60% smart, 40% random |
| Hard | Unbeatable — uses Minimax with Alpha-Beta pruning |

---

## 📁 File Structure

```
tictactoe/
│
└── tictactoe.py     ← single file, run this!
└── README.txt       ← this file
```

---

Made with ❤️ using Python + tkinter
