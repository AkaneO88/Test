import pygame

pygame.init()

screen = pygame.display.set_mode((400,400))
running = True

sprites = pygame.image.load("Sprites.png")
k1 = sprites.subsurface((0,32,32,42))
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
    screen.blit(k1, (0,0))
    pygame.display.update()