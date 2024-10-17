import pygame
import random
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Initializing mixer
pygame.mixer.init()

# Initializing game
pygame.init()

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
grey = (50, 50, 50)

# Constants
UI_HEIGHT = 75  # Reserved space for UI
screen_width = 900
screen_height = 500
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Background Images
bg_home = pygame.image.load("img/bg-home.png")
bg_home = pygame.transform.scale(bg_home, (screen_width, screen_height)).convert_alpha()

bg_game = pygame.image.load("img/bg-game.jpg")
bg_game = pygame.transform.scale(bg_game, (screen_width, screen_height - UI_HEIGHT)).convert_alpha()

# Game Title
pygame.display.set_caption("Game Title")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 50)

# Function to display score on game screen
def display_text(text, color, x, y):
    text = font.render(text, True, color)
    gameWindow.blit(text, [x, y])

def snake_increment(gameWindow, color, snk_len, snake_w, snake_h):
    for x, y in snk_len:
        pygame.draw.rect(gameWindow, color, [x, y, snake_w, snake_h])

# Home Page
def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.blit(bg_home, [0, 0])
        display_text("Welcome to Snakes", white, 200, 200)
        display_text("Press Space Bar To Play", white, 180, 240)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()

        pygame.display.update()
        clock.tick(60)

# Game Loop
def game_loop():
    # Game Variables
    exit_game = False
    game_over = False
    fps = 60
    snake_x = 100
    snake_y = 100
    snake_w = 10
    snake_h = 10
    food_x = random.randint(25, screen_width - 25)
    food_y = random.randint(UI_HEIGHT + 10, screen_height - 25)
    food_w = 10
    food_h = 10
    velocity = 2.5
    snakeVelocity_x = 0
    snakeVelocity_y = 0
    score = 0

    # Read high score
    if os.path.exists("High_Score.txt"):
        with open("High_Score.txt") as f:
            hiscore = f.read().strip()
            if hiscore.isdigit():
                hiscore = int(hiscore)
            else:
                hiscore = 0
    else:
        hiscore = 0
        with open("High_Score.txt", "w") as f:
            f.write(str(hiscore))

    snk_len = []
    snake_length = 1
    
    while not exit_game:
        if game_over:
            gameWindow.fill(grey)
            display_text("Game Over! Press Enter to play again", red, 180, 200)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_loop()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        snakeVelocity_x = velocity
                        snakeVelocity_y = 0
                    if event.key == pygame.K_LEFT:
                        snakeVelocity_x = -velocity
                        snakeVelocity_y = 0
                    if event.key == pygame.K_UP:
                        snakeVelocity_y = -velocity
                        snakeVelocity_x = 0
                    if event.key == pygame.K_DOWN:
                        snakeVelocity_y = velocity
                        snakeVelocity_x = 0
                
            snake_x += snakeVelocity_x
            snake_y += snakeVelocity_y

            # Check for food collision
            if abs(snake_x - food_x) < 6 and abs(snake_y - food_y) < 6:
                score += 10
                if score > hiscore:
                    hiscore = score
                    with open("High_Score.txt", "w") as f:
                        f.write(str(hiscore))
                snake_length += 3
                velocity += velocity * 0.05

                food_x = random.randint(25, screen_width - 25)
                food_y = random.randint(UI_HEIGHT + 10, screen_height - 25)

            # Render game background
            gameWindow.fill(grey)
            gameWindow.blit(bg_game, [0, UI_HEIGHT])

            # Display score and high score
            display_text("Score: " + str(score), red, 5, 5)
            display_text("High Score: " + str(hiscore), red, 5, 35)

            # Draw food
            pygame.draw.rect(gameWindow, red, [food_x, food_y, food_w, food_h])

            head = [snake_x, snake_y]
            snk_len.append(head)

            if len(snk_len) > snake_length:
                del snk_len[0]

            # Check for self-collision
            if head in snk_len[:-1]:
                game_over = True

            # Check for wall collisions
            if snake_x < 0 or snake_x + snake_w > screen_width or snake_y < UI_HEIGHT or snake_y + snake_h > screen_height:
                game_over = True

            # Draw snake
            snake_increment(gameWindow, black, snk_len, snake_w, snake_h)

        # Update the game window
        pygame.display.update()

        # Frame rate control
        clock.tick(fps)
                
    pygame.quit()
    sys.exit()

# Start game
welcome()