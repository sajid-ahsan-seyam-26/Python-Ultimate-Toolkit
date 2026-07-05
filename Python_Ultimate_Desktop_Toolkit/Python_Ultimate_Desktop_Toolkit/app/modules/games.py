import random
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGridLayout, QTabWidget, QMessageBox
from app.widgets.section import make_title


class TicTacToe(QWidget):
    def __init__(self):
        super().__init__()
        self.turn = "X"
        self.buttons = []
        layout = QVBoxLayout(self)
        self.status = QLabel("Turn: X")
        layout.addWidget(self.status)
        grid = QGridLayout()
        for i in range(9):
            btn = QPushButton("")
            btn.setFixedSize(95, 95)
            btn.setStyleSheet("font-size: 28px; font-weight: 900;")
            btn.clicked.connect(lambda _, b=btn: self.move(b))
            self.buttons.append(btn)
            grid.addWidget(btn, i // 3, i % 3)
        layout.addLayout(grid)
        reset = QPushButton("Reset")
        reset.clicked.connect(self.reset)
        layout.addWidget(reset)

    def move(self, btn):
        if btn.text():
            return
        btn.setText(self.turn)
        winner = self.check_winner()
        if winner:
            QMessageBox.information(self, "Game Over", f"{winner} wins!")
            self.reset()
            return
        if all(b.text() for b in self.buttons):
            QMessageBox.information(self, "Game Over", "Draw!")
            self.reset()
            return
        self.turn = "O" if self.turn == "X" else "X"
        self.status.setText(f"Turn: {self.turn}")

    def check_winner(self):
        wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for a,b,c in wins:
            if self.buttons[a].text() and self.buttons[a].text() == self.buttons[b].text() == self.buttons[c].text():
                return self.buttons[a].text()
        return None

    def reset(self):
        for b in self.buttons:
            b.setText("")
        self.turn = "X"
        self.status.setText("Turn: X")


class Game2048(QWidget):
    def __init__(self):
        super().__init__()
        self.grid_values = [[0]*4 for _ in range(4)]
        self.labels = []
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Use keyboard arrow keys to play 2048."))
        grid = QGridLayout()
        for r in range(4):
            row = []
            for c in range(4):
                label = QLabel("0")
                label.setAlignment(Qt.AlignCenter)
                label.setFixedSize(90, 90)
                label.setStyleSheet("border: 1px solid #64748b; border-radius: 8px; font-size: 22px; font-weight: 800;")
                row.append(label)
                grid.addWidget(label, r, c)
            self.labels.append(row)
        layout.addLayout(grid)
        reset = QPushButton("New Game")
        reset.clicked.connect(self.reset)
        layout.addWidget(reset)
        self.reset()

    def reset(self):
        self.grid_values = [[0]*4 for _ in range(4)]
        self.add_tile(); self.add_tile(); self.refresh()

    def add_tile(self):
        empty = [(r,c) for r in range(4) for c in range(4) if self.grid_values[r][c] == 0]
        if empty:
            r, c = random.choice(empty)
            self.grid_values[r][c] = 4 if random.random() < 0.1 else 2

    def compress(self, row):
        nums = [x for x in row if x]
        out = []
        skip = False
        for i, value in enumerate(nums):
            if skip:
                skip = False
                continue
            if i + 1 < len(nums) and nums[i+1] == value:
                out.append(value * 2)
                skip = True
            else:
                out.append(value)
        return out + [0]*(4-len(out))

    def move_left(self):
        old = [row[:] for row in self.grid_values]
        self.grid_values = [self.compress(row) for row in self.grid_values]
        return old != self.grid_values

    def move_right(self):
        old = [row[:] for row in self.grid_values]
        self.grid_values = [list(reversed(self.compress(list(reversed(row))))) for row in self.grid_values]
        return old != self.grid_values

    def transpose(self):
        self.grid_values = [list(row) for row in zip(*self.grid_values)]

    def move_up(self):
        old = [row[:] for row in self.grid_values]
        self.transpose(); self.grid_values = [self.compress(row) for row in self.grid_values]; self.transpose()
        return old != self.grid_values

    def move_down(self):
        old = [row[:] for row in self.grid_values]
        self.transpose(); self.grid_values = [list(reversed(self.compress(list(reversed(row))))) for row in self.grid_values]; self.transpose()
        return old != self.grid_values

    def keyPressEvent(self, event):
        moved = False
        if event.key() == Qt.Key_Left: moved = self.move_left()
        elif event.key() == Qt.Key_Right: moved = self.move_right()
        elif event.key() == Qt.Key_Up: moved = self.move_up()
        elif event.key() == Qt.Key_Down: moved = self.move_down()
        if moved:
            self.add_tile(); self.refresh()

    def refresh(self):
        for r in range(4):
            for c in range(4):
                value = self.grid_values[r][c]
                self.labels[r][c].setText(str(value) if value else "")


class MemoryGame(QWidget):
    def __init__(self):
        super().__init__()
        self.symbols = list("AABBCCDDEEFFGGHH")
        self.first = None
        self.buttons = []
        layout = QVBoxLayout(self)
        grid = QGridLayout()
        for i in range(16):
            btn = QPushButton("?")
            btn.setFixedSize(75, 75)
            btn.clicked.connect(lambda _, idx=i: self.flip(idx))
            self.buttons.append(btn)
            grid.addWidget(btn, i // 4, i % 4)
        layout.addLayout(grid)
        reset = QPushButton("Reset")
        reset.clicked.connect(self.reset)
        layout.addWidget(reset)
        self.reset()

    def reset(self):
        random.shuffle(self.symbols)
        self.first = None
        for b in self.buttons:
            b.setText("?")
            b.setEnabled(True)

    def flip(self, idx):
        btn = self.buttons[idx]
        if btn.text() != "?":
            return
        btn.setText(self.symbols[idx])
        if self.first is None:
            self.first = idx
            return
        if self.symbols[self.first] == self.symbols[idx]:
            self.buttons[self.first].setEnabled(False)
            btn.setEnabled(False)
        else:
            self.buttons[self.first].setText("?")
            btn.setText("?")
        self.first = None


class PlaceholderGame(QWidget):
    def __init__(self, name):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel(f"{name} module is ready as a placeholder. You can extend it from this tab.")
        label.setWordWrap(True)
        layout.addWidget(label)
        layout.addStretch()


class GamesPage(QWidget):
    def __init__(self, logger=None):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.addWidget(make_title("Mini Game Center", "Working mini games plus extension tabs."))
        tabs = QTabWidget()
        tabs.addTab(TicTacToe(), "Tic Tac Toe")
        tabs.addTab(Game2048(), "2048")
        tabs.addTab(MemoryGame(), "Memory")
        tabs.addTab(PlaceholderGame("Snake"), "Snake")
        tabs.addTab(PlaceholderGame("Sudoku"), "Sudoku")
        tabs.addTab(PlaceholderGame("Chess vs AI"), "Chess")
        tabs.addTab(PlaceholderGame("Flappy Bird"), "Flappy Bird")
        layout.addWidget(tabs)
