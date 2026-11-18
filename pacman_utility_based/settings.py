#sabitler (puanlar, süreler, renkler, hücre boyutu)

#puanlar
MOVE_COST = -1
FOOD_SCORE = 10
PELLET_SCORE = 50
GHOST_SCORE = 200

#enerji topu kaç hamle sürsün 
POWER_DURATION = 20

#hayaletler için sabit seed
SEED = 42

#hayaletler başta kaç hamle beklesin
GHOST_START_DELAY = 5

#takip eden hayaletin pacman'i kovalama olasılığı
CHASE_CHANCE = 0.7

FPS = 60
MOVE_DELAY = 150

CELL = 32
HUD_HEIGHT = 70

BLACK = (0, 0, 0)
WALL_COLOR = (33, 33, 222)
FOOD_COLOR = (255, 184, 174)
PELLET_COLOR = (255, 255, 255)
PACMAN_COLOR = (255, 235, 0)
GHOST_COLORS = [(255, 0, 0), (255, 184, 255), (0, 255, 255), (255, 184, 82)]
SCARED_COLOR = (100, 100, 100)
HUD_COLOR = (20, 20, 30)
TEXT_COLOR = (240, 240, 240)
DIM_TEXT = (150, 150, 170)
HIGHLIGHT = (255, 235, 0)
WIN_COLOR = (80, 220, 120)

#her oyuncu başlamadan önce geri sayım (ms)
COUNTDOWN = 3000