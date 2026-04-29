import pygame
import random
import sys

# 游戏窗口大小
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20

# 颜色定义
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# 初始化
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('贪吃蛇')
clock = pygame.time.Clock()

# 贪吃蛇初始状态
snake = [(100, 100), (80, 100), (60, 100)]
direction = 'RIGHT'
change_to = direction

# 食物
food = (random.randrange(1, WIDTH//BLOCK_SIZE) * BLOCK_SIZE,
        random.randrange(1, HEIGHT//BLOCK_SIZE) * BLOCK_SIZE)

score = 0

def show_score():
    font = pygame.font.SysFont('arial', 24)
    score_surf = font.render(f'分数: {score}', True, BLACK)
    screen.blit(score_surf, (10, 10))

def game_over():
    font = pygame.font.SysFont('arial', 48)
    go_surf = font.render('游戏结束', True, RED)
    screen.blit(go_surf, (WIDTH//2-100, HEIGHT//2-40))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

# 游戏主循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'

    direction = change_to
    x, y = snake[0]
    if direction == 'UP':
        y -= BLOCK_SIZE
    elif direction == 'DOWN':
        y += BLOCK_SIZE
    elif direction == 'LEFT':
        x -= BLOCK_SIZE
    elif direction == 'RIGHT':
        x += BLOCK_SIZE
    new_head = (x, y)

    # 撞墙或撞自己
    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or new_head in snake:
        game_over()

    snake.insert(0, new_head)
    if new_head == food:
        score += 1
        food = (random.randrange(1, WIDTH//BLOCK_SIZE) * BLOCK_SIZE,
                random.randrange(1, HEIGHT//BLOCK_SIZE) * BLOCK_SIZE)
    else:
        snake.pop()

    screen.fill(WHITE)
    for block in snake:
        pygame.draw.rect(screen, GREEN, (block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, RED, (food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))
    show_score()
    pygame.display.flip()
    clock.tick(12)
