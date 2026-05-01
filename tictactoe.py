import tkinter as tk
from tkinter import font as tkfont
import random, math

# ══════════════════════════════════════════════════════════════════
#  DESIGN TOKENS
# ══════════════════════════════════════════════════════════════════
BG        = "#070711"
SURFACE   = "#0e0e1f"
SURFACE2  = "#161628"
BORDER    = "#252540"

X_COLOR   = "#c084fc"
X_GLOW    = "#7c3aed"
X_DIM     = "#3b0764"

O_COLOR   = "#fbbf24"
O_GLOW    = "#d97706"
O_DIM     = "#451a03"

WIN_COLOR = "#34d399"

TEXT_HI   = "#f8fafc"
TEXT_MID  = "#94a3b8"
TEXT_LO   = "#334155"

FONT_MARK  = ("Georgia", 52, "bold")
FONT_HEAD  = ("Courier New", 13, "bold")
FONT_BODY  = ("Courier New", 10)
FONT_SCORE = ("Georgia", 22, "bold")
FONT_LABEL = ("Courier New", 9)

WIN_COMBOS = [
    (0,1,2),(3,4,5),(6,7,8),
    (0,3,6),(1,4,7),(2,5,8),
    (0,4,8),(2,4,6)
]

# ══════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════
def check_winner(board):
    for a,b,c in WIN_COMBOS:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    return None

def winning_combo(board):
    for a,b,c in WIN_COMBOS:
        if board[a] and board[a] == board[b] == board[c]:
            return (a,b,c)
    return None

def mark_color(m): return X_COLOR if m == "X" else O_COLOR
def lerp(a, b, t): return a + (b - a) * t
def ease_out(t):   return 1 - (1 - t) ** 3

# ══════════════════════════════════════════════════════════════════
#  MINIMAX AI
# ══════════════════════════════════════════════════════════════════
class AI:
    def __init__(self, ai_mark, human_mark, difficulty="hard"):
        self.ai, self.human, self.diff = ai_mark, human_mark, difficulty

    def best_move(self, board):
        if self.diff == "easy":
            return self._random(board)
        if self.diff == "medium":
            return self._minimax_move(board) if random.random() > 0.42 else self._random(board)
        return self._minimax_move(board)

    def _random(self, board):
        empty = [i for i,v in enumerate(board) if not v]
        return random.choice(empty) if empty else None

    def _minimax_move(self, board):
        best_val, best_idx = -math.inf, None
        for i in range(9):
            if not board[i]:
                board[i] = self.ai
                val = self._mm(board, 0, False, -math.inf, math.inf)
                board[i] = ""
                if val > best_val:
                    best_val, best_idx = val, i
        return best_idx

    def _mm(self, board, d, is_max, a, b):
        w = check_winner(board)
        if w == self.ai:    return 10 - d
        if w == self.human: return d - 10
        if all(board):      return 0
        if is_max:
            best = -math.inf
            for i in range(9):
                if not board[i]:
                    board[i] = self.ai
                    best = max(best, self._mm(board, d+1, False, a, b))
                    board[i] = ""
                    a = max(a, best)
                    if b <= a: break
            return best
        else:
            best = math.inf
            for i in range(9):
                if not board[i]:
                    board[i] = self.human
                    best = min(best, self._mm(board, d+1, True, a, b))
                    board[i] = ""
                    b = min(b, best)
                    if b <= a: break
            return best

# ══════════════════════════════════════════════════════════════════
#  SCREEN BASE
# ══════════════════════════════════════════════════════════════════
class Screen(tk.Tk):
    def __init__(self, w=520, h=680):
        super().__init__()
        self.configure(bg=BG)
        self.resizable(False, False)
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

