#tüm çizim işlemleri

import math
import pygame
from settings import *

# pacman'in ağzı hangi yöne baksın (açı derece)
MOUTH_ANGLE = {"RIGHT": 0, "UP": 90, "LEFT": 180, "DOWN": 270}


def cell_center(r, c):
    return (c * CELL + CELL // 2, HUD_HEIGHT + r * CELL + CELL // 2)


def draw_pacman(screen, pos, facing, tick):
    cx, cy = cell_center(*pos)
    radius = CELL // 2 - 3
    # ağız açılıp kapansın
    opening = 10 + 30 * abs(math.sin(tick / 120))
    base = MOUTH_ANGLE.get(facing, 0)
    points = [(cx, cy)]
    a = base + opening
    while a <= base + 360 - opening:
        rad = math.radians(a)
        points.append((cx + radius * math.cos(rad), cy - radius * math.sin(rad)))
        a += 10
    pygame.draw.polygon(screen, PACMAN_COLOR, points)


def draw_ghost(screen, pos, color):
    cx, cy = cell_center(*pos)
    radius = CELL // 2 - 3
    # üstte yarım daire, altta dikdörtgen gövde
    pygame.draw.circle(screen, color, (cx, cy - 2), radius)
    body = pygame.Rect(cx - radius, cy - 2, radius * 2, radius)
    pygame.draw.rect(screen, color, body)
    # gözler
    for dx in (-5, 5):
        pygame.draw.circle(screen, (255, 255, 255), (cx + dx, cy - 4), 4)
        pygame.draw.circle(screen, (20, 20, 120), (cx + dx, cy - 4), 2)


def draw_map(screen, game, facing="RIGHT", tick=0):
    for r, c in game.walls:
        rect = pygame.Rect(c * CELL + 2, HUD_HEIGHT + r * CELL + 2, CELL - 4, CELL - 4)
        pygame.draw.rect(screen, WALL_COLOR, rect, border_radius=6)

    for r, c in game.food:
        pygame.draw.circle(screen, FOOD_COLOR, cell_center(r, c), 3)

    for r, c in game.pellets:
        pygame.draw.circle(screen, PELLET_COLOR, cell_center(r, c), 8)

    draw_pacman(screen, game.pacman, facing, tick)

    for i in range(len(game.ghosts)):
        if game.power > 0:
            color = SCARED_COLOR
        else:
            color = GHOST_COLORS[i % len(GHOST_COLORS)]
        draw_ghost(screen, game.ghosts[i], color)


def draw_hud(screen, font, small, game, elapsed, width, player_text):
    pygame.draw.rect(screen, HUD_COLOR, (0, 0, width, HUD_HEIGHT))

    # üst satır: kim oynuyor, hangi seviye
    top = small.render(player_text + "   |   Seviye " + str(game.level + 1), True, DIM_TEXT)
    screen.blit(top, (16, 8))

    # alt satır: puan, süre, kalan yemek, enerji
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
        screen.blit(img, (x, 36))
        x += img.get_width() + 26


def draw_message(screen, font, lines, width, height):
    # ortada kutu içinde bir veya birkaç satır yazı
    if isinstance(lines, str):
        lines = [lines]
    imgs = [font.render(t, True, TEXT_COLOR) for t in lines]
    box_w = max(img.get_width() for img in imgs) + 40
    box_h = sum(img.get_height() + 6 for img in imgs) + 24
    box = pygame.Rect(0, 0, box_w, box_h)
    box.center = (width // 2, height // 2)
    pygame.draw.rect(screen, HUD_COLOR, box, border_radius=8)
    pygame.draw.rect(screen, WALL_COLOR, box, 2, border_radius=8)
    y = box.top + 12
    for img in imgs:
        screen.blit(img, img.get_rect(midtop=(width // 2, y)))
        y += img.get_height() + 6


def draw_center(screen, font, text, y, color, width):
    img = font.render(text, True, color)
    screen.blit(img, img.get_rect(midtop=(width // 2, y)))


def draw_menu(screen, big, font, small, width, height, level, level_count, first):
    screen.fill(BLACK)
    draw_center(screen, big, "PACMAN", 60, HIGHLIGHT, width)
    draw_center(screen, small, "İnsan ve utility-based AI ajanı sırayla aynı haritada oynar", 120, DIM_TEXT, width)

    y = 180
    draw_center(screen, font, "Seviye seç (1-" + str(level_count) + " veya ←/→)", y, TEXT_COLOR, width)
    y += 40
    x = width // 2 - (level_count * 70) // 2
    for i in range(level_count):
        rect = pygame.Rect(x + i * 70, y, 56, 40)
        if i == level:
            pygame.draw.rect(screen, HIGHLIGHT, rect, border_radius=6)
            color = BLACK
        else:
            pygame.draw.rect(screen, WALL_COLOR, rect, 2, border_radius=6)
            color = TEXT_COLOR
        img = font.render(str(i + 1), True, color)
        screen.blit(img, img.get_rect(center=rect.center))

    y += 80
    draw_center(screen, font, "Önce kim oynasın? (H: İnsan, A: AI)", y, TEXT_COLOR, width)
    y += 40
    options = ["İnsan", "AI"]
    for i in range(2):
        rect = pygame.Rect(width // 2 - 150 + i * 160, y, 140, 40)
        if options[i] == first:
            pygame.draw.rect(screen, HIGHLIGHT, rect, border_radius=6)
            color = BLACK
        else:
            pygame.draw.rect(screen, WALL_COLOR, rect, 2, border_radius=6)
            color = TEXT_COLOR
        img = font.render(options[i], True, color)
        screen.blit(img, img.get_rect(center=rect.center))

    y += 90
    draw_center(screen, font, "ENTER: başla", y, HIGHLIGHT, width)
    y += 50
    draw_center(screen, small, "İnsan: ok tuşları veya WASD   |   ESC: çıkış", y, DIM_TEXT, width)
    y += 26
    draw_center(screen, small, "Yemek +" + str(FOOD_SCORE) + "   Enerji topu +" + str(PELLET_SCORE) +
                "   Hayalet +" + str(GHOST_SCORE) + "   Her hareket " + str(MOVE_COST), y, DIM_TEXT, width)


def draw_results(screen, big, font, small, width, height, results, winner, reason, level):
    screen.fill(BLACK)
    draw_center(screen, big, "SONUÇLAR", 24, HIGHLIGHT, width)
    draw_center(screen, small, "Seviye " + str(level + 1), 80, DIM_TEXT, width)

    # tablo
    rows = [
        ("", results[0]["name"], results[1]["name"]),
        ("Durum", status_text(results[0]), status_text(results[1])),
        ("Puan", str(results[0]["score"]), str(results[1]["score"])),
        ("Süre", str(results[0]["time"]) + " sn", str(results[1]["time"]) + " sn"),
        ("Hamle", str(results[0]["steps"]), str(results[1]["steps"])),
        ("Kalan yemek", str(results[0]["food_left"]), str(results[1]["food_left"])),
    ]
    cols = [width // 2 - 200, width // 2 + 10, width // 2 + 180]
    y = 120
    for i in range(len(rows)):
        for j in range(3):
            if i == 0:
                color = HIGHLIGHT
            elif j == 0:
                color = DIM_TEXT
            else:
                color = TEXT_COLOR
            img = font.render(rows[i][j], True, color)
            if j == 0:
                screen.blit(img, (cols[0], y))
            else:
                screen.blit(img, img.get_rect(midtop=(cols[j], y)))
        y += 34

    y += 16
    if winner is None:
        draw_center(screen, big, "BERABERE", y, HIGHLIGHT, width)
    else:
        draw_center(screen, big, "Kazanan: " + winner["name"], y, WIN_COLOR, width)
    draw_center(screen, small, "(" + reason + ")", y + 56, DIM_TEXT, width)
    draw_center(screen, small, "Sıralama: önce tamamlama, sonra puan, eşitlikte kısa süre", y + 80, DIM_TEXT, width)
    draw_center(screen, font, "ENTER: menüye dön   |   ESC: çıkış", height - 40, TEXT_COLOR, width)


def status_text(result):
    if result["completed"]:
        return "Tamamladı"
    return "Yakalandı"
