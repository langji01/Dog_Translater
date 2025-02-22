import pygame
import random
import sys
import os
from pygame import mixer

# 初始化Pygame
pygame.init()
mixer.init()

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 游戏设置
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
SNAKE_SPEED = 10

# 创建游戏窗口
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('贪吃蛇游戏')

# 加载音效
try:
    eat_sound = mixer.Sound('sounds/eat.wav')
    crash_sound = mixer.Sound('sounds/crash.wav')
except:
    print("警告：未能加载音效文件")

class Snake:
    def __init__(self):
        self.length = 6
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.score = 0
        self.speed = SNAKE_SPEED

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = ((cur[0] + x) % GRID_WIDTH, (cur[1] + y) % GRID_HEIGHT)
        if new in self.positions[3:]:
            return False
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def reset(self):
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        self.speed = SNAKE_SPEED

    def render(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color,
                           (p[0] * GRID_SIZE, p[1] * GRID_SIZE,
                            GRID_SIZE, GRID_SIZE))

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH-1),
                        random.randint(0, GRID_HEIGHT-1))

    def render(self, surface):
        pygame.draw.rect(surface, self.color,
                        (self.position[0] * GRID_SIZE,
                         self.position[1] * GRID_SIZE,
                         GRID_SIZE, GRID_SIZE))

# 方向常量
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def draw_grid(surface):
    for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            r = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, (40, 40, 40), r, 1)

def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    snake = Snake()
    food = Food()

    font = pygame.font.Font(None, 36)
    score_font = pygame.font.Font(None, 28)

    game_over = False
    paused = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    if game_over:
                        snake.reset()
                        food.randomize_position()
                        game_over = False
                    else:
                        paused = not paused
                elif not game_over and not paused:
                    if event.key == pygame.K_UP and snake.direction != DOWN:
                        snake.direction = UP
                    elif event.key == pygame.K_DOWN and snake.direction != UP:
                        snake.direction = DOWN
                    elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                        snake.direction = LEFT
                    elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                        snake.direction = RIGHT

        surface.fill(BLACK)
        draw_grid(surface)

        if not game_over and not paused:
            if not snake.update():
                game_over = True
                try:
                    crash_sound.play()
                except:
                    pass

            # 检查是否吃到食物
            if snake.get_head_position() == food.position:
                snake.length += 1
                snake.score += 10
                try:
                    eat_sound.play()
                except:
                    pass
                food.randomize_position()
                # 每得100分增加速度
                if snake.score % 100 == 0:
                    snake.speed += 2

        snake.render(surface)
        food.render(surface)

        screen.blit(surface, (0, 0))

        # 显示分数
        score_text = score_font.render(f'分数: {snake.score}', True, WHITE)
        screen.blit(score_text, (5, 5))

        # 显示速度等级
        level = (snake.speed - SNAKE_SPEED) // 2 + 1
        level_text = score_font.render(f'等级: {level}', True, WHITE)
        screen.blit(level_text, (5, 25))

        if game_over:
            game_over_text = font.render('游戏结束! 按空格键重新开始', True, WHITE)
            screen.blit(game_over_text, (WINDOW_WIDTH//2 - 200, WINDOW_HEIGHT//2))
        elif paused:
            pause_text = font.render('游戏暂停! 按空格键继续', True, WHITE)
            screen.blit(pause_text, (WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT//2))

        pygame.display.update()
        clock.tick(snake.speed)

if __name__ == '__main__':
    main() 