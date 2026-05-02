import tkinter as tk
from tkinter import font as tkfont
import random, math, time

# ══════════════════════════════════════════════════════════════════
#  DESIGN TOKENS — Cyberpunk / Neon 3D Theme
# ══════════════════════════════════════════════════════════════════
BG         = "#04040f"
SURFACE    = "#0a0a1e"
SURFACE2   = "#12122a"
SURFACE3   = "#1a1a38"
BORDER     = "#1e1e40"
BORDER2    = "#2a2a55"

X_COLOR    = "#00f5ff"   # cyan neon
X_GLOW     = "#0099bb"
X_DIM      = "#002233"
X_SHADOW   = "#001a2a"

O_COLOR    = "#ff6b35"   # neon orange
O_GLOW     = "#cc4422"
O_DIM      = "#2a1100"
O_SHADOW   = "#1a0a00"

WIN_COLOR  = "#39ff14"   # neon green
WIN_GLOW   = "#22cc0e"

DRAW_COLOR = "#a855f7"   # purple

GOLD       = "#ffd700"
SILVER     = "#c0c0c0"

TEXT_HI    = "#ffffff"
TEXT_MID   = "#8899bb"
TEXT_LO    = "#334466"
TEXT_DIM   = "#1a2244"

FONT_MARK   = ("Courier New", 48, "bold")
FONT_HEAD   = ("Courier New", 13, "bold")
FONT_HEAD2  = ("Courier New", 11, "bold")
FONT_BODY   = ("Courier New", 10)
FONT_SCORE  = ("Courier New", 24, "bold")
FONT_LABEL  = ("Courier New", 9)
FONT_BIG    = ("Courier New", 28, "bold")
FONT_TITLE  = ("Courier New", 32, "bold")

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
def mark_glow(m):  return X_GLOW  if m == "X" else O_GLOW
def lerp(a, b, t): return a + (b - a) * t
def ease_out(t):   return 1 - (1 - t) ** 3
def ease_in_out(t): return t * t * (3 - 2 * t)

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
    def __init__(self, w=560, h=720):
        super().__init__()
        self.configure(bg=BG)
        self.resizable(False, False)
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

# ══════════════════════════════════════════════════════════════════
#  NEON BUTTON WIDGET
# ══════════════════════════════════════════════════════════════════
def neon_btn(parent, text, color, cmd, font=FONT_HEAD, padx=30, pady=12, width=None):
    outer = tk.Frame(parent, bg=color, padx=1, pady=1)
    if width:
        outer.pack_propagate(False)
    inner = tk.Frame(outer, bg=SURFACE2, cursor="hand2")
    inner.pack(fill="both")
    kw = dict(text=text, font=font, bg=SURFACE2, fg=color, pady=pady, cursor="hand2")
    if width:
        kw["width"] = width
    lbl = tk.Label(inner, **kw)
    lbl.pack(padx=padx)

    def on_enter(e): inner.config(bg=SURFACE3); lbl.config(bg=SURFACE3)
    def on_leave(e): inner.config(bg=SURFACE2); lbl.config(bg=SURFACE2)
    def on_click(e): cmd()

    for w in [outer, inner, lbl]:
        w.bind("<Button-1>", on_click)
        w.bind("<Enter>", on_enter)
        w.bind("<Leave>", on_leave)
    return outer

# ══════════════════════════════════════════════════════════════════
#  SCANLINE CANVAS OVERLAY
# ══════════════════════════════════════════════════════════════════
def draw_scanlines(canvas, w, h, step=4):
    for y in range(0, h, step):
        canvas.create_line(0, y, w, y, fill="#ffffff", stipple="gray12", tags="scan")

