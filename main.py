import random
import math
import pygame
from pygame import mixer

# Initialize the pygame module
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Set the background image
background = pygame.image.load("background.png")

# Set background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Create the title and icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Displaying the score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 28)
textX = 10
textY = 10


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# Displaying game over
over_font = pygame.font.Font("freesansbold.ttf", 64)


def game_over_text(x, y):
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


# Create the player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
player_change = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


# Create multiple enemies
enemyImg = []
enemyX = []
enemyY = []
enemy_changeX = []
enemy_changeY = []
num_of_enemies = 5

# Create the enemy
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemy_changeX.append(5)
    enemy_changeY.append(40)


def enemy(x, y):
    screen.blit(enemyImg[i], (x, y))


# Create the bullet
# ready state is when you don't see a bullet on screen
# Fire state is when the bullet is moving
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bullet_changeX = 0
bullet_changeY = 10
bullet_state = "ready"


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y - 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance <= 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    # RGB (Setting the background)
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # checks the type of the keystroke (whether the key is pressed)
        if event.type == pygame.KEYDOWN:
            # If the key is pressed checks which key is pressed
            if event.key == pygame.K_LEFT:
                player_change = -5
            if event.key == pygame.K_RIGHT:
                player_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        # checks the type of the keystroke (whether the key is released)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_change = 0

    # Player movement mechanics
    playerX += player_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    player(playerX, playerY)

    # Enemy movement mechanics
    for i in range(num_of_enemies):

        # Displaying game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
                game_over_text(200, 250)
                break
            break
        enemyX[i] += enemy_changeX[i]
        if enemyX[i] <= 0:
            enemy_changeX[i] = 5
            enemyY[i] += enemy_changeY[i]
        elif enemyX[i] >= 736:
            enemy_changeX[i] = -5
            enemyY[i] += enemy_changeY[i]
        enemy(enemyX[i], enemyY[i])

        # Checks collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

    # Bullet movement mechanics
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bullet_changeY


    show_score(textX, textY)
    pygame.display.update()
