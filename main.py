import pygame  # type: ignore
import random
import sys

pygame.init()

BLOCK_SIZE = 20
WIDTH, HEIGHT = 600, 400
FPS = 10

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Start Game')
clock = pygame.time.Clock()

def draw_block(color, pos):
    pygame.draw.rect(screen, color, pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))


def random_food():
    return [random.randrange(0, WIDTH, BLOCK_SIZE), random.randrange(0, HEIGHT, BLOCK_SIZE)]


def game_over_screen(score):
    font = pygame.font.SysFont(None, 48)
    msg = font.render(f'Game Over! Score: {score}', True, WHITE)
    restart_msg = pygame.font.SysFont(None, 32).render('Press R to Restart or Q to Quit', True, WHITE)

    while True:
        screen.fill(BLACK)
        screen.blit(msg, ((WIDTH - msg.get_width()) // 2, HEIGHT // 3))
        screen.blit(restart_msg, ((WIDTH - restart_msg.get_width()) // 2, HEIGHT // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    game_loop()

def game_loop():
    snake = [[100, 100], [80, 100], [60, 100]]
    direction = 'RIGHT'
    change_to = direction
    food = random_food()
    score = 0

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
        head = snake[0].copy()
        if direction == 'UP':
            head[1] -= BLOCK_SIZE
        elif direction == 'DOWN':
            head[1] += BLOCK_SIZE
        elif direction == 'LEFT':
            head[0] -= BLOCK_SIZE
        elif direction == 'RIGHT':
            head[0] += BLOCK_SIZE

        if (
            head in snake or
            head[0] < 0 or head[0] >= WIDTH or
            head[1] < 0 or head[1] >= HEIGHT
        ):
            break

        snake.insert(0, head)
        if head == food:
            score += 1
            food = random_food()
        else:
            snake.pop()

        screen.fill(BLACK)
        draw_block(RED, food)
        for block in snake:
            draw_block(GREEN, block)

        pygame.display.flip()
        clock.tick(FPS)

    game_over_screen(score)

game_loop()