# ══════════════════════════════════════════════════════════════════
#  MAIN MENU
# ══════════════════════════════════════════════════════════════════
class MainMenu(Screen):
    def __init__(self):
        super().__init__(560, 680)
        self.title("TIC TAC TOE — NEON EDITION")
        self._draw()

    def _draw(self):
        # Top neon strip
        strip = tk.Canvas(self, height=4, bg=BG, highlightthickness=0)
        strip.pack(fill="x")
        strip.create_line(0, 2, 1200, 2, fill=X_COLOR, width=3)

        # Title area
        hdr = tk.Frame(self, bg=BG)
        hdr.pack(fill="x", pady=(40, 0))

        # Animated title rows
        row1 = tk.Frame(hdr, bg=BG); row1.pack()
        title_chars = [
            ("T",X_COLOR),("I",TEXT_MID),("C",TEXT_MID),
            (" ",BG),
            ("T",O_COLOR),("A",TEXT_MID),("C",TEXT_MID),
            (" ",BG),
            ("T",X_COLOR),("O",TEXT_MID),("E",TEXT_MID),
        ]
        for ch, col in title_chars:
            lbl = tk.Label(row1, text=ch, font=("Courier New", 34, "bold"),
                           bg=BG, fg=col, padx=1)
            lbl.pack(side="left")

        tk.Label(self, text="━━━━━━━━━━  N E O N  E D I T I O N  ━━━━━━━━━━",
                 font=("Courier New", 9), bg=BG, fg=TEXT_LO).pack(pady=(4,0))

        # Corner markers — 3D feel
        marker_row = tk.Frame(self, bg=BG)
        marker_row.pack(pady=(2,0))
        tk.Label(marker_row, text="[ X ]", font=("Courier New",11,"bold"),
                 bg=BG, fg=X_COLOR).pack(side="left", padx=30)
        tk.Label(marker_row, text="v 2.0", font=("Courier New",9),
                 bg=BG, fg=TEXT_LO).pack(side="left", padx=20)
        tk.Label(marker_row, text="[ O ]", font=("Courier New",11,"bold"),
                 bg=BG, fg=O_COLOR).pack(side="left", padx=30)

        # Divider
        self._divider()
        tk.Label(self, text="SELECT  MODE", font=FONT_HEAD,
                 bg=BG, fg=TEXT_MID).pack(pady=(0,14))

        self._card("⚡  HUMAN   VS   HUMAN", "Two players · same screen · local PvP",
                   X_COLOR, self._go_hvh)
        tk.Frame(self, height=6, bg=BG).pack()
        self._card("🤖  HUMAN   VS   BOT",  "Challenge the Minimax AI · alpha-beta pruning",
                   O_COLOR, self._go_hvb)

        self._divider()

        # Stats bar
        stats = tk.Frame(self, bg=SURFACE)
        stats.pack(padx=40, fill="x")
        for txt, val, col in [("MINIMAX", "A-β", X_COLOR), ("MODES", "2", TEXT_MID), ("DIFFICULTY", "3", O_COLOR)]:
            c = tk.Frame(stats, bg=SURFACE)
            c.pack(side="left", expand=True, pady=10)
            tk.Label(c, text=val, font=("Courier New",18,"bold"), bg=SURFACE, fg=col).pack()
            tk.Label(c, text=txt, font=FONT_LABEL, bg=SURFACE, fg=TEXT_MID).pack()

        self._divider()

        quit_lbl = tk.Label(self, text="[ QUIT ]", font=FONT_HEAD,
                            bg=BG, fg=TEXT_LO, cursor="hand2")
        quit_lbl.pack(pady=4)
        quit_lbl.bind("<Button-1>", lambda e: self.destroy())
        quit_lbl.bind("<Enter>",    lambda e: quit_lbl.config(fg=TEXT_MID))
        quit_lbl.bind("<Leave>",    lambda e: quit_lbl.config(fg=TEXT_LO))

        # Bottom strip
        bot_strip = tk.Canvas(self, height=4, bg=BG, highlightthickness=0)
        bot_strip.pack(fill="x", side="bottom")
        bot_strip.create_line(0, 2, 1200, 2, fill=O_COLOR, width=3)

    def _divider(self):
        tk.Frame(self, height=1, bg=BORDER2).pack(fill="x", padx=40, pady=16)

    def _card(self, title, subtitle, accent, cmd):
        outer = tk.Frame(self, bg=accent, padx=1, pady=1)
        outer.pack(padx=50, pady=0, fill="x")
        inner = tk.Frame(outer, bg=SURFACE, cursor="hand2")
        inner.pack(fill="both")

        # Left accent bar
        bar = tk.Frame(inner, bg=accent, width=4)
        bar.pack(side="left", fill="y")

        content = tk.Frame(inner, bg=SURFACE)
        content.pack(side="left", fill="both", expand=True, padx=16)

        title_lbl = tk.Label(content, text=title, font=("Courier New",13,"bold"),
                             bg=SURFACE, fg=accent, pady=12, anchor="w")
        title_lbl.pack(fill="x")
        sub_lbl = tk.Label(content, text=subtitle, font=FONT_LABEL,
                           bg=SURFACE, fg=TEXT_MID, anchor="w")
        sub_lbl.pack(fill="x", pady=(0,12))

        arrow = tk.Label(inner, text=" ▶ ", font=("Courier New",16,"bold"),
                         bg=SURFACE, fg=accent, padx=12)
        arrow.pack(side="right", fill="y")

        widgets = [outer, inner, content, title_lbl, sub_lbl, arrow, bar]
        for w in widgets:
            w.bind("<Button-1>", lambda e: cmd())
            w.bind("<Enter>",    lambda e, i=inner, b=bar, a=arrow, t=title_lbl, s=sub_lbl:
                   (i.config(bg=SURFACE2), b.config(bg=accent),
                    a.config(bg=SURFACE2), t.config(bg=SURFACE2), s.config(bg=SURFACE2),
                    content.config(bg=SURFACE2)))
            w.bind("<Leave>",    lambda e, i=inner, b=bar, a=arrow, t=title_lbl, s=sub_lbl:
                   (i.config(bg=SURFACE), b.config(bg=accent),
                    a.config(bg=SURFACE), t.config(bg=SURFACE), s.config(bg=SURFACE),
                    content.config(bg=SURFACE)))

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
        super().__init__(560, 560)
        self.mode   = mode
        self.chosen = tk.StringVar(value="X")
        self.diff   = tk.StringVar(value="hard")
        self.title("Choose Your Mark")
        self._draw()

    def _draw(self):
        # Top strip
        strip = tk.Canvas(self, height=4, bg=BG, highlightthickness=0)
        strip.pack(fill="x")
        strip.create_line(0, 2, 1200, 2, fill=X_COLOR, width=3)

        tk.Label(self, text="CHOOSE  YOUR  MARK", font=FONT_HEAD,
                 bg=BG, fg=TEXT_MID).pack(pady=(32, 20))

        row = tk.Frame(self, bg=BG)
        row.pack()
        self.xcard = self._mcard(row, "X", X_COLOR, X_GLOW, X_DIM)
        tk.Label(row, text="  vs  ", font=("Courier New", 12, "bold"),
                 bg=BG, fg=TEXT_LO).pack(side="left")
        self.ocard = self._mcard(row, "O", O_COLOR, O_GLOW, O_DIM)
        self._refresh()

        tk.Frame(self, height=1, bg=BORDER2).pack(fill="x", padx=50, pady=20)

        if self.mode == "hvb":
            tk.Label(self, text="BOT  DIFFICULTY", font=FONT_HEAD,
                     bg=BG, fg=TEXT_MID).pack(pady=(0, 14))
            drow = tk.Frame(self, bg=BG)
            drow.pack()
            self.dpills = []
            for label, key, col in [("EASY","easy",WIN_COLOR),
                                     ("MEDIUM","medium",O_COLOR),
                                     ("HARD","hard",X_COLOR)]:
                p = tk.Label(drow, text=label, font=FONT_HEAD2,
                             bg=SURFACE2, fg=TEXT_MID,
                             padx=20, pady=9, cursor="hand2",
                             relief="flat", bd=0)
                p._key = key
                p._col = col
                p.pack(side="left", padx=6)
                p.bind("<Button-1>", lambda e, k=key: self._pick_diff(k))
                self.dpills.append(p)
            self._pick_diff("hard")
            tk.Frame(self, height=1, bg=BORDER2).pack(fill="x", padx=50, pady=20)

        self._start_section()

        back = tk.Label(self, text="◀  BACK TO MENU", font=FONT_LABEL,
                        bg=BG, fg=TEXT_LO, cursor="hand2")
        back.pack(pady=(16, 0))
        back.bind("<Button-1>", lambda e: self._go_back())
        back.bind("<Enter>",    lambda e: back.config(fg=TEXT_MID))
        back.bind("<Leave>",    lambda e: back.config(fg=TEXT_LO))

        # Bottom strip
        bot_strip = tk.Canvas(self, height=4, bg=BG, highlightthickness=0)
        bot_strip.pack(fill="x", side="bottom")
        bot_strip.create_line(0, 2, 1200, 2, fill=O_COLOR, width=3)

    def _mcard(self, parent, mark, accent, glow, dim):
        outer = tk.Frame(parent, bg=dim, padx=2, pady=2, cursor="hand2")
        outer.pack(side="left", padx=8)

        inner = tk.Frame(outer, bg=SURFACE, width=120, height=120)
        inner.pack_propagate(False)
        inner.pack()

        # Shadow effect layers
        shadow = tk.Frame(inner, bg=dim, height=4)
        shadow.pack(side="bottom", fill="x")

        lbl = tk.Label(inner, text=mark, font=("Courier New", 50, "bold"),
                       bg=SURFACE, fg=accent)
        lbl.pack(expand=True)

        # Glow label below
        glow_lbl = tk.Label(outer, text=f"── {mark} ──", font=FONT_LABEL,
                            bg=dim, fg=accent)
        glow_lbl.pack(pady=(3,0))

        for w in [outer, inner, lbl, shadow, glow_lbl]:
            w.bind("<Button-1>", lambda e, m=mark: self._pick_mark(m))
        return outer

    def _pick_mark(self, m):
        self.chosen.set(m)
        self._refresh()

    def _refresh(self):
        m = self.chosen.get()
        xsel = m == "X"
        self.xcard.config(bg=X_GLOW if xsel else BORDER)
        self.ocard.config(bg=O_GLOW if not xsel else BORDER)
        # Update start button color
        if hasattr(self, "start_outer"):
            col = X_COLOR if xsel else O_COLOR
            self.start_outer.config(bg=col)

    def _pick_diff(self, key):
        self.diff.set(key)
        if hasattr(self, "dpills"):
            for p in self.dpills:
                active = p._key == key
                p.config(bg=p._col if active else SURFACE2,
                         fg=BG if active else TEXT_MID)

    def _start_section(self):
        m = self.chosen.get()
        col = X_COLOR if m == "X" else O_COLOR
        self.start_outer = tk.Frame(self, bg=col, padx=1, pady=1)
        self.start_outer.pack(padx=70, fill="x")
        inner = tk.Frame(self.start_outer, bg=SURFACE2, cursor="hand2")
        inner.pack(fill="both")
        lbl = tk.Label(inner, text="▶  START  GAME", font=FONT_HEAD,
                       bg=SURFACE2, fg=TEXT_HI, pady=14)
        lbl.pack()
        for w in [self.start_outer, inner, lbl]:
            w.bind("<Button-1>", lambda e: self._launch())
            w.bind("<Enter>",    lambda e: (inner.config(bg=SURFACE3), lbl.config(bg=SURFACE3)))
            w.bind("<Leave>",    lambda e: (inner.config(bg=SURFACE2), lbl.config(bg=SURFACE2)))

    def _launch(self):
        self.destroy()
        GameWindow(mode=self.mode,
                   player_mark=self.chosen.get(),
                   difficulty=self.diff.get()).mainloop()

    def _go_back(self):
        self.destroy()
        MainMenu().mainloop()

