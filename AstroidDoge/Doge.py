import pygame
import sys
import random
import math
import json
import os
import pygame_gui

FILENAME = 'data.json'

import pygame.locals

pygame.init()
# pygame.font.init()

Width = 500
Height = 500
Frames = 60

Ast_spd = 1
score = 0
level = 1
level_cap = 1000
maneger = pygame_gui.UIManager((Width, Height))

screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption('Astroid Avoider')
clock = pygame.time.Clock()
start_img = pygame.image.load('backround/start.png')

bg_img = pygame.image.load('Backround.png')
bg_imgs= []
for num in range(1,9):
    img = pygame.image.load(f"backround/animation-frame ({num}).png")
    img = pygame.transform.scale_by(img,5)
    bg_imgs.append(img)

ship_img= pygame.image.load('Spaceship.png')
astroid_img = [pygame.image.load('slow.png'),
               pygame.image.load('Normal.png'),
               pygame.image.load('Fast.png')
               ]

def load_image(path):
    try:
        return pygame.image.load(path).convert_alpha()
    except pygame.error as e:
        print(f"Error loading image: {path}")
        raise SystemExit(e)
    
def get_username():
    screen2 = pygame.display.set_mode((Width, Height))
    pygame.display.set_caption("Enter Username! You're on the leaderbord!!")

    white = (255,255, 255)
    black = (0,0,0)
    gray = (200, 200, 200)
    blue = (100, 149, 237)
    dark_blue = (65, 105, 225)
    afont = pygame.font.SysFont('arial', 25)


    input_box = pygame.Rect(50, 80, 300, 40)
    username = "" 
    active = True

    button_rect = pygame.Rect(150, 140, 100, 40)
    button_hover = False

    running2 = True 
    while running2:
        screen2.fill(white)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if username.strip():
                        return username.strip()
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    if len(username)<20:
                        username += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    if username.strip():
                        return username.strip()
                    
        mouse_pos = pygame.mouse.get_pos()
        button_hover = button_rect.collidepoint(mouse_pos)

        title_surface = afont.render("Enter Username", True, black)
        title_rect = title_surface.get_rect(center=(200,30))
        screen2.blit(title_surface, title_rect)

        pygame.draw.rect(screen2, gray if not active else blue, input_box, 2)
        text_surface = afont.render(username, True, black)
        screen2.blit(text_surface, (input_box.x+5, input_box.y+8))

        if active and pygame.time.get_ticks() % 1000 < 500:
            cursor_x = input_box.x+5 + text_surface.get_width()
            pygame.draw.line(screen2, black,
                             (cursor_x, input_box.y+5),
                             (cursor_x, input_box.y+35), 2)
            
        button_color = dark_blue if button_hover else blue
        pygame.draw.rect(screen2, button_color, button_rect)
        pygame.draw.rect(screen2, black, button_rect, 2)
        button_text = afont.render("Submit", True, white)
        button_text_rect = button_text.get_rect(center = button_rect.center)
        screen2.blit(button_text, button_text_rect)

        pygame.display.flip()
        clock.tick(60)



