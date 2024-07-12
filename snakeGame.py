import pygame
import random
import logging
import os
import json

logging.basicConfig(level=logging.DEBUG)

# Initialisation Pygame
print(pygame.ver)
pygame.init()

# Set up display
width,height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game !!')

# Load food images
cherry_img = pygame.image.load("images/cerise.png")
apple_img = pygame.image.load("images/pomme.png")
banana_img = pygame.image.load("images/banane.png")

# List of available food images
food_images = [cherry_img, apple_img, banana_img]

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
purple = (128, 0, 128)
red = (255, 0, 0)

# Snake properties
snake_pos = [100, 58]
snake_body = [[100, 50], [90, 50], [80, 50]]
snake_direction = 'RIGHT' # Initialise snake_direction
change_to = snake_direction

# Food properties
food_pos = [random.randrange(1,(width//10)) * 10, 
            random.randrange(1,(height//10)) * 10]

food_spawn = True
current_food_image = random.choice(food_images)

# Score
score = 0

my_font = pygame.font.SysFont('times new roman', 30)

# Draw Score function
def draw_score(score):
    score_surface = my_font.render('Scrore: ' + str(score), True, white)
    score_rect = score_surface.get_rect()
    score_rect.midtop = (width/2, 10)
    screen.blit(score_surface, score_rect)

# Game over function
def game_over():
    game_over_surface = my_font.render('Your Scrore is: ' + str(score), True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (width/2, height/4)
    screen.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    # pygame.quit()
    pygame.time.wait(2000)
    pygame.quit()

    with open("snake_score.json", "w") as score_file:
        json.dump({"score": score}, score_file)

    os._exit(0)    
  
# Draw Food function
def draw_food():
    screen.blit(current_food_image, (food_pos[0], food_pos[1]))
  
# Main Function
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to= 'RIGHT'
                            
    # Validation of directions
    if change_to == 'UP' and snake_direction != 'DOWN':
        snake_direction = 'UP'
    if change_to == 'DOWN' and snake_direction != 'UP':
        snake_direction = 'DOWN'
    if change_to == 'LEFT' and  snake_direction != 'RIGHT':
        snake_direction = 'LEFT'
    if change_to == 'RIGHT' and snake_direction != 'LEFT':
        snake_direction = 'RIGHT'
    
    # Moving the snake
    if snake_direction == 'UP':
        snake_pos[1] -= 10
    if snake_direction == 'DOWN':
        snake_pos[1] += 10
    if snake_direction == 'LEFT':
        snake_pos[0] -= 10
    if snake_direction == 'RIGHT':
        snake_pos[0] += 10
    
    # Snake body growing 
    snake_body.insert(0, list(snake_pos))
    
    # Collision with food and growing
    #if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
    if (
    food_pos[0] <= snake_pos[0] < food_pos[0] + 10 and
    food_pos[1] <= snake_pos[1] < food_pos[1] + 10
    ):
        score += 1
        food_spawn = False
    else:
        snake_body.pop()
        
    if not food_spawn:
        food_pos = [random.randrange(1, (width//10)) * 10, 
                    random.randrange(1, (height//10)) * 10]
        food_spawn = True

    # Draw Snake
    screen.fill(black)
    for pos in snake_body:
        pygame.draw.rect(screen, purple, pygame.Rect(pos[0], pos[1], 10, 10))
        
    # Draw Food
    #pygame.draw.rect(screen, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))
    draw_food()

    # Draw Score
    draw_score(score)

    # Game Over conditions
    if snake_pos[0] < 0 or snake_pos[0] > width-10: game_over()
    if snake_pos[1] < 0 or snake_pos[1] > height-10: game_over()
        
    # Touching the snake body
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]: game_over()
            
    # Refresh screen
    pygame.display.update()

    # Frame Per Second/ Refresh Rate Control
    pygame.time.Clock().tick(15)