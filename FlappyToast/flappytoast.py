import pygame, random
from utils import *
from enum import Enum
from toasterio import IOEvents
from common import Window, BaseEvents, NavigationDestination
from gamescreen import GameScreen

class FlappyToastScreen(GameScreen):
    GROUND_OFFSET = 124
    FLOOR_POS = Window.WIDTH - GROUND_OFFSET
    
    class GameState(Enum):
        IDLE = "idle"
        RUNNING = "running"
        GAME_OVER = "game_over"

    def create_pipe(self):
        if not self.game_state == self.GameState.RUNNING:
            return []
        random_pipe_pos = random.choice(self.pipe_height)
        bottom_pipe = self.pipe_surface.get_rect(midleft = (random_pipe_pos, -100))
        top_pipe = self.pipe_surface.get_rect(midright = (random_pipe_pos-self.pipe_gap, -100))
        return bottom_pipe, top_pipe

    def draw_floor(self, screen):
        blit(screen, self.floor_surface, (self.FLOOR_POS, self.floor_y_pos))
        blit(screen, self.floor_surface, (self.FLOOR_POS, self.floor_y_pos-984))

    def move_pipes(self, pipes):
        for pipe in pipes:
            pipe.centery += self.floor_speed
        return list(filter(lambda pipe: pipe.top < Window.HEIGHT, pipes))

    def draw_pipes(self, pipes, screen):
        for pipe in pipes:
            if pipe.right >= Window.WIDTH:
                screen.blit(self.pipe_surface, pipe)
            else:
                blit(screen, self.flip_pipe_surface, pipe)

    def check_collision(self, pipes):
        for i in range(0, min(2, len(pipes)-1)):
            pipe = pipes[i]
            if self.bird_rect.colliderect(pipe):
                return self.game_over()
        if self.bird_rect.left < -100 or self.bird_rect.right >= self.FLOOR_POS:
            self.bird_rect.right = self.FLOOR_POS
            return self.game_over()
        return self.GameState.RUNNING

    def game_over(self):
        global disable_timer
        self.death_sound.play()
        disable_timer = 30
        return self.GameState.GAME_OVER

    def rotate_bird(self, bird):
        rotation = -3 if self.bird_movement < 0 else -6
        return pygame.transform.rotozoom(bird, self.bird_movement * rotation, 1)

    def bird_animation(self):
        new_bird = self.bird_frames[self.bird_index]
        new_bird_rect = new_bird.get_rect(center = (100, self.bird_rect.centery))
        return new_bird, new_bird_rect

    def score_display(self, screen):
        if self.game_state == self.GameState.RUNNING:
            score_surface = self.game_font.render(str(self.score), True, (255,255,255))
            score_surface = pygame.transform.rotate(score_surface, 90)
            score_rect = score_surface.get_rect(center = (50, Window.HEIGHT/2))
            blit(screen, score_surface, score_rect)
        if self.game_state == self.GameState.IDLE or self.game_state == self.GameState.GAME_OVER:
            score_surface = self.game_font.render(f'Score: {self.score}', True, (255,255,255))
            score_surface = pygame.transform.rotate(score_surface, 90)
            score_rect = score_surface.get_rect(center = (50, Window.HEIGHT/2))
            blit(screen, score_surface, score_rect)

            high_score_surface = self.game_font.render(f'High score: {self.high_score}', True, (255,255,255))
            high_score_surface = pygame.transform.rotate(high_score_surface, 90)
            high_score_rect = high_score_surface.get_rect(center = (750, Window.HEIGHT/2))
            blit(screen, high_score_surface, high_score_rect)

    def update_score(self, score, high_score, pipes):
        if len(pipes) == 0:
            return score, high_score
        
        pipe_center = pipes[0].centery
        if self.bird_rect.centery in range(pipe_center-self.floor_speed, pipe_center):
            score += 1
            self.score_sound.play()
        
        if score > high_score:
            high_score = score
        
        return score, high_score

    def __init__(self):
        self.game_font = pygame.font.Font("fonts/04B_19.TTF", 40)

        # Game Variables
        self.gravity = 0.5
        self.bird_movement = 0
        self.game_state = self.GameState.IDLE
        self.score = 0
        self.high_score = 0
        self.floor_speed = 3
        self.bird_jump = 9
        self.pipe_gap = 145
        self.disable_timer = 0

        # Surfaces
        self.btn_back = Icon("sprites/ic_back.png", (44, Window.HEIGHT - 44), NavigationDestination.BACK)

        self.bg_surface = loadAndScale("sprites/background-day.png")

        self.floor_surface = loadAndScale("sprites/base.png")
        self.floor_y_pos = 0
 
        bird_downflap = loadAndScale("sprites/bluebird-downflap.png", True)
        bird_midflap = loadAndScale("sprites/bluebird-midflap.png", True)
        bird_upflap = loadAndScale("sprites/bluebird-upflap.png", True)
        self.bird_frames = [bird_downflap, bird_midflap, bird_upflap]
        self.bird_index = 0
        self.bird_surface = self.bird_frames[self.bird_index]
        self.bird_rect = self.bird_surface.get_rect(center=(Window.WIDTH/2, Window.HEIGHT - 100))

        self.pipe_surface = loadAndScale("sprites/pipe-green.png")
        self.flip_pipe_surface = pygame.transform.flip(self.pipe_surface, True, False)
        self.pipe_list = []
        self.SPAWNPIPE = BaseEvents.FLAPPY_TOAST


        pygame.time.set_timer(self.SPAWNPIPE, 2000)
        self.pipe_height = [200, 250, 300, 350]

        self.BUTTONPRESS = BaseEvents.FLAPPY_TOAST + 1
        self.BIRDFLAP = BaseEvents.FLAPPY_TOAST + 2
        pygame.time.set_timer(self.BIRDFLAP, 200)

        self.game_over_surface = loadAndScale("sprites/message.png", True)
        self.game_over_rect = self.game_over_surface.get_rect(center = (Window.WIDTH/2,Window.HEIGHT/2))

        self.flap_sound = loadSound("audio/wing.wav")
        self.death_sound = loadSound("audio/hit.wav")
        self.score_sound = loadSound("audio/point.wav")

    def tick(self, screen, events):
        if self.disable_timer > 0:
            self.disable_timer -= 1

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.btn_back.check_press(event.pos)
            if event.type == IOEvents.EVENT_BUTTON_PRESS:
                if self.disable_timer <= 0:
                    if self.game_state != self.GameState.RUNNING:
                        self.game_state = self.GameState.RUNNING
                        self.pipe_list = []
                        self.bird_rect.centerx = Window.WIDTH/2
                        self.score = 0
                    self.bird_movement = -self.bird_jump
                    self.flap_sound.play()
            if event.type == self.BIRDFLAP:
                self.bird_index = (self.bird_index + 1) % len(self.bird_frames)
                self.bird_surface, _ = self.bird_animation()
            if event.type == self.SPAWNPIPE:
                self.pipe_list.extend(self.create_pipe())

        blit(screen, self.bg_surface, (0,0))

        if self.game_state == self.GameState.RUNNING:
            # Bird
            self.bird_movement += self.gravity
            rotated_bird = self.rotate_bird(self.bird_surface)
            self.bird_rect.centerx += self.bird_movement
            blit(screen, rotated_bird, self.bird_rect)
            
            # Pipes
            self.pipe_list = self.move_pipes(self.pipe_list)
            self.draw_pipes(self.pipe_list, screen)

            self.game_state = self.check_collision(self.pipe_list)
            self.score, self.high_score = self.update_score(self.score, self.high_score, self.pipe_list)
        else:
            rotated_bird = self.rotate_bird(self.bird_surface)
            blit(screen, rotated_bird, self.bird_rect)

            self.draw_pipes(self.pipe_list, screen)

            blit(screen, self.game_over_surface, self.game_over_rect)
            

        # Floor
        if self.game_state != self.GameState.GAME_OVER:
            self.floor_y_pos += self.floor_speed
        self.draw_floor(screen)
        if self.floor_y_pos >= 984:
            self.floor_y_pos = 0

        self.score_display(screen)

        self.btn_back.draw(screen)