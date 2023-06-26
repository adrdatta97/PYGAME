import pygame
import random
import math 
from pygame import mixer 

# Initiazing pygame: 
pygame.init()

# Screen Resolution: 
screen = pygame.display.set_mode((800,600))

# Title of the Game:
pygame.display.set_caption("Adrika's Space Invasion Game")

# Icon of the Game : 
icon = pygame.image.load("astronaut.png")
pygame.display.set_icon(icon)

# Background :
background = pygame.image.load("Background.jpg")

# Add background music: 
mixer.music.load('background_music.mp3')
mixer.music.set_volume(0.2)
mixer.music.play(-1)

# Player Variables: 
img_player = pygame.image.load("spaceship.png")
player_x_axis = 368
player_y_axis = 510
player_x_change = 0

# Enemy Variables: 
img_enemy = []
enemy_x_axis = []
enemy_y_axis = []
enemy_x_change = []
enemy_y_change = []
number_of_enemies = 8

for e in range(number_of_enemies):
    img_enemy.append(pygame.image.load("enemy.png"))
    enemy_x_axis.append(random.randint(0, 736))
    enemy_y_axis.append(random.randint(50,200))
    enemy_x_change.append(1)
    enemy_y_change.append(50)


# Bullet Variables: 
img_bullet = pygame.image.load("bullet.png")
bullet_x_axis = 0
bullet_y_axis = 500
bullet_x_change = 0
bullet_y_change = 3
visible_bullet = False

# Score Variable : 
score = 0 
my_font = pygame.font.Font('freesansbold.ttf', 16)
text_x = 10
text_y = 10


# End of Game Text: 
end_font = pygame.font.Font('freesansbold.ttf', 50)

def final_text():
    my_final_font = end_font.render("Game Over", True, (255,255,255))
    screen.blit(my_final_font, (250, 250))

# Show Score Function : 
def show_score(x,y):
    text = my_font.render(f'Score: {score}', True, (255,255,255))
    screen.blit(text, (x,y))

# Player function : 
def player(x,y):
    screen.blit(img_player, (x,y))

# Enemy function : 
def enemy(x,y, en):
    screen.blit(img_enemy[en], (x,y))    

# Shoot bullet function : 
def shoot_bullet(x,y):
    global visible_bullet
    visible_bullet = True
    screen.blit(img_bullet, (x+16,y+10))

# Detect Collision function : 
def there_is_a_collision(x_1, y_1, x_2, y_2):
    distance = math.sqrt(math.pow(x_1 - x_2,2) + math.pow(y_1 - y_2,2))
    if distance < 27:
        return True
    else:
        return False


# Game Loop: 
is_running = True
while is_running:
    # Background : 
    screen.blit(background, (0,0))
    

    # Event Iteration : 
    for event in pygame.event.get():

        # Closing the Game: 
        if event.type == pygame.QUIT:
            is_running = False
        
        # Press key event : 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -1
            if event.key == pygame.K_RIGHT:
                player_x_change = 1
            if event.key == pygame.K_SPACE:
                bullet_sound = mixer.Sound('shot.mp3')
                bullet_sound.play()
                if visible_bullet == False:
                    bullet_x_axis = player_x_axis
                    shoot_bullet(bullet_x_axis, bullet_y_axis)

        # Released Key Event :         
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # Modify Player Location : 
    player_x_axis += player_x_change 

    # Keep our spaceship inside the screen : 
    if player_x_axis <= 0:
        player_x_axis = 0 
    elif player_x_axis >= 736:
        player_x_axis = 736

    # Modify Enemy Location : 
    for enem in range(number_of_enemies):
        # End of Game : 
        if enemy_y_axis[enem] > 500:
            for k in range(number_of_enemies):
                enemy_y_axis[k] = 1000
            final_text()
            break
        enemy_x_axis[enem] += enemy_x_change[enem]

    # Keep enemy inside the screen : 
        if enemy_x_axis[enem] <= 0:
            enemy_x_change[enem] = 1
            enemy_y_axis[enem] += enemy_y_change[enem]
        elif enemy_x_axis[enem] >= 736:
            enemy_x_axis[enem] = -1
            enemy_y_axis[enem] += enemy_y_change[enem]

        # Collision : 
        collision = there_is_a_collision(enemy_x_axis[enem],enemy_y_axis[enem],bullet_x_axis,bullet_y_axis)
        if collision:
            collision_sound = mixer.Sound('punch.mp3')
            collision_sound.play()
            bullet_y_axis = 500
            visible_bullet = False 
            score += 1
            enemy_x_axis[enem] = random.randint(0, 736)
            enemy_y_axis[enem] = random.randint(50,200)

        enemy(enemy_x_axis[enem], enemy_y_axis[enem], enem)


    # Bullet Movement : 
    if bullet_y_axis <= -32:
        bullet_y_axis = 500
        visible_bullet = False
    if visible_bullet:
        shoot_bullet(bullet_x_axis, bullet_y_axis)
        bullet_y_axis -= bullet_y_change



    player(player_x_axis, player_y_axis)
    
    show_score(text_x, text_y)
    # Update : 
    pygame.display.update()





