#giriş noktası, ana döngü, ekran akışı

import sys
import pygame

from game import Game
from render import draw_map, draw_hud, draw_message
from settings import *


def main():
    pygame.init()
    game = Game(0)
    width = game.width * CELL
    height = HUD_HEIGHT + game.height * CELL
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pacman")
    font = pygame.font.SysFont("arial", 22, bold=True)
    clock = pygame.time.Clock()

    direction = None   # şu an gidilen yön
    wanted = None      # tuşla istenen yön
    start = pygame.time.get_ticks()
    last_move = start
    end_time = None

    running = True
    while running:
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    game = Game(0)
                    direction = None
                    wanted = None
                    start = now
                    last_move = now
                    end_time = None
                elif event.key in (pygame.K_UP, pygame.K_w):
                    wanted = "UP"
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    wanted = "DOWN"
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    wanted = "LEFT"
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    wanted = "RIGHT"

        # belli aralıklarla bir hamle yap
        if not game.is_finished() and now - last_move >= MOVE_DELAY:
            last_move = now
            if wanted is not None and game.can_move(wanted):
                direction = wanted
            if direction is not None and game.can_move(direction):
                game.step(direction)
            if game.is_finished():
                end_time = now

        if end_time is not None:
            elapsed = (end_time - start) / 1000
        else:
            elapsed = (now - start) / 1000

        screen.fill(BLACK)
        draw_hud(screen, font, game, elapsed, width)
        draw_map(screen, game)
        if game.completed:
            draw_message(screen, font, "Seviye tamamlandı (R: tekrar)", width, height)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


main()