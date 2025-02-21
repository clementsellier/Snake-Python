import pygame
import sys
import random


class Block:
    def __init__(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos


class Food:
    def __init__(self):

        x = random.randint(0, NB_COL - 1)
        y = random.randint(0, NB_ROW - 1)
        self.block = Block(x, y)
    def draw_food(self):
        rect = pygame.Rect(self.block.x * CELL_SIZE, self.block.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, pygame.Color("orange"), rect)


class Snake:
    def __init__(self):
        self.body = [Block(2, 6), Block(3, 6), Block(4, 6)]
        self.direction = "RIGHT"

    def draw_snake(self):
        for block in self.body:
            x_coord = block.x * CELL_SIZE
            y_coord = block.y * CELL_SIZE
            block_rect = pygame.Rect(x_coord, y_coord, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, pygame.Color("green"), block_rect)

    def move_snake(self):
        self_block_count = len(self.body)
        old_head = self.body[self_block_count - 1]

        if self.direction == "RIGHT":
            new_head = Block(old_head.x + 1, old_head.y)

        elif self.direction == "LEFT":
            new_head = Block(old_head.x - 1, old_head.y)

        elif self.direction == "TOP":
            new_head = Block(old_head.x, old_head.y - 1)

        else:
            new_head = Block(old_head.x, old_head.y + 1)

        self.body.append(new_head)


class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.generate_food()
        self.score = 0

    def update(self):
        font = pygame.font.SysFont("Calibri", 20, 1)
        score_text = font.render(f"score : {self.score}", True, (255, 0, 0))
        screen.blit(score_text, (20, 20))
        self.snake.move_snake()
        self.check_head_on_food()
        self.game_over()

    def draw_game_element(self):
        self.food.draw_food()
        self.snake.draw_snake()

    def check_head_on_food(self):
        snake_length = len(self.snake.body)
        snake_head_block = self.snake.body[snake_length - 1]
        food_block = self.food.block
        if snake_head_block.x == food_block.x and snake_head_block.y == food_block.y:
            self.generate_food()
        else:
            self.snake.body.pop(0)

    def generate_food(self):
        should_generate_food = True
        while should_generate_food:
            count = 0
            for block in self.snake.body:
                if (block.x == self.food.block.x) and (block.y == self.food.block.y):
                    count += 1
            if count == 0:
                should_generate_food = False
            else:
                self.food = Food()

    # def text(self, surface, text, size, x, y):
    #     font = pg.font.Font(self.font_name, size)
    #     text_surface = font.render(text, True, WHITE)
    #     text.rect = text_surface.get.rect()
    #     text.rect.midtop = (x, y)
    #     self.screen.blit(text_surface, text_rect)

    def game_over(self):
        snake_lenght = len(self.snake.body)
        snake_head = self.snake.body[snake_lenght - 1]
        if (snake_head.x not in range(0, NB_COL)) or (snake_head.y not in range(0, NB_ROW)):
            print("Game over")
            pygame.quit()
            sys.exit()
        for block in self.snake.body[0:snake_lenght - 1]:
            if block.x == snake_head.x and block.y == snake_head.y:
                print("GAME OVER")
                pygame.quit()
                sys.exit()
        self.score = 0




pygame.init()


NB_COL = 10
NB_ROW = 15
CELL_SIZE = 40

screen = pygame.display.set_mode(size=(NB_COL * CELL_SIZE, NB_ROW * CELL_SIZE))
timer = pygame.time.Clock()
game_on = True
game = Game()
red = pygame.Color(255, 0, 0)
white = pygame.Color(255, 255, 255)
game_window = pygame.display.set_mode(size=(NB_COL * CELL_SIZE, NB_ROW * CELL_SIZE))

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 250)


def show_grid():
    for i in range(0, NB_COL):
        for j in range(0, NB_ROW):
            rect = pygame.Rect(i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, pygame.Color("orange"), rect, width=1)


while game_on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
           game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if game.snake.direction != "DOWN":
                    game.snake.direction = "TOP"
            if event.key == pygame.K_DOWN:
                if game.snake.direction != "TOP":
                    game.snake.direction = "DOWN"
            if event.key == pygame.K_LEFT:
                if game.snake.direction != "RIGHT":
                    game.snake.direction = "LEFT"
            if event.key == pygame.K_RIGHT:
                if game.snake.direction != "LEFT":
                    game.snake.direction = "RIGHT"

    screen.fill(pygame.Color("black"))
    game.draw_game_element()
    pygame.display.update()
    timer.tick(60)