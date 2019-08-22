import tkinter as tk
from random import randint
from PIL import Image, ImageTk
import time

MOVE_INCREMENT = 20

class Snake(tk.Canvas):
    def __init__(self):
        super().__init__(
            width=600, height=620, background="black", highlightthickness=0
        )

        self.snake_positions = [(100, 100), (80, 100), (60, 100)]
        self.food_position = self.set_new_food_position()
        self.direction = "Right"

        self.score = 0

        self.loadAssets()
        self.createObjects()

        self.bind_all("<Key>", self.on_key_press)

        self.pack()

        self.after(50, self.perform_actions)

    def loadAssets(self):
        try:
            self.snake_body_image = Image.open("./assets/snake.png")
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)

            self.food_image = Image.open("./assets/food.png")
            self.food = ImageTk.PhotoImage(self.food_image)
        except IOError as error:
            print(error)
            root.destroy()

    def createObjects(self):
        self.create_text(30, 10, text=f"Score: {self.score}", tag="score", fill="#fff")

        for x_position, y_position in self.snake_positions:
            self.create_image(
                x_position, y_position, image=self.snake_body, tag="snake"
            )

        self.create_image(*self.food_position, image=self.food, tag="food")
    
    def check_collisions(self):
        head_x_position, head_y_position = self.snake_positions[0]

        if head_x_position in (0, 600) or head_y_position in (20, 620):
            return True
        elif (head_x_position, head_y_position) in self.snake_positions[1:]:
            return True
    
    def check_food_collision(self):
        if self.snake_positions[0] == self.food_position:
            self.score += 1
            self.snake_positions.append(self.snake_positions[-1])
            
            self.create_image(*self.snake_positions[-1], image=self.snake_body, tag="snake")
            self.food_position = self.set_new_food_position()
            self.coords(self.find_withtag("food"), *self.food_position)

            score = self.find_withtag("score")
            self.itemconfigure(score, text=f"Score: {self.score}", tag="score")

    def end_game(self):
        self.delete(tk.ALL)
        self.create_text(
            self.winfo_width() / 2,
            self.winfo_height() / 2,
            text=f"Game over! You scored {self.score}!",
            fill="#fff"
        )

    def move_snake(self):
        head_x_position, head_y_position = self.snake_positions[0]
        
        if self.direction == "Left":
            new_head_position = (head_x_position - MOVE_INCREMENT, head_y_position)
        elif self.direction == "Right":
            new_head_position = (head_x_position + MOVE_INCREMENT, head_y_position)
        elif self.direction == "Down":
            new_head_position = (head_x_position, head_y_position + MOVE_INCREMENT)
        elif self.direction == "Up":
            new_head_position = (head_x_position, head_y_position - MOVE_INCREMENT)

            
        self.snake_positions = [new_head_position] + self.snake_positions[:-1]

        for segment, position in zip(self.find_withtag("snake"), self.snake_positions):
            self.coords(segment, position)

    def on_key_press(self, e):
        if e.keysym in ("Up", "Down", "Left", "Right"):
            self.direction = e.keysym

    def perform_actions(self):
        if self.check_collisions():
            self.end_game()

        self.check_food_collision()
        self.move_snake()

        self.after(50, self.perform_actions)

    def set_new_food_position(self):
        while True:
            x_position = randint(1, 29) * MOVE_INCREMENT
            y_position = randint(3, 30) * MOVE_INCREMENT
            food_position = (x_position, y_position)

            if food_position not in self.snake_positions:
                return food_position


root = tk.Tk()
root.title("Snake")

board = Snake()

root.mainloop()
