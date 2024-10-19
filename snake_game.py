
import torch
import tkinter as tk
import random

WIDTH = 500
HEIGHT = 500
GRID_SIZE = 25
INITIAL_LENGTH = 3
SNAKE_COLOR = "green"
SNAKE_HEAD_COLOR = "spring green"
FOOD_COLOR = "red"
BACKGROUND_COLOR = "black"
DELAY = 100

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg=BACKGROUND_COLOR)
        self.canvas.pack()

        # 초기 설정
        self.direction = "Right"
        self.snake = [(100, 100)]  # 뱀의 초기 위치
        for _ in range(1, INITIAL_LENGTH):
            self.snake.append((self.snake[-1][0] - GRID_SIZE, self.snake[-1][1]))

        self.food = self.place_food()
        self.score = 0
        self.reward = 0
        self.game_over = False

        # 키보드 입력
        #self.root.bind("<KeyPress>", self.change_direction)

        # 게임 시작
        self.update()

    def place_food(self):

        #x = random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE
        #y = random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE

        grid_x = [x for x in range(0, WIDTH, GRID_SIZE)]
        grid_y = [y for y in range(0, HEIGHT, GRID_SIZE)]

        grid = []
        for x, y in zip(grid_x, grid_y):
            if (x, y) not in self.snake:
                grid.append((x, y))

        locate = random.choice(grid)

        return locate

    def change_direction(self, event):
        if event in ["Up", "Down", "Left", "Right"]:
            if (event == "Up" and self.direction != "Down") or \
               (event == "Down" and self.direction != "Up") or \
               (event == "Left" and self.direction != "Right") or \
               (event == "Right" and self.direction != "Left"):
                self.direction = event
                #print(self.direction)
    def move_snake(self):
        head_x, head_y = self.snake[0]
        self.reward = self.reward + 1

        if self.direction == "Up":
            new_head = (head_x, head_y - GRID_SIZE)
        elif self.direction == "Down":
            new_head = (head_x, head_y + GRID_SIZE)
        elif self.direction == "Left":
            new_head = (head_x - GRID_SIZE, head_y)
        elif self.direction == "Right":
            new_head = (head_x + GRID_SIZE, head_y)

        # 벽에 충돌하거나 자기 자신과 충돌하면 게임 오버
        if (new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT or
            new_head in self.snake):
            self.reward = self.reward - 100
            self.game_over = True

            return self.score

        # 뱀이 먹이를 먹으면 길이 증가
        self.snake = [new_head] + self.snake
        if new_head == self.food:
            self.food = self.place_food()  # 새로운 먹이 배치
            self.score += 1
            self.reward += 100
            #print(self.score)
        else:
            self.snake.pop()  # 꼬리를 제거해 이동 구현

        #self.board = self.board_tensor()

    def draw(self):
        self.canvas.delete(tk.ALL)  # 화면을 지우고 새로 그리기

        # 점수 표시
        self.canvas.create_text(WIDTH // 2, 10, text=f"Score: {self.score}",
                                fill="white", font=("Arial", 12))

        # 뱀 그리기
        for i, segment in enumerate(self.snake):
            if i == 0:
                self.canvas.create_rectangle(segment[0], segment[1],
                                             segment[0] + GRID_SIZE, segment[1] + GRID_SIZE,
                                             fill=SNAKE_HEAD_COLOR)
            else:
                self.canvas.create_rectangle(segment[0], segment[1],
                                             segment[0] + GRID_SIZE, segment[1] + GRID_SIZE,
                                             fill=SNAKE_COLOR)

        # 먹이 그리기
        self.canvas.create_rectangle(self.food[0], self.food[1],
                                     self.food[0] + GRID_SIZE, self.food[1] + GRID_SIZE,
                                     fill=FOOD_COLOR)

    def board_tensor(self):
        board = torch.zeros(3, WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE)

        for segment in self.snake:
            board[0, segment[1] // GRID_SIZE, segment[0] // GRID_SIZE] = 1  # 뱀의 몸통

        board[1, self.food[1] // GRID_SIZE, self.food[0] // GRID_SIZE] = 5  # 먹이 위치

        # 뱀의 머리
        for W in range(WIDTH // GRID_SIZE):
            board[2, 0, W] = 1
            board[2, HEIGHT // GRID_SIZE - 1, W] = 1

        for H in range(HEIGHT // GRID_SIZE):
            board[2, H, 0] = 1
            board[2, H, HEIGHT // GRID_SIZE - 1] = 1

        return board

    def update(self):
        if not self.game_over:
            self.move_snake()
            self.draw()
            self.root.after(DELAY, self.update)
        else:
            self.canvas.create_text(WIDTH // 2, HEIGHT // 2,
                                    text=f"Game Over! Final Score: {self.score}",
                                    fill="white", font=("Arial", 24))

