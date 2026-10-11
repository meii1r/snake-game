import random
import tkinter as tk

CELL = 20     # размер клетки в пикселях
COLS = 15     # ширина поля в клетках
ROWS = 15     # высота поля в клетках
SPEED = 150   # пауза между шагами (мс), меньше = быстрее
RECORD_FILE = "record.txt"


def load_record():
    try:
        with open(RECORD_FILE) as f:
            return int(f.read().strip())
    except (OSError, ValueError):
        return 0


def save_record(value):
    try:
        with open(RECORD_FILE, "w") as f:
            f.write(str(value))
    except OSError:
        pass


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.job = None
        self.record = load_record()
        root.title("Змейка")

        self.score_label = tk.Label(root, font=("Arial", 16))
        self.score_label.pack(pady=5)

        self.canvas = tk.Canvas(root, width=COLS * CELL, height=ROWS * CELL, bg="black")
        self.canvas.pack()

        self.make_buttons()
        self.bind_keys()
        self.new_game()

    def make_buttons(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)
        tk.Button(frame, text="▲", width=4, height=2,
                  command=lambda: self.turn(0, -1)).grid(row=0, column=1)
        tk.Button(frame, text="◀", width=4, height=2,
                  command=lambda: self.turn(-1, 0)).grid(row=1, column=0)
        tk.Button(frame, text="▼", width=4, height=2,
                  command=lambda: self.turn(0, 1)).grid(row=1, column=1)
        tk.Button(frame, text="▶", width=4, height=2,
                  command=lambda: self.turn(1, 0)).grid(row=1, column=2)
        tk.Button(self.root, text="Заново", command=self.new_game).pack(pady=5)

    def bind_keys(self):
        keys = {
            "Up": (0, -1), "w": (0, -1),
            "Down": (0, 1), "s": (0, 1),
            "Left": (-1, 0), "a": (-1, 0),
            "Right": (1, 0), "d": (1, 0),
        }
        for key, (dx, dy) in keys.items():
            self.root.bind(f"<{key}>", lambda e, dx=dx, dy=dy: self.turn(dx, dy))

    def update_score(self):
        self.score_label.config(text=f"Счёт: {self.score}   Рекорд: {self.record}")

    def new_game(self):
        if self.job is not None:
            self.root.after_cancel(self.job)
        self.snake = [(7, 7), (6, 7), (5, 7)]  # первая клетка - голова
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.score = 0
        self.update_score()
        self.place_food()
        self.step()

    def place_food(self):
        free = [(x, y) for x in range(COLS) for y in range(ROWS)
                if (x, y) not in self.snake]
        if not free:
            self.food = None
            return False
        self.food = random.choice(free)
        return True

    def turn(self, dx, dy):
        # нельзя развернуться на 180 градусов
        if (dx, dy) != (-self.direction[0], -self.direction[1]):
            self.next_direction = (dx, dy)

    def step(self):
        self.direction = self.next_direction
        x, y = self.snake[0]
        new_head = (x + self.direction[0], y + self.direction[1])

        # удар о стену или об себя
        if (new_head[0] < 0 or new_head[0] >= COLS
                or new_head[1] < 0 or new_head[1] >= ROWS
                or new_head in self.snake):
            self.draw()
            self.finish("Игра окончена")
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            if self.score > self.record:
                self.record = self.score
                save_record(self.record)
            self.update_score()
            if not self.place_food():
                self.draw()
                self.finish("Победа!")
                return
        else:
            self.snake.pop()  # не съела еду - хвост двигается

        self.draw()
        self.job = self.root.after(SPEED, self.step)

    def draw(self):
        self.canvas.delete("all")
        if self.food is not None:
            fx, fy = self.food
            self.canvas.create_oval(fx * CELL, fy * CELL,
                                    (fx + 1) * CELL, (fy + 1) * CELL, fill="red")
        for i, (x, y) in enumerate(self.snake):
            color = "lime" if i == 0 else "green"
            self.canvas.create_rectangle(x * CELL, y * CELL,
                                         (x + 1) * CELL, (y + 1) * CELL,
                                         fill=color, outline="black")

    def finish(self, text):
        self.job = None
        self.canvas.create_text(COLS * CELL // 2, ROWS * CELL // 2,
                                text=text, fill="white", font=("Arial", 22))


if __name__ == "__main__":
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()
