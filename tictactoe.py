import tkinter as tk
from tkinter import messagebox, ttk
import random
import math

# ─────────────────────────────────────────────
#  COLORS & FONTS
# ─────────────────────────────────────────────
BG       = "#0d0d1a"
PANEL    = "#12122a"
ACCENT1  = "#00f5d4"   # X color (cyan-green)
ACCENT2  = "#f72585"   # O color (hot pink)
WHITE    = "#e8e8ff"
GRAY     = "#3a3a5c"
BTN_BG   = "#1a1a3e"
BTN_HOV  = "#252550"
WIN_LINE = "#ffd60a"

FONT_TITLE  = ("Courier New", 28, "bold")
FONT_CELL   = ("Courier New", 42, "bold")
FONT_STATUS = ("Courier New", 14, "bold")
FONT_BTN    = ("Courier New", 12, "bold")
FONT_SCORE  = ("Courier New", 11)
FONT_LABEL  = ("Courier New", 10)


# ─────────────────────────────────────────────
#  AI  (Minimax with alpha-beta pruning)
# ─────────────────────────────────────────────
class AI:
    def __init__(self, ai_mark, human_mark, difficulty="hard"):
        self.ai    = ai_mark
        self.human = human_mark
        self.diff  = difficulty          # easy | medium | hard

    def best_move(self, board):
        if self.diff == "easy":
            return self._random_move(board)
        if self.diff == "medium":
            # 60% chance smart, 40% random
            return self._minimax_move(board) if random.random() > 0.4 else self._random_move(board)
        return self._minimax_move(board)

    def _random_move(self, board):
        empty = [i for i, v in enumerate(board) if v == ""]
        return random.choice(empty) if empty else None

    def _minimax_move(self, board):
        best_val, best_idx = -math.inf, None
        for i in range(9):
            if board[i] == "":
                board[i] = self.ai
                val = self._minimax(board, 0, False, -math.inf, math.inf)
                board[i] = ""
                if val > best_val:
                    best_val, best_idx = val, i
        return best_idx

    def _minimax(self, board, depth, is_max, alpha, beta):
        winner = check_winner(board)
        if winner == self.ai:    return 10 - depth
        if winner == self.human: return depth - 10
        if all(v != "" for v in board): return 0

        if is_max:
            best = -math.inf
            for i in range(9):
                if board[i] == "":
                    board[i] = self.ai
                    best = max(best, self._minimax(board, depth+1, False, alpha, beta))
                    board[i] = ""
                    alpha = max(alpha, best)
                    if beta <= alpha: break
            return best
        else:
            best = math.inf
            for i in range(9):
                if board[i] == "":
                    board[i] = self.human
                    best = min(best, self._minimax(board, depth+1, True, alpha, beta))
                    board[i] = ""
                    beta = min(beta, best)
                    if beta <= alpha: break
            return best


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
WIN_COMBOS = [
    (0,1,2),(3,4,5),(6,7,8),   # rows
    (0,3,6),(1,4,7),(2,5,8),   # cols
    (0,4,8),(2,4,6)            # diags
]

def check_winner(board):
    for a,b,c in WIN_COMBOS:
        if board[a] != "" and board[a] == board[b] == board[c]:
            return board[a]
    return None

def winning_combo(board):
    for a,b,c in WIN_COMBOS:
        if board[a] != "" and board[a] == board[b] == board[c]:
            return (a,b,c)
    return None


