#tüm çizim işlmeleri

import pygame
from settings import *


def cell_center(r, c):
    return (c * CELL + CELL // 2, HUD_HEIGHT + r * CELL + CELL // 2)


def draw_map(screen, game):
    for r, c in game.walls:
        rect = pygame.Rect(c * CELL + 2, HUD_HEIGHT + r * CELL + 2, CELL - 4, CELL - 4)
        pygame.draw.rect(screen, WALL_COLOR, rect, border_radius=6)

    for r, c in game.food:
        pygame.draw.circle(screen, FOOD_COLOR, cell_center(r, c), 3)

    for r, c in game.pellets:
        pygame.draw.circle(screen, PELLET_COLOR, cell_center(r, c), 8)

    pygame.draw.circle(screen, PACMAN_COLOR, cell_center(*game.pacman), CELL // 2 - 3)

    for i in range(len(game.ghosts)):
        if game.power > 0:
            color = SCARED_COLOR
        else:
            color = GHOST_COLORS[i % len(GHOST_COLORS)]
        pygame.draw.circle(screen, color, cell_center(*game.ghosts[i]), CELL // 2 - 3)


def draw_hud(screen, font, game, elapsed, width):
    pygame.draw.rect(screen, HUD_COLOR, (0, 0, width, HUD_HEIGHT))

    texts = [
        "Puan: " + str(game.score),
        "Süre: " + str(round(elapsed, 1)) + " sn",
        "Kalan yemek: " + str(game.food_left()),
    ]
    if game.power > 0:
        texts.append("Enerji: " + str(game.power))

    x = 16
    for t in texts:
        img = font.render(t, True, TEXT_COLOR)
        screen.blit(img, (x, 18))
        x += img.get_width() + 30


def draw_message(screen, font, text, width, height):
    img = font.render(text, True, TEXT_COLOR)
    rect = img.get_rect(center=(width // 2, height // 2))
    pygame.draw.rect(screen, HUD_COLOR, rect.inflate(30, 20))
    screen.blit(img, rect)