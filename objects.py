import pygame
import random
import math
from settings import *

def create_gradient_bg(width, height, color1, color2):
    bg_surface = pygame.Surface((width, height))
    for y in range(0, height, 4):
        alpha = y / height
        r = int(color1[0] * (1 - alpha) + color2[0] * alpha)
        g = int(color1[1] * (1 - alpha) + color2[1] * alpha)
        b = int(color1[2] * (1 - alpha) + color2[2] * alpha)
        pygame.draw.rect(bg_surface, (r, g, b), (0, y, width, 4))
    return bg_surface

class VirtualJoystick:
    def __init__(self, x, y, radius):
        self.base_x = x
        self.base_y = y
        self.radius = radius
        self.stick_x = x
        self.stick_y = y
        self.stick_radius = STICK_RADIUS
        self.is_active = False
        self.output_x = 0.0
        self.output_y = 0.0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if math.hypot(mx - self.base_x, my - self.base_y) <= self.radius * 1.5:
                self.is_active = True
                self.update_position(mx, my)
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.is_active:
                self.is_active = False
                self.stick_x = self.base_x
                self.stick_y = self.base_y
                self.output_x = 0
                self.output_y = 0
                
        elif event.type == pygame.MOUSEMOTION:
            if self.is_active:
                mx, my = event.pos
                self.update_position(mx, my)

    def update_position(self, mx, my):
        dx = mx - self.base_x
        dy = my - self.base_y
        distance = math.hypot(dx, dy)

        if distance <= self.radius:
            self.stick_x = mx
            self.stick_y = my
        else:
            angle = math.atan2(dy, dx)
            self.stick_x = self.base_x + math.cos(angle) * self.radius
            self.stick_y = self.base_y + math.sin(angle) * self.radius
            distance = self.radius

        if distance > 0:
            self.output_x = (self.stick_x - self.base_x) / self.radius
            self.output_y = (self.stick_y - self.base_y) / self.radius

    def draw(self, surface):
        base_surf = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(base_surf, (255, 255, 255, 40), (self.radius, self.radius), self.radius)
        pygame.draw.circle(base_surf, (255, 255, 255, 90), (self.radius, self.radius), self.radius, 3)
        surface.blit(base_surf, (self.base_x - self.radius, self.base_y - self.radius))

        stick_surf = pygame.Surface((self.stick_radius * 2, self.stick_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(stick_surf, (143, 240, 217, 160), (self.stick_radius, self.stick_radius), self.stick_radius)
        pygame.draw.circle(stick_surf, (255, 255, 255, 220), (self.stick_radius, self.stick_radius), self.stick_radius - 5)
        surface.blit(stick_surf, (int(self.stick_x - self.stick_radius), int(self.stick_y - self.stick_radius)))

class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 3
        self.radius = PLAYER_RADIUS
        self.speed = BASE_UNIT * 0.012 
        self.vx = 0
        self.vy = 0
        self.friction = 0.85

    def move(self, joystick):
        dx, dy = 0, 0
        if joystick.is_active:
            dx = joystick.output_x * self.speed
            dy = joystick.output_y * self.speed

        self.vx = self.vx * self.friction + dx * (1 - self.friction)
        self.vy = self.vy * self.friction + dy * (1 - self.friction)

        self.x += self.vx
        self.y += self.vy

        self.x = max(self.radius, min(WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(HEIGHT - self.radius, self.y))

    def draw(self, surface):
        glow_surf = pygame.Surface((self.radius * 4, self.radius * 4), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (143, 240, 217, 30), (self.radius * 2, self.radius * 2), self.radius * 2)
        pygame.draw.circle(glow_surf, (143, 240, 217, 60), (self.radius * 2, self.radius * 2), self.radius * 1.3)
        surface.blit(glow_surf, (int(self.x - self.radius * 2), int(self.y - self.radius * 2)))
        
        pygame.draw.circle(surface, PLAYER_COLOR, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), self.radius - 5)

class MagicStar:
    def __init__(self):
        self.x = random.randint(int(STAR_MAX_RADIUS*2), WIDTH - int(STAR_MAX_RADIUS*2))
        self.y = random.randint(int(STAR_MAX_RADIUS*2), HEIGHT - int(JOYSTICK_RADIUS * 2.5))
        self.base_radius = random.randint(int(STAR_MAX_RADIUS*0.6), STAR_MAX_RADIUS)
        self.color = random.choice(STAR_COLORS)
        self.angle = random.uniform(0, 3.14)
        self.pulse_speed = random.uniform(0.04, 0.08)

    def draw(self, surface):
        self.angle += self.pulse_speed
        current_radius = self.base_radius + math.sin(self.angle) * (self.base_radius * 0.25)
        
        glow = pygame.Surface((int(current_radius * 3), int(current_radius * 3)), pygame.SRCALPHA)
        pygame.draw.circle(glow, (self.color[0], self.color[1], self.color[2], 50), (int(current_radius * 1.5), int(current_radius * 1.5)), int(current_radius * 1.5))
        surface.blit(glow, (int(self.x - current_radius * 1.5), int(self.y - current_radius * 1.5)))
        
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(current_radius))
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), int(current_radius * 0.4))

class Particle:
    def __init__(self, x, y, color, speed_mult=1.0):
        self.x = x
        self.y = y
        self.color = color
        self.vx = random.uniform(-3, 3) * speed_mult
        self.vy = random.uniform(-3, 3) * speed_mult
        self.radius = random.randint(3, 8)
        self.alpha = 255
        self.fade_speed = random.randint(4, 8)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.alpha -= self.fade_speed
        if self.radius > 0.1:
            self.radius -= 0.05

    def draw(self, surface):
        if self.alpha > 0 and self.radius > 0:
            p_surf = pygame.Surface((int(self.radius * 2), int(self.radius * 2)), pygame.SRCALPHA)
            pygame.draw.circle(p_surf, (self.color[0], self.color[1], self.color[2], self.alpha), (int(self.radius), int(self.radius)), int(self.radius))
            surface.blit(p_surf, (int(self.x - self.radius), int(self.y - self.radius)))

class AmbientDust:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.radius = random.uniform(1, 3.5)
        self.speed = random.uniform(0.3, 0.8)

    def update(self):
        self.y -= self.speed
        if self.y < -10:
            self.y = HEIGHT + 10
            self.x = random.randint(0, WIDTH)

    def draw(self, surface):
        dust_surf = pygame.Surface((int(self.radius*2), int(self.radius*2)), pygame.SRCALPHA)
        pygame.draw.circle(dust_surf, (255, 255, 255, 70), (int(self.radius), int(self.radius)), int(self.radius))
        surface.blit(dust_surf, (int(self.x - self.radius), int(self.y - self.radius)))