def main_menu():
    start_button = pygame.transform.scale(load_image('backround/start_default.png'),(150,60))
    start_hover = pygame.transform.scale(load_image('backround/start_press.png'),(150,60))
    quit_button = pygame.transform.scale(load_image('backround/quit.png'),(150,60))
    quit_hover = pygame.transform.scale(load_image('backround/quit_press.png'),(150,60))
    start_backround = pygame.transform.scale(load_image('backround/start.png'),(Width,Height))

    rects = [
        start_button.get_rect(center=(Width//2, Height//2+50)), 
        quit_button.get_rect(center=(Width//2, Height//2+150))
    ]
    while True:
        screen.blit(start_backround,(0,0))

        mouse_pos = pygame.mouse.get_pos()

        if rects[0].collidepoint(mouse_pos):
            screen.blit(start_hover, rects[0])
        else : 
            screen.blit(start_button, rects[0])

        if rects[1].collidepoint(mouse_pos):
            screen.blit(quit_hover, rects[1])
        else : 
            screen.blit(quit_button, rects[1])
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if rects[0].collidepoint(mouse_pos):
                    main()
                elif rects[1].collidepoint(mouse_pos):
                 pygame.quit(); sys.exit()
                    
def load_leaderboard():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as file:
            return json.load(file)
    else:
        data = {'leaderboard': []}
        save_leaderboard(data)
        return data 

def save_leaderboard(data):
    with open(FILENAME, 'w') as file:
        json.dump(data, file, indent=2)

def add_player(name, score):
    data = load_leaderboard()
    data['leaderboard'].append({'name': name, 'score': score})
    data = update_ranks(data)
    save_leaderboard(data)
    print(f"Player {name} with score: {score} added to the leaderborad")

def update_ranks(data):
    sorted_players = sorted(
        data['leaderboard'],
        key=lambda x: x['score'],
        reverse = True
    )[:10]
    for i, player in enumerate(sorted_players, start=1):
        player['rank'] = i
    data['leaderboard'] = sorted_players
    return data

ship_img = pygame.transform.scale(ship_img, (40, 80))
bg_img = pygame.transform.scale(bg_img, (Width, Height))
astroid_img[0] = pygame.transform.scale(astroid_img[0], (70, 70))
astroid_img[1] = pygame.transform.scale(astroid_img[1], (60, 60))
astroid_img[2] = pygame.transform.scale(astroid_img[2], (50, 50))
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)
hit_sound = pygame.mixer.Sound('backround/hit.mp3')
hit_sound.set_volume(0.8)
class Asteroid:
    def __init__(self):
        num = random.randint(1,3)
        self.image = astroid_img[num-1]
        self.rect = self.image.get_rect(
            center=(random.randint(30, Width -30), random.randint(-200, -60))
        )
        if num == 1:
            self.speed = 3
        elif num == 2:
            self.speed = 6
        else:
            self.speed = 9

    def reset(self):
        self.rect.y = random.randint(-200, -60)
        self.rect.x = random.randint(30, Width -30)
        num = random.randint(1,3)
        self.image = astroid_img[num-1]
        global Ast_spd
        if num == 1:
            self.speed = 3*Ast_spd
        elif num == 2:
            self.speed = 6*Ast_spd
        else:
            self.speed = 9*Ast_spd
        self.rect = self.image.get_rect(center =(self.rect.x, self.rect.y))    
    def update(self):
        self.rect.y += self.speed
        global score
        global level
        global level_cap
        global Ast_spd

        if self.rect.top > Height:
            if num ==1:
                score += 5
            elif num == 2:
                score += 10
            else:
                score += 15
            if score > level_cap:
                level_cap += math.pow(2,level) + 1000
                level += 1
                Ast_spd += .3
            self.reset()


    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Rocket:
    def __init__(self):
        self.image = ship_img
        self.rect = self.image.get_rect(center = (Width//2, Height - 80))
        self.hitbox = pygame.Rect(self.rect.x, self.rect.y, 25, 50)
        self.speed = 5

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < Width:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < Height:
            self.rect.y += self.speed
        self.hitbox.x = self.rect.x+5
        self.hitbox.y = self.rect.y+25

    def draw(self, surface):
        surface.blit(self.image, self.rect)
text_imput = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 275), (900,50)), manager=maneger, object_id='#main_text_entry')
font = pygame.font.SysFont('upheavtt.ttf', 25)
MENU = 0
play = 1
current_state = MENU
start_img = pygame.image.load('backround/start.png').convert_alpha()
start_img_rect = start_img.get_rect()
start_img_rect.center = (250,250)

def main():
    running = True
    lives = 6
    bg_index = 0
    time_check = 0

    data = load_leaderboard()
    if data['leaderboard']:
        on_leaderbord = data['leaderboard'][-1]['score']
        rank_amm = len(data['leaderboard'])
    else: 
        on_leaderbord = 0
        rank_amm = 0 


    rocket = Rocket()
    Asteroids = [Asteroid() for _ in range(5)]

    while(running):
        ##time_delta = clock.tick(Frames)/1000
        dt = clock.tick(Frames)
        time_check += dt
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                    print(f"Text entered: {event.text}")

            maneger.process_events(event)
    
        maneger.update(dt)
        
        


        rocket.move(keys)

        for asteroid in Asteroids:
            asteroid.update()
            if rocket.hitbox.colliderect(asteroid.rect):
                lives -= 1
                hit_sound.play()
                asteroid.reset()
                if lives <= 0:
                    if rank_amm < 10 or score > on_leaderbord:
                        username = get_username()
                        add_player(username, score)
                    running = False

        screen.blit(bg_imgs[bg_index], (0,0))
        if time_check>= 125: 
            time_check = 0  
            bg_index+=1
            if bg_index==8:
             bg_index = 0
        rocket.draw(screen)
        for asteroid in Asteroids:
            asteroid.draw(screen)
        lives_text = font.render(f"Lives : {lives}", True, (255, 255,255))
        screen.blit(lives_text, (10,10))
        Score_text = font.render(f"Score : {score}", True, (255, 255,255))
        screen.blit(Score_text, (Width - 200, 10))
        Level_text = font.render(f"Level : {level}", True, (255, 255,255))
        screen.blit(Level_text, (Width - 280, 480))

        pygame.display.flip()

    
    screen.fill((0,0,0))
    ##game_over = font.render("Game Over!", True, (255, 0,0))
    screen.blit(pygame.transform.scale(load_image('backround/game_over.png'),(Width,Height)),(0,0))
    pygame.mixer.music.stop()
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()
##make screen biger after g-o and show leaderbord
if __name__ == "__main__":
    main_menu()