# ══════════════════════════════════════════════════════════════════
#  RESULT OVERLAY — Full screen win/draw/lose popup
# ══════════════════════════════════════════════════════════════════
class ResultOverlay(tk.Toplevel):
    def __init__(self, parent, result_text, sub_text, color,
                 on_again, on_menu, scores, mode, p_mark):
        super().__init__(parent)
        self.overrideredirect(True)
        self.configure(bg=BG)
        self.resizable(False, False)

        # Position over parent
        px = parent.winfo_x()
        py = parent.winfo_y()
        pw = parent.winfo_width()
        ph = parent.winfo_height()
        w, h = 460, 380
        self.geometry(f"{w}x{h}+{px+(pw-w)//2}+{py+(ph-h)//2}")

        self.lift()
        self.grab_set()

        self._build(result_text, sub_text, color, on_again, on_menu, scores, mode, p_mark)
        self._animate_in(0)

    def _build(self, result_text, sub_text, color, on_again, on_menu, scores, mode, p_mark):
        # Outer border
        border = tk.Frame(self, bg=color, padx=2, pady=2)
        border.pack(fill="both", expand=True, padx=0, pady=0)

        main = tk.Frame(border, bg=BG)
        main.pack(fill="both", expand=True)

        # Corner brackets 3D effect
        corners = tk.Frame(main, bg=BG)
        corners.pack(fill="x", padx=10, pady=(10,0))
        tk.Label(corners, text="╔══", font=("Courier New",10), bg=BG, fg=color).pack(side="left")
        tk.Label(corners, text="══╗", font=("Courier New",10), bg=BG, fg=color).pack(side="right")

        # Main result
        self.result_lbl = tk.Label(main, text=result_text,
                                   font=("Courier New", 36, "bold"),
                                   bg=BG, fg=color)
        self.result_lbl.pack(pady=(10, 4))

        tk.Label(main, text=sub_text, font=("Courier New", 12),
                 bg=BG, fg=TEXT_MID).pack(pady=(0, 8))

        # Score summary inside overlay
        tk.Frame(main, height=1, bg=BORDER2).pack(fill="x", padx=30, pady=8)

        sf = tk.Frame(main, bg=SURFACE)
        sf.pack(padx=30, fill="x")

        if mode == "hvh":
            cols = [("P1", "X", X_COLOR), ("DRAW", "D", TEXT_MID), ("P2", "O", O_COLOR)]
        else:
            you  = "YOU" if p_mark == "X" else "BOT"
            them = "BOT" if p_mark == "X" else "YOU"
            x_n = you  if p_mark == "X" else them
            o_n = them if p_mark == "X" else you
            cols = [(x_n, "X", X_COLOR), ("DRAW", "D", TEXT_MID), (o_n, "O", O_COLOR)]

        for lbl, key, col in cols:
            c = tk.Frame(sf, bg=SURFACE)
            c.pack(side="left", expand=True, pady=8)
            tk.Label(c, text=str(scores[key]), font=("Courier New",20,"bold"),
                     bg=SURFACE, fg=col).pack()
            tk.Label(c, text=lbl, font=FONT_LABEL, bg=SURFACE, fg=TEXT_MID).pack()

        tk.Frame(main, height=1, bg=BORDER2).pack(fill="x", padx=30, pady=10)

        # Buttons row
        btn_row = tk.Frame(main, bg=BG)
        btn_row.pack(pady=(0, 14))

        # PLAY AGAIN button
        again_outer = tk.Frame(btn_row, bg=color, padx=1, pady=1)
        again_outer.pack(side="left", padx=10)
        again_inner = tk.Frame(again_outer, bg=SURFACE2, cursor="hand2")
        again_inner.pack(fill="both")
        again_lbl = tk.Label(again_inner, text="▶  PLAY  AGAIN",
                             font=("Courier New",10,"bold"),
                             bg=SURFACE2, fg=color, padx=18, pady=10)
        again_lbl.pack()
        for w in [again_outer, again_inner, again_lbl]:
            w.bind("<Button-1>", lambda e: (self.destroy(), on_again()))
            w.bind("<Enter>", lambda e: (again_inner.config(bg=SURFACE3), again_lbl.config(bg=SURFACE3)))
            w.bind("<Leave>", lambda e: (again_inner.config(bg=SURFACE2), again_lbl.config(bg=SURFACE2)))

        # MENU button
        menu_outer = tk.Frame(btn_row, bg=TEXT_MID, padx=1, pady=1)
        menu_outer.pack(side="left", padx=10)
        menu_inner = tk.Frame(menu_outer, bg=SURFACE2, cursor="hand2")
        menu_inner.pack(fill="both")
        menu_lbl = tk.Label(menu_inner, text="⌂  MAIN  MENU",
                            font=("Courier New",10,"bold"),
                            bg=SURFACE2, fg=TEXT_MID, padx=18, pady=10)
        menu_lbl.pack()
        for w in [menu_outer, menu_inner, menu_lbl]:
            w.bind("<Button-1>", lambda e: (self.destroy(), on_menu()))
            w.bind("<Enter>", lambda e: (menu_inner.config(bg=SURFACE3), menu_lbl.config(bg=SURFACE3)))
            w.bind("<Leave>", lambda e: (menu_inner.config(bg=SURFACE2), menu_lbl.config(bg=SURFACE2)))

        # Bottom corners
        bot_corners = tk.Frame(main, bg=BG)
        bot_corners.pack(fill="x", padx=10, pady=(0, 8))
        tk.Label(bot_corners, text="╚══", font=("Courier New",10), bg=BG, fg=color).pack(side="left")
        tk.Label(bot_corners, text="══╝", font=("Courier New",10), bg=BG, fg=color).pack(side="right")

    def _animate_in(self, step, total=12):
        if step > total: return
        t = ease_out(step / total)
        alpha = int(t * 255)
        # Pulse the result label size
        size = int(lerp(20, 36, t))
        try:
            self.result_lbl.config(font=("Courier New", size, "bold"))
        except:
            pass
        if step < total:
            self.after(20, lambda: self._animate_in(step+1, total))