# ══════════════════════════════════════════════════════════════════
#  MAIN MENU
# ══════════════════════════════════════════════════════════════════
class MainMenu(Screen):
    def __init__(self):
        super().__init__(520, 660)
        self.title("Tic Tac Toe")
        self._draw()

    def _draw(self):
        hdr = tk.Frame(self, bg=BG)
        hdr.pack(fill="x", pady=(54, 0))
        row = tk.Frame(hdr, bg=BG)
        row.pack()
        chars  = list("TIC TAC TOE")
        colors = [X_COLOR, TEXT_MID, TEXT_MID,
                  O_COLOR, TEXT_MID, TEXT_MID,
                  X_COLOR, TEXT_MID, TEXT_MID,
                  O_COLOR, X_COLOR]
        for ch, col in zip(chars, colors):
            tk.Label(row, text=ch, font=("Georgia", 30, "bold"),
                     bg=BG, fg=col, padx=1).pack(side="left")

        tk.Label(self, text="a python experiment",
                 font=("Courier New", 10), bg=BG, fg=TEXT_LO).pack(pady=(6, 0))

        tk.Frame(self, height=1, bg=BORDER).pack(fill="x", padx=50, pady=22)
        tk.Label(self, text="CHOOSE MODE", font=FONT_HEAD,
                 bg=BG, fg=TEXT_MID).pack(pady=(0, 14))

        self._card("Human  x  Human", "Two players, same screen", X_COLOR, self._go_hvh)
        self._card("Human  x  Bot",   "Face the Minimax machine", O_COLOR, self._go_hvb)

        tk.Frame(self, height=1, bg=BORDER).pack(fill="x", padx=50, pady=22)

        q = tk.Label(self, text="QUIT", font=FONT_HEAD,
                     bg=BG, fg=TEXT_LO, cursor="hand2")
        q.pack(pady=4)
        q.bind("<Button-1>", lambda e: self.destroy())
        q.bind("<Enter>",    lambda e: q.config(fg=TEXT_MID))
        q.bind("<Leave>",    lambda e: q.config(fg=TEXT_LO))

        tk.Label(self, text="X moves first  .  bot plays Minimax a-b",
                 font=FONT_LABEL, bg=BG, fg=TEXT_LO).pack(side="bottom", pady=18)

    def _card(self, title, subtitle, accent, cmd):
        outer = tk.Frame(self, bg=accent, padx=1, pady=1)
        outer.pack(padx=54, pady=7, fill="x")
        inner = tk.Frame(outer, bg=SURFACE, cursor="hand2")
        inner.pack(fill="both")

        title_lbl = tk.Label(inner, text=title, font=("Georgia", 14, "bold"),
                             bg=SURFACE, fg=accent, pady=12)
        title_lbl.pack()
        sub_lbl = tk.Label(inner, text=subtitle, font=FONT_LABEL,
                           bg=SURFACE, fg=TEXT_MID)
        sub_lbl.pack(pady=(0, 12))

        # FIX: use a list, not tuple concatenation
        widgets = [outer, inner, title_lbl, sub_lbl]
        for w in widgets:
            w.bind("<Button-1>", lambda e: cmd())
            w.bind("<Enter>",    lambda e, i=inner: i.config(bg=SURFACE2))
            w.bind("<Leave>",    lambda e, i=inner: i.config(bg=SURFACE))

    def _go_hvh(self):
        self.destroy()
        MarkPicker(mode="hvh").mainloop()

    def _go_hvb(self):
        self.destroy()
        MarkPicker(mode="hvb").mainloop()

