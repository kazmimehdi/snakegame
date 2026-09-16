import random
import tkinter as tk


CELL_SIZE = 20
GRID_SIZE = 20
BOARD_SIZE = CELL_SIZE * GRID_SIZE
SPEED_MS = 120


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake")
        self.root.resizable(False, False)

        self.score_label = tk.Label(root, text="Score: 0", font=("Arial", 14))
        self.score_label.pack(pady=(8, 0))

        self.canvas = tk.Canvas(
            root,
            width=BOARD_SIZE,
            height=BOARD_SIZE,
            bg="#111827",
            highlightthickness=0,
        )
        self.canvas.pack(padx=8, pady=8)
        self.canvas.focus_set()
        self.canvas.bind("<KeyPress>", self.handle_key)

        self.reset()

    def reset(self):
        middle = GRID_SIZE // 2
        self.snake = [(middle, middle), (middle - 1, middle), (middle - 2, middle)]
        self.direction = (1, 0)
        self.next_direction = self.direction
        self.food = self.place_food()
        self.score = 0
        self.game_over = False
        self.score_label.config(text="Score: 0")
        self.draw()
        self.root.after(SPEED_MS, self.tick)

    def place_food(self):
        open_spaces = [
            (x, y)
            for x in range(GRID_SIZE)
            for y in range(GRID_SIZE)
            if (x, y) not in self.snake
        ]
        return random.choice(open_spaces)

    def handle_key(self, event):
        directions = {
            "Up": (0, -1),
            "Down": (0, 1),
            "Left": (-1, 0),
            "Right": (1, 0),
            "w": (0, -1),
            "s": (0, 1),
            "a": (-1, 0),
            "d": (1, 0),
        }

        if event.keysym.lower() == "r" and self.game_over:
            self.reset()
            return

        new_direction = directions.get(event.keysym)
        if new_direction and new_direction != (
            -self.direction[0],
            -self.direction[1],
        ):
            self.next_direction = new_direction

    def tick(self):
        if self.game_over:
            return

        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        delta_x, delta_y = self.direction
        new_head = (head_x + delta_x, head_y + delta_y)

        ate_food = new_head == self.food
        body_to_check = self.snake if ate_food else self.snake[:-1]
        hit_wall = not (
            0 <= new_head[0] < GRID_SIZE and 0 <= new_head[1] < GRID_SIZE
        )

        if hit_wall or new_head in body_to_check:
            self.game_over = True
            self.draw()
            return

        self.snake.insert(0, new_head)
        if ate_food:
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            self.food = self.place_food()
        else:
            self.snake.pop()

        self.draw()
        self.root.after(SPEED_MS, self.tick)

    def draw(self):
        self.canvas.delete("all")

        food_x, food_y = self.food
        self.canvas.create_oval(
            food_x * CELL_SIZE + 3,
            food_y * CELL_SIZE + 3,
            (food_x + 1) * CELL_SIZE - 3,
            (food_y + 1) * CELL_SIZE - 3,
            fill="#ef4444",
            outline="",
        )

        for index, (x, y) in enumerate(self.snake):
            color = "#22c55e" if index == 0 else "#16a34a"
            self.canvas.create_rectangle(
                x * CELL_SIZE + 1,
                y * CELL_SIZE + 1,
                (x + 1) * CELL_SIZE - 1,
                (y + 1) * CELL_SIZE - 1,
                fill=color,
                outline="",
            )

        if self.game_over:
            self.canvas.create_text(
                BOARD_SIZE // 2,
                BOARD_SIZE // 2 - 12,
                text="GAME OVER",
                fill="white",
                font=("Arial", 24, "bold"),
            )
            self.canvas.create_text(
                BOARD_SIZE // 2,
                BOARD_SIZE // 2 + 20,
                text="Press R to restart",
                fill="#d1d5db",
                font=("Arial", 12),
            )


if __name__ == "__main__":
    window = tk.Tk()
    SnakeGame(window)
    window.mainloop()