# ══════════════════════════════════════════════════════════════════
#  GAME WINDOW
# ══════════════════════════════════════════════════════════════════
class GameWindow(Screen):
    CELL   = 132
    MARGIN = 20

    def __init__(self, mode="hvh", player_mark="X", difficulty="hard"):
        super().__init__(560, 760)
        self.mode       = mode
        self.p_mark     = player_mark
        self.bot_mark   = "O" if player_mark == "X" else "X"
        self.difficulty = difficulty
        self.board      = [""] * 9
        self.current    = "X"
        # Separate score tracking: X wins, O wins, draws + total games
        self.scores     = {"X": 0, "O": 0, "D": 0}
        self.total_games = 0
        self.game_over  = False
        self.btns       = []
        self.pulse_jobs = []
        self.hover_jobs = {}
        self.ai = AI(self.bot_mark, self.p_mark, difficulty) if mode == "hvb" else None
        self.title("TIC TAC TOE — NEON EDITION")
        self._build()

    def _build(self):
        # Top neon strip
        strip = tk.Canvas(self, height=4, bg=BG, highlightthickness=0)
        strip.pack(fill="x")
        strip.create_line(0, 2, 1200, 2, fill=X_COLOR, width=3)

        # Nav bar
        nav = tk.Frame(self, bg=BG)
        nav.pack(fill="x", padx=20, pady=(10, 0))
        back = tk.Label(nav, text="◀  MENU", font=FONT_LABEL,
                        bg=BG, fg=TEXT_LO, cursor="hand2")
        back.pack(side="left")
        back.bind("<Button-1>", lambda e: self._go_menu())
        back.bind("<Enter>",    lambda e: back.config(fg=TEXT_MID))
        back.bind("<Leave>",    lambda e: back.config(fg=TEXT_LO))

        ml = "PvP  ·  LOCAL" if self.mode == "hvh" else f"PvB  ·  {self.difficulty.upper()}"
        tk.Label(nav, text=ml, font=FONT_LABEL, bg=BG, fg=TEXT_LO).pack(side="right")

        # Score panel
        self._build_scores()

        # Match tracker
        self._build_match_tracker()

        # Status
        self.status_var = tk.StringVar()
        self.status_lbl = tk.Label(self, textvariable=self.status_var,
                                   font=("Courier New", 13, "bold"),
                                   bg=BG, fg=TEXT_MID, pady=8)
        self.status_lbl.pack()
        self._set_status()

        # Game board canvas
        cs = self.CELL * 3 + self.MARGIN * 2
        self.canvas = tk.Canvas(self, width=cs, height=cs,
                                bg=BG, highlightthickness=0)
        self.canvas.pack()
        self._draw_grid()
        self._draw_cells()

        # Bottom bar
        self._build_bottom_bar()

        # Bottom neon strip
        bot_strip = tk.Canvas(self, height=4, bg=BG, highlightthickness=0)
        bot_strip.pack(fill="x", side="bottom")
        bot_strip.create_line(0, 2, 1200, 2, fill=O_COLOR, width=3)

        if self.mode == "hvb" and self.bot_mark == "X":
            self.after(600, self._bot_move)

    def _build_scores(self):
        sf = tk.Frame(self, bg=SURFACE, relief="flat")
        sf.pack(padx=30, pady=(14, 0), fill="x")

        # Top accent line
        tk.Frame(sf, height=2, bg=BORDER2).pack(fill="x")

        inner = tk.Frame(sf, bg=SURFACE)
        inner.pack(fill="x")

        self.score_vars  = {}
        self.name_labels = {}

        if self.mode == "hvh":
            cols = [
                ("X", X_COLOR, "PLAYER 1", "X"),
                ("D", TEXT_MID, "DRAWS",    "·"),
                ("O", O_COLOR,  "PLAYER 2", "O"),
            ]
        else:
            you  = "YOU"  if self.p_mark == "X" else "BOT"
            them = "BOT"  if self.p_mark == "X" else "YOU"
            x_name = you  if self.p_mark == "X" else them
            o_name = them if self.p_mark == "X" else you
            cols = [
                ("X", X_COLOR, x_name, "X"),
                ("D", TEXT_MID, "DRAWS", "·"),
                ("O", O_COLOR, o_name, "O"),
            ]

        for key, color, name, mark in cols:
            cell = tk.Frame(inner, bg=SURFACE)
            cell.pack(side="left", expand=True, fill="x")

            # Vertical divider (except first)
            if key != "X":
                tk.Frame(inner, width=1, bg=BORDER2).pack(side="left", fill="y")
                cell = tk.Frame(inner, bg=SURFACE)
                cell.pack(side="left", expand=True, fill="x")

            name_lbl = tk.Label(cell, text=name, font=FONT_LABEL,
                                bg=SURFACE, fg=TEXT_MID)
            name_lbl.pack(pady=(8, 0))
            self.name_labels[key] = name_lbl

            var = tk.StringVar(value="0")
            self.score_vars[key] = var
            tk.Label(cell, textvariable=var, font=("Courier New", 28, "bold"),
                     bg=SURFACE, fg=color).pack(pady=(2, 6))

            if mark in ("X", "O"):
                tk.Label(cell, text=f"[ {mark} ]", font=FONT_LABEL,
                         bg=SURFACE, fg=color).pack(pady=(0, 8))
            else:
                tk.Label(cell, text="[ — ]", font=FONT_LABEL,
                         bg=SURFACE, fg=TEXT_LO).pack(pady=(0, 8))

        tk.Frame(sf, height=2, bg=BORDER2).pack(fill="x")

    def _build_match_tracker(self):
        self.tracker_frame = tk.Frame(self, bg=BG)
        self.tracker_frame.pack(pady=(6, 0))
        self.tracker_var = tk.StringVar(value="")
        self.tracker_lbl = tk.Label(self.tracker_frame, textvariable=self.tracker_var,
                                    font=FONT_LABEL, bg=BG, fg=TEXT_LO)
        self.tracker_lbl.pack()

    def _update_tracker(self):
        if self.total_games == 0:
            self.tracker_var.set("")
            return
        x_w = self.scores["X"]
        o_w = self.scores["O"]
        d   = self.scores["D"]

        if self.mode == "hvh":
            lead = "P1 LEADS" if x_w > o_w else ("P2 LEADS" if o_w > x_w else "TIED")
        else:
            you_mark, bot_mark = self.p_mark, self.bot_mark
            y_w = self.scores[you_mark]
            b_w = self.scores[bot_mark]
            lead = "YOU LEAD" if y_w > b_w else ("BOT LEADS" if b_w > y_w else "TIED")

        self.tracker_var.set(
            f"GAMES: {self.total_games}  ·  X:{x_w}  O:{o_w}  D:{d}  ·  {lead}"
        )

    def _build_bottom_bar(self):
        bar = tk.Frame(self, bg=SURFACE)
        bar.pack(fill="x", padx=30, pady=(14, 0))
        tk.Frame(bar, height=1, bg=BORDER2).pack(fill="x")

        row = tk.Frame(bar, bg=SURFACE)
        row.pack(fill="x", pady=8)

        new_btn = tk.Label(row, text="▶  NEW GAME", font=FONT_HEAD2,
                           bg=SURFACE, fg=X_COLOR, cursor="hand2", padx=20)
        new_btn.pack(side="left")
        new_btn.bind("<Button-1>", lambda e: self._reset())
        new_btn.bind("<Enter>",    lambda e: new_btn.config(fg=WIN_COLOR))
        new_btn.bind("<Leave>",    lambda e: new_btn.config(fg=X_COLOR))

        # Separator
        tk.Label(row, text="|", font=FONT_HEAD2, bg=SURFACE, fg=TEXT_LO).pack(side="left")

        menu_btn = tk.Label(row, text="⌂  MAIN MENU", font=FONT_HEAD2,
                            bg=SURFACE, fg=TEXT_MID, cursor="hand2", padx=20)
        menu_btn.pack(side="left")
        menu_btn.bind("<Button-1>", lambda e: self._go_menu())
        menu_btn.bind("<Enter>",    lambda e: menu_btn.config(fg=TEXT_HI))
        menu_btn.bind("<Leave>",    lambda e: menu_btn.config(fg=TEXT_MID))

        # Turn indicator dot on right
        self.turn_dot = tk.Label(row, text="●", font=("Courier New", 16),
                                 bg=SURFACE, fg=X_COLOR, padx=20)
        self.turn_dot.pack(side="right")

        tk.Frame(bar, height=1, bg=BORDER2).pack(fill="x")

    def _draw_grid(self):
        self.canvas.delete("grid")
        M, C = self.MARGIN, self.CELL
        total = C * 3 + M * 2

        # Background fill with subtle gradient effect
        self.canvas.create_rectangle(0, 0, total, total, fill=BG, outline="")

        # 3D cell backgrounds
        for i in range(9):
            r, c = divmod(i, 3)
            x0 = M + c*C + 5
            y0 = M + r*C + 5
            x1 = x0 + C - 10
            y1 = y0 + C - 10
            # Shadow (bottom-right)
            self.canvas.create_rectangle(x0+3, y0+3, x1+3, y1+3,
                fill="#000000", outline="", tags="grid")
            # Main cell
            self.canvas.create_rectangle(x0, y0, x1, y1,
                fill=SURFACE, outline=BORDER2, width=1, tags="grid")
            # Highlight (top-left edge for 3D)
            self.canvas.create_line(x0, y1, x0, y0, fill=BORDER2, width=1, tags="grid")
            self.canvas.create_line(x0, y0, x1, y0, fill=BORDER2, width=1, tags="grid")

        # Grid lines — neon glow
        for i in [1, 2]:
            x = M + i*C
            y = M + i*C
            # Glow effect: multiple lines with decreasing opacity
            for offset, opacity in [(2, "#0a0a20"), (1, "#151530"), (0, BORDER2)]:
                self.canvas.create_line(x-offset, M, x-offset, total-M,
                    fill=opacity, width=1, tags="grid")
                self.canvas.create_line(x+offset, M, x+offset, total-M,
                    fill=opacity, width=1, tags="grid")
                self.canvas.create_line(M, y-offset, total-M, y-offset,
                    fill=opacity, width=1, tags="grid")
                self.canvas.create_line(M, y+offset, total-M, y+offset,
                    fill=opacity, width=1, tags="grid")
            self.canvas.create_line(x, M, x, total-M,
                fill="#2a2a55", width=2, tags="grid")
            self.canvas.create_line(M, y, total-M, y,
                fill="#2a2a55", width=2, tags="grid")

    def _draw_cells(self):
        self.btns = []
        M, C = self.MARGIN, self.CELL
        for idx in range(9):
            r, c = divmod(idx, 3)
            x0 = M + c*C + 5
            y0 = M + r*C + 5
            x1 = x0 + C - 10
            y1 = y0 + C - 10

            rect = self.canvas.create_rectangle(x0, y0, x1, y1,
                fill="", outline="", tags=f"r{idx}")
            text = self.canvas.create_text((x0+x1)/2, (y0+y1)/2,
                text="", font=FONT_MARK, fill=TEXT_HI, tags=f"t{idx}")
            # Glow text (slightly offset, same color but dimmer)
            glow = self.canvas.create_text((x0+x1)/2+1, (y0+y1)/2+1,
                text="", font=FONT_MARK, fill="", tags=f"g{idx}")

            self.canvas.tag_bind(f"r{idx}", "<Button-1>", lambda e, i=idx: self._click(i))
            self.canvas.tag_bind(f"t{idx}", "<Button-1>", lambda e, i=idx: self._click(i))
            self.canvas.tag_bind(f"r{idx}", "<Enter>",    lambda e, i=idx: self._hover(i, True))
            self.canvas.tag_bind(f"r{idx}", "<Leave>",    lambda e, i=idx: self._hover(i, False))
            self.btns.append((rect, text, x0, y0, x1, y1, glow))

    def _cell_center(self, idx):
        _, _, x0, y0, x1, y1, _ = self.btns[idx]
        return (x0+x1)/2, (y0+y1)/2

    def _click(self, idx):
        if self.game_over or self.board[idx]: return
        if self.mode == "hvb" and self.current == self.bot_mark: return
        self._place(idx)

    def _hover(self, idx, on):
        if self.game_over or self.board[idx]: return
        rect = self.btns[idx][0]
        col  = mark_color(self.current)
        if on:
            # Subtle highlight with current player color
            self.canvas.itemconfig(rect, fill=SURFACE2, outline=col, width=1)
            # Preview ghost mark
            text = self.btns[idx][1]
            self.canvas.itemconfig(text, text=self.current,
                                   fill=mark_glow(self.current))
        else:
            self.canvas.itemconfig(rect, fill="", outline="", width=0)
            text = self.btns[idx][1]
            self.canvas.itemconfig(text, text="")

    def _place(self, idx):
        mark = self.current
        self.board[idx] = mark
        rect, text, x0, y0, x1, y1, glow = self.btns[idx]
        self.canvas.itemconfig(rect, fill="", outline="", width=0)
        self.canvas.itemconfig(text, text=mark, fill=mark_color(mark))
        self.canvas.itemconfig(glow, text=mark, fill=mark_glow(mark))
        self._anim_pop(idx, 0)

        winner = check_winner(self.board)
        if winner:
            self.after(200, lambda: self._end(winner))
        elif all(self.board):
            self.after(200, lambda: self._end(None))
        else:
            self.current = "O" if mark == "X" else "X"
            self._set_status()
            if self.mode == "hvb" and self.current == self.bot_mark:
                self.after(520, self._bot_move)

    def _bot_move(self):
        if self.game_over: return
        mv = self.ai.best_move(self.board)
        if mv is not None:
            self._place(mv)

    def _anim_pop(self, idx, step, total=10):
        text = self.btns[idx][1]
        glow = self.btns[idx][6]
        t    = ease_out(step / total)
        size = int(lerp(14, 46, t))
        try:
            f = tkfont.Font(family="Courier New", size=size, weight="bold")
            self.canvas.itemconfig(text, font=f)
            self.canvas.itemconfig(glow, font=f)
        except Exception:
            pass
        if step < total:
            self.after(16, lambda: self._anim_pop(idx, step+1, total))
        else:
            # Final font
            try:
                ff = tkfont.Font(family="Courier New", size=46, weight="bold")
                self.canvas.itemconfig(text, font=ff)
                self.canvas.itemconfig(glow, font=ff)
            except:
                pass

    def _anim_win(self, combo, step=0, total=20):
        a, _, c = combo
        ax, ay  = self._cell_center(a)
        cx, cy  = self._cell_center(c)
        t = ease_out(step / total)
        self.canvas.delete("winline")

        # Glow line (wider, dimmer)
        self.canvas.create_line(ax, ay,
            lerp(ax, cx, t), lerp(ay, cy, t),
            fill=WIN_GLOW, width=12, capstyle="round", tags="winline")
        # Main line
        self.canvas.create_line(ax, ay,
            lerp(ax, cx, t), lerp(ay, cy, t),
            fill=WIN_COLOR, width=4, capstyle="round", tags="winline")

        if step < total:
            self.after(14, lambda: self._anim_win(combo, step+1, total))
        else:
            for i in combo:
                self._pulse(i, 0)

    def _pulse(self, idx, step):
        text = self.btns[idx][1]
        t    = (1 + math.sin(step * 0.55)) / 2
        size = int(lerp(40, 52, t))
        try:
            f = tkfont.Font(family="Courier New", size=size, weight="bold")
            self.canvas.itemconfig(text, font=f)
        except Exception:
            pass
        job = self.after(50, lambda: self._pulse(idx, step+1))
        self.pulse_jobs.append(job)

    def _stop_pulses(self):
        for j in self.pulse_jobs:
            try: self.after_cancel(j)
            except Exception: pass
        self.pulse_jobs.clear()

    def _set_status(self):
        m = self.current
        if self.mode == "hvh":
            name = f"PLAYER  {m}  ─  YOUR  TURN"
        else:
            name = "YOUR  TURN" if m == self.p_mark else "BOT  IS  THINKING . . ."
        self.status_var.set(name)
        col = mark_color(m)
        if hasattr(self, "status_lbl"):
            self.status_lbl.config(fg=col)
        if hasattr(self, "turn_dot"):
            self.turn_dot.config(fg=col)

    def _end(self, winner):
        self.game_over = True
        self.total_games += 1

        if winner:
            self.scores[winner] += 1
            self.score_vars[winner].set(str(self.scores[winner]))
            if self.mode == "hvh":
                p = "PLAYER 1" if winner == "X" else "PLAYER 2"
                result_text = f"{p}  WINS!"
                sub_text    = f"Playing as  [{winner}]  ·  Congratulations!"
            else:
                if winner == self.p_mark:
                    result_text = "YOU  WIN!"
                    sub_text    = f"You played  [{winner}]  ·  Well played!"
                else:
                    result_text = "BOT  WINS!"
                    sub_text    = f"Bot played  [{winner}]  ·  Better luck next time!"
            color = mark_color(winner)
            status_msg = result_text
            self.status_lbl.config(fg=WIN_COLOR)

            combo = winning_combo(self.board)
            if combo:
                self.after(100, lambda: self._anim_win(combo))
        else:
            self.scores["D"] += 1
            self.score_vars["D"].set(str(self.scores["D"]))
            result_text = "DRAW!"
            sub_text    = "No winner this round."
            color       = DRAW_COLOR
            self.status_var.set("DRAW")
            self.status_lbl.config(fg=DRAW_COLOR)

        self._update_tracker()
        self.after(700, lambda: ResultOverlay(
            self, result_text, sub_text, color,
            self._reset, self._go_menu,
            self.scores, self.mode, self.p_mark
        ))

    def _reset(self):
        self._stop_pulses()
        self.board     = [""] * 9
        self.current   = "X"
        self.game_over = False
        self.canvas.delete("winline")

        self._draw_grid()
        for rect, text, x0, y0, x1, y1, glow in self.btns:
            self.canvas.itemconfig(rect, fill="", outline="", width=0)
            self.canvas.itemconfig(text, text="",
                                   font=tkfont.Font(family="Courier New", size=46, weight="bold"))
            self.canvas.itemconfig(glow, text="")
        self._draw_cells_reset()

        self._set_status()
        self._update_tracker()

        if self.mode == "hvb" and self.bot_mark == "X":
            self.after(600, self._bot_move)

    def _draw_cells_reset(self):
        # Re-bind events after reset
        for idx in range(9):
            r_tag = f"r{idx}"
            t_tag = f"t{idx}"
            self.canvas.tag_bind(r_tag, "<Button-1>", lambda e, i=idx: self._click(i))
            self.canvas.tag_bind(t_tag, "<Button-1>", lambda e, i=idx: self._click(i))
            self.canvas.tag_bind(r_tag, "<Enter>",    lambda e, i=idx: self._hover(i, True))
            self.canvas.tag_bind(r_tag, "<Leave>",    lambda e, i=idx: self._hover(i, False))

    def _go_menu(self):
        self._stop_pulses()
        self.destroy()
        MainMenu().mainloop()

# ══════════════════════════════════════════════════════════════════
#  ENTRY
# ══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    MainMenu().mainloop()