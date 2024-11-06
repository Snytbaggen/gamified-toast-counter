import pygame, sys, random
import RPi.GPIO as GPIO
from enum import Enum

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 480
GROUND_OFFSET = 62
FLOOR_POS = WINDOW_HEIGHT - GROUND_OFFSET
BUTTON_PIN = 37

class GameState(Enum):
    IDLE = "idle"
    RUNNING = "running"
    GAME_OVER = "game_over"

def create_pipe():
    if not game_state == GameState.RUNNING:
        return []
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (WINDOW_WIDTH + 100,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (WINDOW_WIDTH + 100,random_pipe_pos-pipe_gap))
    return bottom_pipe, top_pipe

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos,FLOOR_POS))
    screen.blit(floor_surface, (floor_x_pos+984,FLOOR_POS))

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= x_speed
    return list(filter(lambda pipe: pipe.right > 0, pipes))

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= WINDOW_HEIGHT:
            screen.blit(pipe_surface, pipe)
        else:
            screen.blit(flip_pipe_surface, pipe)

def check_collision(pipes):
    for i in range(0, min(2, len(pipes)-1)):
        pipe = pipes[i]
        if bird_rect.colliderect(pipe):
            return game_over()
    if bird_rect.top < -100 or bird_rect.bottom >= FLOOR_POS:
        bird_rect.bottom = FLOOR_POS
        return game_over()
    return GameState.RUNNING

def game_over():
    global disable_timer
    death_sound.play()
    disable_timer = 30
    return GameState.GAME_OVER

def rotate_bird(bird):
    rotation = -3 if bird_movement < 0 else -6
    return pygame.transform.rotozoom(bird, bird_movement * rotation, 1)

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display():
    if game_state == GameState.RUNNING:
        score_surface = game_font.render(str(score), True, (255,255,255))
        score_rect = score_surface.get_rect(center = (WINDOW_WIDTH/2, 50))
        screen.blit(score_surface, score_rect)
    if game_state == GameState.IDLE or game_state == GameState.GAME_OVER:
        score_surface = game_font.render(f'Score: {score}', True, (255,255,255))
        score_rect = score_surface.get_rect(center = (WINDOW_WIDTH/2, 50))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High score: {high_score}', True, (255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (WINDOW_WIDTH/2, 400))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score, pipes):
    if len(pipes) == 0:
        return score, high_score
    
    pipe_center = pipes[0].centerx
    if bird_rect.centerx in range(pipe_center-x_speed, pipe_center):
        score += 1
        score_sound.play()
    
    if score > high_score:
        high_score = score
    
    return score, high_score

def check_button():
    global button_state
    new_state = not GPIO.input(BUTTON_PIN) # Active low, so we invert it
    if button_state != new_state:
        button_state = new_state
        if button_state:
            pygame.event.post(pygame.event.Event(BUTTONPRESS))

pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), vsync=1)
clock = pygame.time.Clock()
game_font = pygame.font.Font("04B_19.TTF",40)

# Hardware setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
button_state = False

# Game Variables
gravity = 0.5
bird_movement = 0
game_state = GameState.IDLE
score = 0
high_score = 0
x_speed = 3
bird_jump = 8
pipe_gap = 100
disable_timer = 0

# Surfaces
bg_surface = pygame.image.load("sprites/background-day.png").convert()

floor_surface = pygame.image.load("sprites/base.png").convert()
floor_x_pos = 0

bird_downflap = pygame.image.load("sprites/bluebird-downflap.png").convert_alpha()
bird_midflap = pygame.image.load("sprites/bluebird-midflap.png").convert_alpha()
bird_upflap = pygame.image.load("sprites/bluebird-upflap.png").convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100,WINDOW_HEIGHT/2))

BUTTONPRESS = pygame.USEREVENT + 1
BIRDFLAP = pygame.USEREVENT + 2
pygame.time.set_timer(BIRDFLAP, 200)

pipe_surface = pygame.image.load("sprites/pipe-green.png").convert()
flip_pipe_surface = pygame.transform.flip(pipe_surface, False, True)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [200, 250, 300, 350]

game_over_surface = pygame.image.load("sprites/message.png").convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))

flap_sound = pygame.mixer.Sound("audio/wing.wav")
death_sound = pygame.mixer.Sound("audio/hit.wav")
score_sound = pygame.mixer.Sound("audio/point.wav")

while True:
    check_button()
    
    if disable_timer > 0:
        disable_timer -= 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN or event.type == BUTTONPRESS:
            if disable_timer <= 0:
                if game_state != GameState.RUNNING:
                    game_state = GameState.RUNNING
                    pipe_list = []
                    bird_rect.centery = WINDOW_HEIGHT/2
                    score = 0
                bird_movement = -bird_jump
                flap_sound.play()
        if event.type == BIRDFLAP:
            bird_index = (bird_index + 1) % len(bird_frames)
            bird_surface, bird_rect = bird_animation()
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    screen.blit(bg_surface, (0,0))

    if game_state == GameState.RUNNING:
        # Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        game_state = check_collision(pipe_list)
        score, high_score = update_score(score, high_score, pipe_list)
        score_display()
    else:
        rotated_bird = rotate_bird(bird_surface)
        screen.blit(rotated_bird, bird_rect)

        draw_pipes(pipe_list)

        screen.blit(game_over_surface, game_over_rect)
        score_display()

    # Floor
    if game_state != GameState.GAME_OVER:
        floor_x_pos -= x_speed
    draw_floor()
    if floor_x_pos <= -984:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(60)
