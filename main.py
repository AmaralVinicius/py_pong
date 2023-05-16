import pygame
from pygame.locals import *
import random

pygame.init()
clock = pygame.time.Clock()

screen_width = 960
screen_height  = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('PyPong')

run = True

def text(font, color,text):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    return (text_surface, text_rect)

def ball_start(ball_rect, speed, score_timer):

    ball_rect.center = (screen_width / 2, screen_height / 2)

    current_time = pygame.time.get_ticks()
    if current_time - score_timer < 3500:
        ball_speed = [0, 0]
        if current_time - score_timer < 500:
            return score_timer, 0
        elif current_time - score_timer < 1500:
            return score_timer, 1
        elif current_time - score_timer < 2500:
            return score_timer, 2
        elif current_time - score_timer < 3500:
            return score_timer, 3
    else:
        score_timer = 0
        speed[0] = 9 * random.choice((1, -1))
        speed[1] = 9 * random.choice((1, -1))
        return score_timer, 0

def ball_moviment(ball_rect, speed):
    global score_timer
    if score_timer == 0:
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
            game_score['opponent_score'] += 1
            score_timer = pygame.time.get_ticks()
        if ball_rect.left <= 0:
            ball_rect.left = 0
            speed[0] *= -1
            game_score['player_score'] += 1
            score_timer = pygame.time.get_ticks()

    return ball_rect

font = pygame.font.SysFont("freesansbold", 30)
game_score = {'opponent_score': 0,  'player_score': 0}
score_timer = 1000
score_timer_counter = 0
score_background = pygame.Rect(0, 0, 400, 75)
score_background.center = (screen_width / 2, screen_height / 2)

player = pygame.Rect(screen_width - 30, screen_height / 2 - 70, 20, 140)
player_direction = 'idle'
down_button = False
up_button = False
player_speed  = 0
player_collision = {'top': False, 'bottom': False, 'right': False, 'left': False}
opponent = pygame.Rect(10, screen_height / 2 - 70, 20, 140)
opponent_speed = 7.5
opponent_collision = {'top': False, 'bottom': False, 'right': False, 'left': False}
ball = pygame.Rect(screen_width / 2 - 10, screen_height / 2 - 10, 20, 20)
ball_speed = [0, 0]

while run:
    screen.fill((11, 11, 21))

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == KEYDOWN:
            if event.key == K_DOWN and player.bottom <= screen_height:
                player_direction = 'down'
                down_button = True
            if event.key == K_UP and player.top >= 0:
                player_direction = 'up'
                up_button = True
        if event.type == KEYUP:
            if event.key == K_DOWN:
                down_button = False
                if up_button and player.top >= 0:
                    player_direction = 'up'
                else:
                    player_direction = 'idle'
            if event.key == K_UP:
                up_button = False
                if down_button and player.bottom <= screen_height:
                    player_direction = 'down'
                else:
                    player_direction = 'idle'

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

    if ball.colliderect(player):
        top = abs(ball.top - player.bottom)
        bottom = abs(ball.bottom - player.top)
        right = abs(ball.right - player.left)
        left = abs(ball.left - player.right)

        if min((top, bottom, right, left)) == top and ball_speed[1] < 0:
            player_collision['top'] = True
        if min((top, bottom, right, left)) == bottom and ball_speed[1] > 0:
            player_collision['bottom'] = True
        if min((top, bottom, right, left)) == right and ball_speed[0] > 0:
            player_collision['right'] = True
        if min((top, bottom, right, left)) == left and ball_speed[0] < 0:
            player_collision['left'] = True

        if player_collision['top']:
            ball.top = player.bottom
            ball_speed[1] = abs(ball_speed[1])
        if player_collision['bottom']:
            ball.bottom = player.top
            ball_speed[1] = -(abs(ball_speed[1]))
        if player_collision['right']:
            ball.right = player.left
            ball_speed[0] = -(abs(ball_speed[0]))
        if player_collision['left']:
            ball.left = player.right
            ball_speed[0] = abs(ball_speed[0])
    else:
        player_collision = {'top': False, 'bottom': False, 'right': False, 'left': False}

    if ball.colliderect(opponent):
        top = abs(ball.top - opponent.bottom)
        bottom = abs(ball.bottom - opponent.top)
        right = abs(ball.right - opponent.left)
        left = abs(ball.left - opponent.right)

        if min((top, bottom, right, left)) == top and ball_speed[1] < 0:
            opponent_collision['top'] = True
        if min((top, bottom, right, left)) == bottom and ball_speed[1] > 0:
            opponent_collision['bottom'] = True
        if min((top, bottom, right, left)) == right and ball_speed[0] > 0:
            opponent_collision['right'] = True
        if min((top, bottom, right, left)) == left and ball_speed[0] < 0:
            opponent_collision['left'] = True

        if opponent_collision['top']:
            ball.top = opponent.bottom
            ball_speed[1] = abs(ball_speed[1])
        if opponent_collision['bottom']:
            ball.bottom = opponent.top
            ball_speed[1] = -(abs(ball_speed[1]))
        if opponent_collision['right']:
            ball.right = opponent.left
            ball_speed[0] = -(abs(ball_speed[0]))
        if opponent_collision['left']:
            ball.left = opponent.right
            ball_speed[0] = abs(ball_speed[0])
        else:
            opponent_collision = {'top': False, 'bottom': False, 'right': False, 'left': False}

    pygame.draw.line(screen, (200, 200, 200), (screen_width / 2 - 1, 0), (screen_width / 2 - 1, screen_height), width = 2)
    pygame.draw.rect(screen, (11, 11, 21), score_background)

    opponent_score, opponent_score_rect = text(font, (255, 255, 255), f'{game_score["opponent_score"]}')
    opponent_score_rect.right = screen_width / 2 - 20
    opponent_score_rect.center = (opponent_score_rect.center[0], screen_height / 2)

    player_score, player_score_rect = text(font, (255, 255, 255), f'{game_score["player_score"]}')
    player_score_rect.left = screen_width / 2 + 20
    player_score_rect.center = (player_score_rect.center[0], screen_height / 2)

    screen.blit(opponent_score, opponent_score_rect)
    screen.blit(player_score, player_score_rect)

    pygame.draw.rect(screen, (225, 225, 225), player)
    pygame.draw.rect(screen, (225, 225, 225), opponent)
    pygame.draw.rect(screen, (225, 75, 75), ball)

    if score_timer_counter != 0:
        timer_text, timer_text_rect = text(font, (6, 6, 17), f'{score_timer_counter}')
        timer_text_rect.center = (screen_width / 2, screen_height / 2 + 1)
        screen.blit(timer_text,  timer_text_rect)

    if score_timer:
        score_timer, score_timer_counter = ball_start(ball, ball_speed, score_timer)

    clock.tick(60)
    pygame.display.update()

pygame.quit()