# ─────────────────────────────────────────────
#  MAIN MENU
# ─────────────────────────────────────────────
class MainMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic Tac Toe")
        self.geometry("480x580")
        self.resizable(False, False)
        self.configure(bg=BG)
        self._build_ui()

    def _build_ui(self):
        # Title
        tk.Label(self, text="TIC TAC TOE", font=FONT_TITLE,
                 bg=BG, fg=ACCENT1).pack(pady=(40,4))
        tk.Label(self, text="— by Python —", font=FONT_LABEL,
                 bg=BG, fg=GRAY).pack()

        # Separator
        tk.Frame(self, height=2, bg=ACCENT1).pack(fill="x", padx=60, pady=20)

        # Mode selector
        tk.Label(self, text="SELECT MODE", font=FONT_STATUS,
                 bg=BG, fg=WHITE).pack(pady=(10,12))

        self._btn("👤  Human  vs  Human", self._start_hvh)
        self._btn("🤖  Human  vs  Bot",   self._show_diff_menu)

        # Separator
        tk.Frame(self, height=2, bg=GRAY).pack(fill="x", padx=60, pady=24)

        # Quit
        self._btn("❌  Quit", self.destroy, color=ACCENT2)

        # Footer
        tk.Label(self, text="X goes first   |   Bot uses Minimax AI",
                 font=FONT_LABEL, bg=BG, fg=GRAY).pack(side="bottom", pady=14)

    def _btn(self, text, cmd, color=ACCENT1):
        f = tk.Frame(self, bg=BTN_BG, bd=0, highlightthickness=1,
                     highlightbackground=color)
        f.pack(padx=60, pady=6, fill="x")
        b = tk.Label(f, text=text, font=FONT_BTN, bg=BTN_BG, fg=color,
                     padx=20, pady=12, cursor="hand2")
        b.pack(fill="x")
        b.bind("<Button-1>", lambda e: cmd())
        b.bind("<Enter>",    lambda e: b.configure(bg=BTN_HOV))
        b.bind("<Leave>",    lambda e: b.configure(bg=BTN_BG))
        f.bind("<Enter>",    lambda e: b.configure(bg=BTN_HOV))
        f.bind("<Leave>",    lambda e: b.configure(bg=BTN_BG))

    def _start_hvh(self):
        self.destroy()
        GameWindow(mode="hvh").mainloop()

    def _show_diff_menu(self):
        # Difficulty popup
        popup = tk.Toplevel(self)
        popup.title("Difficulty")
        popup.geometry("340x280")
        popup.configure(bg=BG)
        popup.resizable(False, False)
        popup.grab_set()

        tk.Label(popup, text="CHOOSE DIFFICULTY", font=FONT_STATUS,
                 bg=BG, fg=WHITE).pack(pady=(28,16))

        for label, key in [("😊  Easy", "easy"), ("🤔  Medium", "medium"), ("💀  Hard (Minimax)", "hard")]:
            b = tk.Button(popup, text=label, font=FONT_BTN,
                          bg=BTN_BG, fg=ACCENT1, activebackground=BTN_HOV,
                          activeforeground=ACCENT1, bd=0, pady=10,
                          cursor="hand2",
                          command=lambda k=key: self._launch_bot(popup, k))
            b.pack(padx=40, pady=6, fill="x")

        tk.Button(popup, text="← Back", font=FONT_LABEL,
                  bg=BG, fg=GRAY, bd=0, cursor="hand2",
                  command=popup.destroy).pack(pady=(12,0))

    def _launch_bot(self, popup, difficulty):
        popup.destroy()
        self.destroy()
        GameWindow(mode="hvb", difficulty=difficulty).mainloop()