# ══════════════════════════════════════════════════════════════════
#  MARK PICKER
# ══════════════════════════════════════════════════════════════════
class MarkPicker(Screen):
    def __init__(self, mode="hvh"):
        super().__init__(520, 540)
        self.mode   = mode
        self.chosen = tk.StringVar(value="X")
        self.diff   = tk.StringVar(value="hard")
        self.title("Choose Your Mark")
        self._draw()

    def _draw(self):
        tk.Label(self, text="PICK YOUR MARK", font=FONT_HEAD,
                 bg=BG, fg=TEXT_MID).pack(pady=(44, 20))

        row = tk.Frame(self, bg=BG)
        row.pack()
        self.xcard = self._mcard(row, "X", X_COLOR, X_GLOW, X_DIM)
        tk.Label(row, text="or", font=("Courier New", 11),
                 bg=BG, fg=TEXT_LO).pack(side="left", padx=18)
        self.ocard = self._mcard(row, "O", O_COLOR, O_GLOW, O_DIM)
        self._refresh()

        tk.Frame(self, height=1, bg=BORDER).pack(fill="x", padx=50, pady=22)

        if self.mode == "hvb":
            tk.Label(self, text="BOT DIFFICULTY", font=FONT_HEAD,
                     bg=BG, fg=TEXT_MID).pack(pady=(0, 14))
            drow = tk.Frame(self, bg=BG)
            drow.pack()
            self.dpills = []
            for label, key in [("Easy","easy"), ("Medium","medium"), ("Hard","hard")]:
                p = tk.Label(drow, text=label, font=FONT_BODY,
                             bg=SURFACE2, fg=TEXT_MID,
                             padx=18, pady=7, cursor="hand2")
                p._key = key
                p.pack(side="left", padx=5)
                p.bind("<Button-1>", lambda e, k=key: self._pick_diff(k))
                self.dpills.append(p)
            self._pick_diff("hard")
            tk.Frame(self, height=1, bg=BORDER).pack(fill="x", padx=50, pady=22)

        self._start_section()

        back = tk.Label(self, text="<- back", font=FONT_LABEL,
                        bg=BG, fg=TEXT_LO, cursor="hand2")
        back.pack(pady=(14, 0))
        back.bind("<Button-1>", lambda e: self._go_back())
        back.bind("<Enter>",    lambda e: back.config(fg=TEXT_MID))
        back.bind("<Leave>",    lambda e: back.config(fg=TEXT_LO))

    def _mcard(self, parent, mark, accent, glow, dim):
        f = tk.Frame(parent, bg=dim, padx=2, pady=2, cursor="hand2")
        f.pack(side="left")
        inner = tk.Frame(f, bg=SURFACE, width=110, height=110)
        inner.pack_propagate(False)
        inner.pack()
        lbl = tk.Label(inner, text=mark, font=("Georgia", 46, "bold"),
                       bg=SURFACE, fg=accent)
        lbl.pack(expand=True)
        for w in [f, inner, lbl]:
            w.bind("<Button-1>", lambda e, m=mark: self._pick_mark(m))
        return f

    def _pick_mark(self, m):
        self.chosen.set(m)
        self._refresh()
        if hasattr(self, "start_outer"):
            self.start_outer.config(bg=X_COLOR if m == "X" else O_COLOR)

    def _refresh(self):
        m = self.chosen.get()
        self.xcard.config(bg=X_GLOW if m == "X" else BORDER)
        self.ocard.config(bg=O_GLOW if m == "O" else BORDER)

    def _pick_diff(self, key):
        self.diff.set(key)
        if hasattr(self, "dpills"):
            for p in self.dpills:
                active = p._key == key
                p.config(bg=O_GLOW if active else SURFACE2,
                         fg=TEXT_HI if active else TEXT_MID)

    def _start_section(self):
        c = X_COLOR if self.chosen.get() == "X" else O_COLOR
        self.start_outer = tk.Frame(self, bg=c, padx=1, pady=1)
        self.start_outer.pack(padx=80, fill="x")
        inner = tk.Frame(self.start_outer, bg=SURFACE2, cursor="hand2")
        inner.pack(fill="both")
        lbl = tk.Label(inner, text="START GAME", font=FONT_HEAD,
                       bg=SURFACE2, fg=TEXT_HI, pady=13)
        lbl.pack()
        for w in [self.start_outer, inner, lbl]:
            w.bind("<Button-1>", lambda e: self._launch())
            w.bind("<Enter>",    lambda e: inner.config(bg=BORDER))
            w.bind("<Leave>",    lambda e: inner.config(bg=SURFACE2))

    def _launch(self):
        self.destroy()
        GameWindow(mode=self.mode,
                   player_mark=self.chosen.get(),
                   difficulty=self.diff.get()).mainloop()

    def _go_back(self):
        self.destroy()
        MainMenu().mainloop()

