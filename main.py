import pygame
from pygame.locals import *
from random import randint

pygame.init()
clock = pygame.time.Clock()

screen_width = 960
screen_height  = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('PyPong')

run = True

def ball_moviment(ball_rect, speed):
    ball_rect.x += speed[0]
    ball_rect.y += speed[1]
    
    if ball_rect.top <= 0:
        ball_rect.top = 0
        speed[1] *= -1
    if ball_rect.bottom >= screen_height:
        ball_rect.bottom = screen_height
        speed[1] *= -1
    if ball_rect.right >= screen_width:
        ball_rect.right = screen_width
        speed[0] *= -1
        ball_rect = pygame.Rect(screen_width / 2 - 10, screen_height / 2 - 10, 20, 20)
    if ball_rect.left <= 0:
        ball_rect.left = 0
        speed[0] *= -1
        ball_rect = pygame.Rect(screen_width / 2 - 10, screen_height / 2 - 10, 20, 20)

    return ball_rect

player = pygame.Rect(screen_width - 30, screen_height / 2 - 70, 20, 140)
player_direction = 'idle'
down_button = False
up_button = True
player_speed  = 0
opponent = pygame.Rect(10, screen_height / 2 - 70, 20, 140)
opponent_speed = 7
ball = pygame.Rect(screen_width / 2 - 10, screen_height / 2 - 10, 20, 20)
ball_speed = [7, 7]

while run:

    screen.fill((11, 11, 21))

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == KEYDOWN:
            if event.key == K_DOWN and player.bottom < screen_height:
                player_direction = 'down'
                down_button = True
            if event.key == K_UP and player.top > 0:
                player_direction = 'up'
                up_button = True
        if event.type == KEYUP:
            if event.key == K_DOWN:
                down_button = False
                if up_button and player.top > 0:
                    player_direction = 'up'
                else:
                    player_direction = 'idle'
            if event.key == K_UP:
                up_button = False
                if down_button and player.bottom < screen_height:
                    player_direction = 'down'
                else:
                    player_direction = 'idle'

    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed[0] *= -1

    if opponent.center[1] < ball.center[1] and opponent.bottom < screen_height:
        opponent.y  += opponent_speed
    if opponent.center[1] > ball.center[1] and opponent.top > 0:
        opponent.y -= opponent_speed

    if player_direction == 'idle':
        player_speed = 0
    elif player_direction == 'down':
        player_speed = 10
    elif player_direction == 'up':
        player_speed = -10

    player.y += player_speed

    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

    ball = ball_moviment(ball, ball_speed)

    pygame.draw.line(screen, (200, 200, 200), (screen_width / 2 - 1, 0), (screen_width / 2 - 1, screen_height), width = 2)
    pygame.draw.rect(screen, (225, 225, 225), player)
    pygame.draw.rect(screen, (225, 225, 225), opponent)
    pygame.draw.rect(screen, (225, 225, 225), ball)

    clock.tick(60)
    pygame.display.update()

pygame.quit()
