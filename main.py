import random
import sys

import pygame


WIDTH, HEIGHT = 640, 460
BLOCK_SIZE = 20
HEADER_HEIGHT = 60
PLAY_TOP = HEADER_HEIGHT
GRID_WIDTH = WIDTH
GRID_HEIGHT = HEIGHT - HEADER_HEIGHT
FPS = 12

BG = (13, 18, 32)
PANEL = (24, 32, 52)
GRID_LINE = (35, 45, 68)
TEXT = (232, 238, 252)
MUTED = (133, 146, 173)
SNAKE_HEAD = (95, 255, 184)
SNAKE_TAIL = (29, 185, 125)
SNAKE_SHADOW = (6, 10, 18)
FOOD = (255, 92, 115)
FOOD_HIGHLIGHT = (255, 182, 193)
ACCENT = (101, 210, 255)
DANGER = (255, 92, 115)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Snake")
clock = pygame.time.Clock()

title_font = pygame.font.SysFont("segoeui", 28, bold=True)
ui_font = pygame.font.SysFont("segoeui", 22, bold=True)
small_font = pygame.font.SysFont("segoeui", 16)
game_over_font = pygame.font.SysFont("segoeui", 46, bold=True)


def grid_random_position():
    return (
        random.randrange(0, GRID_WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
        random.randrange(PLAY_TOP // BLOCK_SIZE, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE,
    )


def spawn_food(snake):
    food = grid_random_position()
    while food in snake:
        food = grid_random_position()
    return food


snake = [(120, 120), (100, 120), (80, 120)]
direction = "RIGHT"
change_to = direction
food = spawn_food(snake)
score = 0


def lerp_color(start, end, amount):
    return tuple(int(start[i] + (end[i] - start[i]) * amount) for i in range(3))


def draw_background():
    screen.fill(BG)
    pygame.draw.rect(screen, PANEL, (0, 0, WIDTH, HEADER_HEIGHT))
    pygame.draw.line(screen, ACCENT, (0, HEADER_HEIGHT - 1), (WIDTH, HEADER_HEIGHT - 1), 2)

    for x in range(0, WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, GRID_LINE, (x, PLAY_TOP), (x, HEIGHT), 1)
    for y in range(PLAY_TOP, HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, GRID_LINE, (0, y), (WIDTH, y), 1)


def draw_ui():
    title = title_font.render("Neon Snake", True, TEXT)
    hint = small_font.render("Arrow keys to move", True, MUTED)
    score_label = ui_font.render(f"Score  {score}", True, TEXT)

    screen.blit(title, (18, 10))
    screen.blit(hint, (182, 24))

    score_rect = pygame.Rect(WIDTH - 148, 12, 128, 36)
    pygame.draw.rect(screen, (15, 23, 42), score_rect, border_radius=10)
    pygame.draw.rect(screen, (54, 72, 106), score_rect, 1, border_radius=10)
    screen.blit(score_label, score_label.get_rect(center=score_rect.center))


def draw_snake():
    for index, block in enumerate(reversed(snake)):
        real_index = len(snake) - 1 - index
        x, y = block
        amount = real_index / max(len(snake) - 1, 1)
        color = lerp_color(SNAKE_HEAD, SNAKE_TAIL, amount)
        inset = 2 if real_index == 0 else 3

        shadow_rect = pygame.Rect(x + 2, y + 3, BLOCK_SIZE - 2, BLOCK_SIZE - 2)
        body_rect = pygame.Rect(x + inset, y + inset, BLOCK_SIZE - inset * 2, BLOCK_SIZE - inset * 2)

        pygame.draw.rect(screen, SNAKE_SHADOW, shadow_rect, border_radius=7)
        pygame.draw.rect(screen, color, body_rect, border_radius=7)

        if real_index == 0:
            draw_snake_eyes(x, y)


def draw_snake_eyes(x, y):
    eye_color = (5, 18, 28)
    shine = (230, 255, 250)

    offsets = {
        "UP": [(6, 5), (14, 5)],
        "DOWN": [(6, 14), (14, 14)],
        "LEFT": [(5, 6), (5, 14)],
        "RIGHT": [(14, 6), (14, 14)],
    }[direction]

    for ox, oy in offsets:
        pygame.draw.circle(screen, eye_color, (x + ox, y + oy), 3)
        pygame.draw.circle(screen, shine, (x + ox - 1, y + oy - 1), 1)


def draw_food():
    x, y = food
    center = (x + BLOCK_SIZE // 2, y + BLOCK_SIZE // 2)
    pygame.draw.circle(screen, SNAKE_SHADOW, (center[0] + 2, center[1] + 3), 9)
    pygame.draw.circle(screen, FOOD, center, 9)
    pygame.draw.circle(screen, FOOD_HIGHLIGHT, (center[0] - 3, center[1] - 3), 3)
    pygame.draw.rect(screen, (81, 210, 133), (center[0] + 2, center[1] - 12, 7, 4), border_radius=3)


def show_game_over():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((5, 8, 14, 184))
    screen.blit(overlay, (0, 0))

    card = pygame.Rect(WIDTH // 2 - 170, HEIGHT // 2 - 92, 340, 184)
    pygame.draw.rect(screen, (22, 30, 49), card, border_radius=18)
    pygame.draw.rect(screen, DANGER, card, 2, border_radius=18)

    title = game_over_font.render("Game Over", True, TEXT)
    final_score = ui_font.render(f"Final Score  {score}", True, FOOD_HIGHLIGHT)
    prompt = small_font.render("Close the window to exit", True, MUTED)

    screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 42)))
    screen.blit(final_score, final_score.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 14)))
    screen.blit(prompt, prompt.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 54)))
    pygame.display.flip()
    pygame.time.wait(2200)
    pygame.quit()
    sys.exit()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                change_to = "UP"
            elif event.key == pygame.K_DOWN and direction != "UP":
                change_to = "DOWN"
            elif event.key == pygame.K_LEFT and direction != "RIGHT":
                change_to = "LEFT"
            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                change_to = "RIGHT"

    direction = change_to
    x, y = snake[0]

    if direction == "UP":
        y -= BLOCK_SIZE
    elif direction == "DOWN":
        y += BLOCK_SIZE
    elif direction == "LEFT":
        x -= BLOCK_SIZE
    elif direction == "RIGHT":
        x += BLOCK_SIZE

    new_head = (x, y)

    if x < 0 or x >= WIDTH or y < PLAY_TOP or y >= HEIGHT or new_head in snake:
        draw_background()
        draw_food()
        draw_snake()
        draw_ui()
        show_game_over()

    snake.insert(0, new_head)
    if new_head == food:
        score += 1
        food = spawn_food(snake)
    else:
        snake.pop()

    draw_background()
    draw_food()
    draw_snake()
    draw_ui()

    pygame.display.flip()
    clock.tick(FPS)
