import pygame
import pygame_gui
import sys

pygame.init()

WIDTH, HEIGHT = 1600, 900
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

maneger = pygame_gui.UIManager((WIDTH, HEIGHT))

text_imput = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 275), (900,50)), manager=maneger, object_id='#main_text_entry')

clock = pygame.time.Clock()
run = True

while run:
    time_delta = clock.tick(60)/1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                print(f"Text entered: {event.text}")

        maneger.process_events(event)
    
    maneger.update(time_delta)

    SCREEN.fill((30, 30, 30))
    maneger.draw_ui(SCREEN)

    pygame.display.flip()

pygame.quit()
sys.exit()