# ─────────────────────────────────────────────
#  GAME WINDOW
# ─────────────────────────────────────────────
class GameWindow(tk.Tk):
    def __init__(self, mode="hvh", difficulty="hard"):
        super().__init__()
        self.mode       = mode          # "hvh" or "hvb"
        self.difficulty = difficulty
        self.board      = [""] * 9
        self.current    = "X"           # X always starts
        self.scores     = {"X": 0, "O": 0, "Draw": 0}
        self.game_over  = False
        self.buttons    = []

        if mode == "hvb":
            self.ai = AI("O", "X", difficulty)   # Bot plays as O
        else:
            self.ai = None

        title_suffix = f"vs Bot [{difficulty.capitalize()}]" if mode=="hvb" else "vs Human"
        self.title(f"Tic Tac Toe — {title_suffix}")
        self.geometry("500x640")
        self.resizable(False, False)
        self.configure(bg=BG)
        self._build_ui()

    # ── UI construction ────────────────────────
    def _build_ui(self):
        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", padx=20, pady=(16,4))

        self.back_btn = tk.Label(top, text="← Menu", font=FONT_LABEL,
                                 bg=BG, fg=GRAY, cursor="hand2")
        self.back_btn.pack(side="left")
        self.back_btn.bind("<Button-1>", self._go_menu)

        mode_txt = "👤 vs 👤" if self.mode=="hvh" else f"👤 vs 🤖 [{self.difficulty}]"
        tk.Label(top, text=mode_txt, font=FONT_LABEL, bg=BG, fg=GRAY).pack(side="right")

        # Status bar
        self.status_var = tk.StringVar(value="Player X's turn")
        tk.Label(self, textvariable=self.status_var, font=FONT_STATUS,
                 bg=BG, fg=WHITE, pady=8).pack()

        # Score board
        sf = tk.Frame(self, bg=PANEL)
        sf.pack(padx=30, pady=(0,12), fill="x")
        self.score_labels = {}
        for col, (player, color) in enumerate([("X", ACCENT1), ("Draw", WIN_LINE), ("O", ACCENT2)]):
            f = tk.Frame(sf, bg=PANEL)
            f.grid(row=0, column=col, padx=1, pady=1, sticky="nsew")
            sf.columnconfigure(col, weight=1)
            tk.Label(f, text=player, font=FONT_LABEL, bg=PANEL, fg=color).pack(pady=(8,0))
            lbl = tk.Label(f, text="0", font=FONT_STATUS, bg=PANEL, fg=color)
            lbl.pack(pady=(0,8))
            self.score_labels[player] = lbl

        # Grid canvas (for win-line drawing)
        self.canvas = tk.Canvas(self, width=420, height=420, bg=BG,
                                highlightthickness=0)
        self.canvas.pack(pady=(0,4))
        self._draw_grid()
        self._draw_buttons()

        # Restart button
        tk.Button(self, text="↺  New Game", font=FONT_BTN,
                  bg=BTN_BG, fg=ACCENT1, activebackground=BTN_HOV,
                  activeforeground=ACCENT1, bd=0, padx=20, pady=10,
                  cursor="hand2", command=self._reset).pack(pady=8)

    def _draw_grid(self):
        self.canvas.delete("grid")
        margin, size = 20, 420
        third = (size - 2*margin) / 3
        # Vertical lines
        for i in 1,2:
            x = margin + i*third
            self.canvas.create_line(x, margin, x, size-margin,
                                    fill=GRAY, width=3, tags="grid")
        # Horizontal lines
        for i in 1,2:
            y = margin + i*third
            self.canvas.create_line(margin, y, size-margin, y,
                                    fill=GRAY, width=3, tags="grid")

    def _draw_buttons(self):
        margin, size = 20, 420
        third = (size - 2*margin) / 3
        self.buttons = []
        for idx in range(9):
            row, col = divmod(idx, 3)
            x0 = margin + col*third + 4
            y0 = margin + row*third + 4
            x1 = x0 + third - 8
            y1 = y0 + third - 8
            btn_id = self.canvas.create_text(
                (x0+x1)/2, (y0+y1)/2,
                text="", font=FONT_CELL, fill=WHITE, tags=f"btn{idx}"
            )
            # Invisible clickable rectangle
            rect_id = self.canvas.create_rectangle(
                x0, y0, x1, y1,
                fill="", outline="", tags=f"rect{idx}"
            )
            self.canvas.tag_bind(f"rect{idx}", "<Button-1>",
                                 lambda e, i=idx: self._click(i))
            self.canvas.tag_bind(f"btn{idx}", "<Button-1>",
                                 lambda e, i=idx: self._click(i))
            self.canvas.tag_bind(f"rect{idx}", "<Enter>",
                                 lambda e, i=idx: self._hover(i, True))
            self.canvas.tag_bind(f"rect{idx}", "<Leave>",
                                 lambda e, i=idx: self._hover(i, False))
            self.buttons.append((rect_id, btn_id))

    # ── Game logic ─────────────────────────────
    def _click(self, idx):
        if self.game_over or self.board[idx] != "":
            return
        # In HvB mode, only allow click on X's turn
        if self.mode == "hvb" and self.current == "O":
            return
        self._place(idx)

    def _place(self, idx):
        mark  = self.current
        color = ACCENT1 if mark == "X" else ACCENT2
        self.board[idx] = mark

        # Update canvas text
        _, btn_id = self.buttons[idx]
        self.canvas.itemconfig(btn_id, text=mark, fill=color)

        winner = check_winner(self.board)
        if winner:
            self._end_game(winner)
        elif all(v != "" for v in self.board):
            self._end_game(None)
        else:
            self.current = "O" if mark == "X" else "X"
            turn_name = "Bot" if (self.mode=="hvb" and self.current=="O") else f"Player {self.current}"
            self.status_var.set(f"{turn_name}'s turn")
            if self.mode == "hvb" and self.current == "O":
                self.after(400, self._bot_move)

    def _bot_move(self):
        if self.game_over: return
        move = self.ai.best_move(self.board)
        if move is not None:
            self._place(move)

    def _hover(self, idx, entering):
        if self.game_over or self.board[idx] != "": return
        rect_id, _ = self.buttons[idx]
        self.canvas.itemconfig(rect_id, fill="#1a1a2e" if entering else "")

    def _end_game(self, winner):
        self.game_over = True
        combo = winning_combo(self.board)
        if winner:
            self.scores[winner] += 1
            self.score_labels[winner].config(text=str(self.scores[winner]))
            name = "Bot" if (self.mode=="hvb" and winner=="O") else f"Player {winner}"
            self.status_var.set(f"🎉  {name} Wins!")
            if combo:
                self._draw_win_line(combo)
        else:
            self.scores["Draw"] += 1
            self.score_labels["Draw"].config(text=str(self.scores["Draw"]))
            self.status_var.set("🤝  It's a Draw!")

    def _draw_win_line(self, combo):
        margin, size = 20, 420
        third = (size - 2*margin) / 3

        def cell_center(idx):
            r, c = divmod(idx, 3)
            cx = margin + c*third + third/2
            cy = margin + r*third + third/2
            return cx, cy

        a, b, c = combo
        x1, y1 = cell_center(a)
        x2, y2 = cell_center(c)
        self.canvas.create_line(x1, y1, x2, y2,
                                fill=WIN_LINE, width=6, capstyle="round")

    def _reset(self):
        self.board     = [""] * 9
        self.current   = "X"
        self.game_over = False
        # Clear canvas texts and win line
        for rect_id, btn_id in self.buttons:
            self.canvas.itemconfig(btn_id, text="")
            self.canvas.itemconfig(rect_id, fill="")
        self.canvas.delete("winline")
        self._draw_grid()
        self.status_var.set("Player X's turn")
        # Redraw win line removal (delete all non-grid, non-btn items)
        for item in self.canvas.find_all():
            tags = self.canvas.gettags(item)
            if "grid" not in tags and not any(t.startswith("btn") or t.startswith("rect") for t in tags):
                self.canvas.delete(item)

    def _go_menu(self, event=None):
        self.destroy()
        MainMenu().mainloop()


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    MainMenu().mainloop()