# ══════════════════════════════════════════════════════════════════
#  GAME WINDOW
# ══════════════════════════════════════════════════════════════════
class GameWindow(Screen):
    CELL   = 126
    MARGIN = 24

    def __init__(self, mode="hvh", player_mark="X", difficulty="hard"):
        super().__init__(520, 700)
        self.mode       = mode
        self.p_mark     = player_mark
        self.bot_mark   = "O" if player_mark == "X" else "X"
        self.difficulty = difficulty
        self.board      = [""] * 9
        self.current    = "X"
        self.scores     = {"X": 0, "O": 0, "D": 0}
        self.game_over  = False
        self.btns       = []
        self.pulse_jobs = []
        self.ai = AI(self.bot_mark, self.p_mark, difficulty) if mode == "hvb" else None
        self.title("Tic Tac Toe")
        self._build()

    def _build(self):
        nav = tk.Frame(self, bg=BG)
        nav.pack(fill="x", padx=20, pady=(14, 0))
        back = tk.Label(nav, text="<- menu", font=FONT_LABEL,
                        bg=BG, fg=TEXT_LO, cursor="hand2")
        back.pack(side="left")
        back.bind("<Button-1>", lambda e: self._go_menu())
        back.bind("<Enter>",    lambda e: back.config(fg=TEXT_MID))
        back.bind("<Leave>",    lambda e: back.config(fg=TEXT_LO))

        ml = "Human  x  Human" if self.mode == "hvh" else f"Human  x  Bot  [{self.difficulty}]"
        tk.Label(nav, text=ml, font=FONT_LABEL, bg=BG, fg=TEXT_LO).pack(side="right")

        self._build_scores()

        self.status_var = tk.StringVar()
        self.status_lbl = tk.Label(self, textvariable=self.status_var,
                                   font=("Courier New", 12, "bold"),
                                   bg=BG, fg=TEXT_MID, pady=10)
        self.status_lbl.pack()
        self._set_status()

        cs = self.CELL * 3 + self.MARGIN * 2
        self.canvas = tk.Canvas(self, width=cs, height=cs,
                                bg=BG, highlightthickness=0)
        self.canvas.pack()
        self._draw_grid()
        self._draw_cells()

        btn = tk.Label(self, text="new game", font=FONT_HEAD,
                       bg=BG, fg=TEXT_LO, pady=14, cursor="hand2")
        btn.pack(pady=(14, 0))
        btn.bind("<Button-1>", lambda e: self._reset())
        btn.bind("<Enter>",    lambda e: btn.config(fg=TEXT_MID))
        btn.bind("<Leave>",    lambda e: btn.config(fg=TEXT_LO))

        if self.mode == "hvb" and self.bot_mark == "X":
            self.after(600, self._bot_move)

    def _build_scores(self):
        sf = tk.Frame(self, bg=SURFACE)
        sf.pack(padx=40, pady=(18, 0), fill="x")
        self.score_vars = {}

        if self.mode == "hvh":
            cols = [("X", X_COLOR, "Player 1"),
                    ("D", TEXT_MID, "Draw"),
                    ("O", O_COLOR,  "Player 2")]
        else:
            you  = "You" if self.p_mark == "X" else "Bot"
            them = "Bot" if self.p_mark == "X" else "You"
            x_name = you  if self.p_mark == "X" else them
            o_name = them if self.p_mark == "X" else you
            cols = [("X", X_COLOR, x_name),
                    ("D", TEXT_MID, "Draw"),
                    ("O", O_COLOR,  o_name)]

        for idx, (key, color, name) in enumerate(cols):
            cell = tk.Frame(sf, bg=SURFACE)
            cell.grid(row=0, column=idx, sticky="nsew", padx=1)
            sf.columnconfigure(idx, weight=1)
            tk.Label(cell, text=name.upper(), font=FONT_LABEL,
                     bg=SURFACE, fg=TEXT_MID).pack(pady=(10, 0))
            var = tk.StringVar(value="0")
            self.score_vars[key] = var
            tk.Label(cell, textvariable=var, font=FONT_SCORE,
                     bg=SURFACE, fg=color).pack(pady=(2, 10))

    def _draw_grid(self):
        self.canvas.delete("grid")
        M, C = self.MARGIN, self.CELL
        total = C * 3 + M * 2
        for i in range(9):
            r, c = divmod(i, 3)
            x0 = M + c*C + 4
            y0 = M + r*C + 4
            self.canvas.create_rectangle(x0, y0, x0+C-8, y0+C-8,
                fill=SURFACE, outline="", tags="grid")
        for i in [1, 2]:
            x = M + i*C
            y = M + i*C
            self.canvas.create_line(x, M, x, total-M, fill=BORDER, width=2, tags="grid")
            self.canvas.create_line(M, y, total-M, y, fill=BORDER, width=2, tags="grid")

    def _draw_cells(self):
        self.btns = []
        M, C = self.MARGIN, self.CELL
        for idx in range(9):
            r, c = divmod(idx, 3)
            x0 = M + c*C + 4
            y0 = M + r*C + 4
            x1 = x0 + C - 8
            y1 = y0 + C - 8
            rect = self.canvas.create_rectangle(x0, y0, x1, y1,
                fill="", outline="", tags=f"r{idx}")
            text = self.canvas.create_text((x0+x1)/2, (y0+y1)/2,
                text="", font=FONT_MARK, fill=TEXT_HI, tags=f"t{idx}")
            self.canvas.tag_bind(f"r{idx}", "<Button-1>", lambda e, i=idx: self._click(i))
            self.canvas.tag_bind(f"t{idx}", "<Button-1>", lambda e, i=idx: self._click(i))
            self.canvas.tag_bind(f"r{idx}", "<Enter>",    lambda e, i=idx: self._hover(i, True))
            self.canvas.tag_bind(f"r{idx}", "<Leave>",    lambda e, i=idx: self._hover(i, False))
            self.btns.append((rect, text, x0, y0, x1, y1))

    def _cell_center(self, idx):
        _, _, x0, y0, x1, y1 = self.btns[idx]
        return (x0+x1)/2, (y0+y1)/2

    def _click(self, idx):
        if self.game_over or self.board[idx]: return
        if self.mode == "hvb" and self.current == self.bot_mark: return
        self._place(idx)

    def _hover(self, idx, on):
        if self.game_over or self.board[idx]: return
        rect = self.btns[idx][0]
        self.canvas.itemconfig(rect, fill=SURFACE2 if on else "")

    def _place(self, idx):
        mark = self.current
        self.board[idx] = mark
        rect, text = self.btns[idx][0], self.btns[idx][1]
        self.canvas.itemconfig(rect, fill="")
        self.canvas.itemconfig(text, text=mark, fill=mark_color(mark))
        self._anim_pop(idx, 0)

        winner = check_winner(self.board)
        if winner:
            self.after(160, lambda: self._end(winner))
        elif all(self.board):
            self.after(160, lambda: self._end(None))
        else:
            self.current = "O" if mark == "X" else "X"
            self._set_status()
            if self.mode == "hvb" and self.current == self.bot_mark:
                self.after(480, self._bot_move)

    def _bot_move(self):
        if self.game_over: return
        mv = self.ai.best_move(self.board)
        if mv is not None:
            self._place(mv)

    def _anim_pop(self, idx, step, total=8):
        text = self.btns[idx][1]
        t    = ease_out(step / total)
        size = int(lerp(18, 52, t))
        try:
            f = tkfont.Font(family="Georgia", size=size, weight="bold")
            self.canvas.itemconfig(text, font=f)
        except Exception:
            pass
        if step < total:
            self.after(18, lambda: self._anim_pop(idx, step+1, total))

    def _anim_win(self, combo, step=0, total=18):
        a, _, c = combo
        ax, ay  = self._cell_center(a)
        cx, cy  = self._cell_center(c)
        t = ease_out(step / total)
        self.canvas.delete("winline")
        self.canvas.create_line(ax, ay, lerp(ax, cx, t), lerp(ay, cy, t),
            fill=WIN_COLOR, width=5, capstyle="round", tags="winline")
        if step < total:
            self.after(16, lambda: self._anim_win(combo, step+1, total))
        else:
            for i in combo:
                self._pulse(i, 0)

    def _pulse(self, idx, step):
        text = self.btns[idx][1]
        t    = (1 + math.sin(step * 0.6)) / 2
        size = int(lerp(46, 54, t))
        try:
            f = tkfont.Font(family="Georgia", size=size, weight="bold")
            self.canvas.itemconfig(text, font=f)
        except Exception:
            pass
        job = self.after(55, lambda: self._pulse(idx, step+1))
        self.pulse_jobs.append(job)

    def _stop_pulses(self):
        for j in self.pulse_jobs:
            try: self.after_cancel(j)
            except Exception: pass
        self.pulse_jobs.clear()

    def _set_status(self):
        m = self.current
        if self.mode == "hvh":
            name = f"Player  {m}'s  turn"
        else:
            name = "Your turn" if m == self.p_mark else "Bot is thinking..."
        self.status_var.set(name)
        if hasattr(self, "status_lbl"):
            self.status_lbl.config(fg=mark_color(m))

    def _end(self, winner):
        self.game_over = True
        if winner:
            self.scores[winner] += 1
            self.score_vars[winner].set(str(self.scores[winner]))
            if self.mode == "hvh":
                msg = f"Player {winner} wins"
            else:
                msg = "You win!" if winner == self.p_mark else "Bot wins"
            self.status_var.set(msg)
            self.status_lbl.config(fg=WIN_COLOR)
            combo = winning_combo(self.board)
            if combo:
                self._anim_win(combo)
        else:
            self.scores["D"] += 1
            self.score_vars["D"].set(str(self.scores["D"]))
            self.status_var.set("Draw")
            self.status_lbl.config(fg=TEXT_MID)

    def _reset(self):
        self._stop_pulses()
        self.board     = [""] * 9
        self.current   = "X"
        self.game_over = False
        self.canvas.delete("winline")
        for rect, text, *_ in self.btns:
            self.canvas.itemconfig(rect, fill="")
            self.canvas.itemconfig(text, text="", font=("Georgia", 52, "bold"))
        self._set_status()
        if self.mode == "hvb" and self.bot_mark == "X":
            self.after(600, self._bot_move)

    def _go_menu(self):
        self._stop_pulses()
        self.destroy()
        MainMenu().mainloop()

# ══════════════════════════════════════════════════════════════════
#  ENTRY
# ══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    MainMenu().mainloop()
