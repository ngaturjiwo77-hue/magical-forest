import pygame
import sys
import random
import math

from settings import *
from objects import VirtualJoystick, Player, MagicStar, Particle, AmbientDust, create_gradient_bg

# ==========================================
# SETUP LAYAR & GAME
# ==========================================
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Magical Forest Mobile")
clock = pygame.time.Clock()

player = Player()

joystick_x = int(JOYSTICK_RADIUS * 1.5)
joystick_y = HEIGHT - int(JOYSTICK_RADIUS * 1.5)
joystick = VirtualJoystick(joystick_x, joystick_y, JOYSTICK_RADIUS)

stars = [MagicStar() for _ in range(7)]
particles = []
dust_cloud = [AmbientDust() for _ in range(35)]

score = 0
level = 1
score_needed_for_levelup = 5

current_level_bg = create_gradient_bg(WIDTH, HEIGHT, LEVEL_THEMES[1][0], LEVEL_THEMES[1][1])

try:
    font = pygame.font.Font(None, FONT_LARGE)
    font_sub = pygame.font.Font(None, FONT_SMALL)
except:
    font = pygame.font.SysFont("sans-serif", FONT_LARGE)
    font_sub = pygame.font.SysFont("sans-serif", FONT_SMALL)

# ==========================================
# LOOP UTAMA GAME
# ==========================================
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        joystick.handle_event(event)

    player.move(joystick)

    for dust in dust_cloud:
        dust.update()

    for p in particles[:]:
        p.update()
        if p.alpha <= 0 or p.radius <= 0:
            particles.remove(p)

    for star in stars[:]:
        distance = math.hypot(player.x - star.x, player.y - star.y)
        if distance < player.radius + star.base_radius:
            for _ in range(12):
                particles.append(Particle(star.x, star.y, star.color))
            
            score += 1
            stars.remove(star)
            stars.append(MagicStar())

            if score >= level * score_needed_for_levelup:
                level += 1
                for _ in range(50):
                    particles.append(Particle(player.x, player.y, random.choice(STAR_COLORS), speed_mult=2.5))
                
                theme_key = level if level in LEVEL_THEMES else max(LEVEL_THEMES.keys())
                color_top, color_bottom = LEVEL_THEMES[theme_key]
                current_level_bg = create_gradient_bg(WIDTH, HEIGHT, color_top, color_bottom)
                player.speed += BASE_UNIT * 0.002

    screen.blit(current_level_bg, (0, 0))

    for dust in dust_cloud:
        dust.draw(screen)

    for star in stars:
        star.draw(screen)

    for p in particles:
        p.draw(screen)

    player.draw(screen)
    joystick.draw(screen)

    text_level = font.render(f"LEVEL: {level}", True, PLAYER_COLOR)
    text_score = font_sub.render(f"Energi Terkumpul: {score} / {level * score_needed_for_levelup}", True, TEXT_COLOR)
    text_guide = font_sub.render("Kumpulkan energi ajaib untuk menaikkan level hutan", True, (170, 160, 190))
    
    screen.blit(text_level, (40, 40))
    screen.blit(text_score, (40, 40 + FONT_LARGE))
    screen.blit(text_guide, (joystick_x + JOYSTICK_RADIUS + 30, HEIGHT - int(JOYSTICK_RADIUS * 1.3)))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
