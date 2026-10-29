#giriş noktası, ana döngü, ekran akışı

import sys
import time

import pygame

from levels import LEVELS, parse_level, validate_level

CELL = 32
HUD_HEIGHT = 60

# Renkler
BLACK = (0, 0, 0)
WALL = (33, 33, 222)
FOOD = (255, 184, 174)
PELLET = (255, 255, 255)
PACMAN = (255, 235, 0)
GHOST_COLORS = [(255, 0, 0), (255, 184, 255), (0, 255, 255), (255, 184, 82)]
HUD_BG = (20, 20, 30)
TEXT = (240, 240, 240)


class GameState:
    """Oyunun tüm durumu tek nesnede tutulur (AI simülasyonu için kopyalanabilir)."""

    def __init__(self, level_index=0):
        rows = LEVELS[level_index]
        validate_level(rows)
        self.rows = rows
        self.height = len(rows)
        self.width = len(rows[0])
        walls, food, pellets, pacman, ghosts = parse_level(rows)
        self.walls = walls
        self.food = food
        self.pellets = pellets
        self.pacman = pacman
        self.ghosts = ghosts
        self.score = 0
        self.start_time = time.time()

    @property
    def remaining_food(self):
        return len(self.food) + len(self.pellets)

    def elapsed(self):
        return time.time() - self.start_time


def draw_map(screen, state):
    for (r, c) in state.walls:
        rect = pygame.Rect(c * CELL, HUD_HEIGHT + r * CELL, CELL, CELL)
        pygame.draw.rect(screen, WALL, rect.inflate(-4, -4), border_radius=6)

    for (r, c) in state.food:
        center = (c * CELL + CELL // 2, HUD_HEIGHT + r * CELL + CELL // 2)
        pygame.draw.circle(screen, FOOD, center, 3)

    for (r, c) in state.pellets:
        center = (c * CELL + CELL // 2, HUD_HEIGHT + r * CELL + CELL // 2)
        pygame.draw.circle(screen, PELLET, center, 8)

    r, c = state.pacman
    center = (c * CELL + CELL // 2, HUD_HEIGHT + r * CELL + CELL // 2)
    pygame.draw.circle(screen, PACMAN, center, CELL // 2 - 3)

    for i, (r, c) in enumerate(state.ghosts):
        color = GHOST_COLORS[i % len(GHOST_COLORS)]
        center = (c * CELL + CELL // 2, HUD_HEIGHT + r * CELL + CELL // 2)
        pygame.draw.circle(screen, color, center, CELL // 2 - 3)


def draw_hud(screen, font, state, width):
    pygame.draw.rect(screen, HUD_BG, (0, 0, width, HUD_HEIGHT))
    items = [
        f"Puan: {state.score}",
        f"Süre: {state.elapsed():.1f} sn",
        f"Kalan yemek: {state.remaining_food}",
    ]
    x = 16
    for text in items:
        surf = font.render(text, True, TEXT)
        screen.blit(surf, (x, (HUD_HEIGHT - surf.get_height()) // 2))
        x += surf.get_width() + 40


def main():
    pygame.init()
    state = GameState(0)
    width = state.width * CELL
    height = HUD_HEIGHT + state.height * CELL
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pacman - Utility-Based AI")
    font = pygame.font.SysFont("arial", 22, bold=True)
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        screen.fill(BLACK)
        draw_hud(screen, font, state, width)
        draw_map(screen, state)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()