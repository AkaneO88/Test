import pygame
import random
import sys

pygame.init()

WIDTH = 800
HEIGHT = 600
CELL_SIZE  = 20

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 000)
BLUE = (0, 0, 255)
BLACK = (0,0,0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake')

fps = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 25)

def draw_snake(snake_body):
    for segment in snake_body:
        pygame.draw.rect(screen, BLUE, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE))

def place_food():
    return[
        random.randrange(0,WIDTH, CELL_SIZE),
        random.randrange(0,HEIGHT, CELL_SIZE),
    ]

def game_over(score):
    message =font.render(f'Game Over! Your Score: {score}', True, RED)
    screen.blit(message,[WIDTH // 6, HEIGHT // 3])
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

def main():
    snake_pos =[50,50]
    snake_body = [[100, 50], [80,50], [60,50]]
    direction = 'RIGHT'
    change_to = direction
    food_pos=place_food()
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction !='DOWN':
                    change_to ='UP'
                elif event.key == pygame.K_DOWN and direction !='UP':
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    change_to = 'RIGHT'
        
        direction = change_to

        if direction == 'UP':
            snake_pos[1] -= CELL_SIZE
        if direction == 'DOWN':
            snake_pos[1] += CELL_SIZE
        if direction == 'LEFT':
            snake_pos[0] -= CELL_SIZE
        if direction == 'RIGHT':
            snake_pos[0] += CELL_SIZE

        snake_body.insert(0, list(snake_pos))

        snake_head_rect=pygame.Rect(snake_pos[0], snake_pos[1], CELL_SIZE, CELL_SIZE)
        food_rect =pygame.Rect(food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE)

        if snake_head_rect.colliderect(food_rect):
            score += 1
            food_pos = place_food()
        else:
            snake_body.pop()

        if snake_pos[0] < 0:
            snake_pos[0] = WIDTH - CELL_SIZE
        elif snake_pos[0] >= WIDTH:
            snake_pos[0] = 0
        if snake_pos[1] < 0:
            snake_pos[1] = HEIGHT - CELL_SIZE
        elif snake_pos[1] >= HEIGHT:
            snake_pos[1] =0

        if snake_pos in snake_body[1:]:
            game_over(score)

        screen.fill(BLACK)
        draw_snake(snake_body)
        pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE))
        pygame.display.update()

        score_text = font.render(f'{score}', True, WHITE)
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))
        
        pygame.display.flip()
        fps.tick(10 + score // 3)

if __name__ == '__main__':
    main()
    