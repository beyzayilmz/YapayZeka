#oyun kuralları ve durum

import random

from levels import LEVELS, parse_level, check_level
from ghosts import move_ghosts
from settings import MOVE_COST, FOOD_SCORE, PELLET_SCORE, GHOST_SCORE, POWER_DURATION, GHOST_START_DELAY, SEED

DIRECTIONS = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1),
}

class Game:
    def __init__(self, level=0):
        rows = LEVELS[level]
        check_level(rows)
        self.level = level
        self.height = len(rows)
        self.width = len(rows[0])

        self.walls, self.food, self.pellets, self.pacman, self.ghosts = parse_level(rows)

        self.ghost_starts = list(self.ghosts)  # yakalanınca buraya dönerler
        self.ghost_wait = [GHOST_START_DELAY] * len(self.ghosts)
        self.rng = random.Random(SEED)  # sabit seed, iki turda aynı hareketler

        self.score = 0
        self.steps = 0
        self.power = 0 # 0 dan büyükse enerji etkisi var
        self.completed = False
        self.game_over = False

    def copy(self):
        #AI hamleleri denerken kullanacak
        g = Game.__new__(Game)
        g.level = self.level
        g.height = self.height
        g.width = self.width
        g.walls = self.walls
        g.food = set(self.food)
        g.pellets = set(self.pellets)
        g.pacman = self.pacman
        g.ghosts = list(self.ghosts)
        g.ghost_starts = self.ghost_starts
        g.ghost_wait = list(self.ghost_wait)
        g.rng = random.Random()
        g.rng.setstate(self.rng.getstate())
        g.score = self.score
        g.steps = self.steps
        g.power = self.power
        g.completed = self.completed
        g.game_over = self.game_over
        return g

    def food_left(self):
        return len(self.food) + len(self.pellets)
 
    def is_finished(self):
        return self.completed or self.game_over
 
    def can_move(self, direction):
        dr, dc = DIRECTIONS[direction]
        r = self.pacman[0] + dr
        c = self.pacman[1] + dc
        if r < 0 or r >= self.height or c < 0 or c >= self.width:
            return False
        return (r, c) not in self.walls
 
    def valid_moves(self):
        moves = []
        for d in DIRECTIONS:
            if self.can_move(d):
                moves.append(d)
        return moves
 
    def step(self, direction, ghosts_move=True):
        if self.is_finished() or not self.can_move(direction):
            return False
 
        if self.power > 0:
            self.power -= 1
 
        dr, dc = DIRECTIONS[direction]
        self.pacman = (self.pacman[0] + dr, self.pacman[1] + dc)
        self.steps += 1
        self.score += MOVE_COST
 
        if self.pacman in self.food:
            self.food.remove(self.pacman)
            self.score += FOOD_SCORE
        elif self.pacman in self.pellets:
            self.pellets.remove(self.pacman)
            self.score += PELLET_SCORE
            self.power = POWER_DURATION
 
        # pacman hareket etti, hayaletle aynı hücrede mi?
        self.check_collision(self.pacman, list(self.ghosts))

        if not self.game_over and self.food_left() == 0:
            self.completed = True

        # hayaletler hareket etsin (AI denerken kapatılabilir)
        if ghosts_move and not self.is_finished():
            old_pacman = self.pacman
            old_ghosts = list(self.ghosts)
            move_ghosts(self)
            self.check_collision(old_pacman, old_ghosts)

        return True

    def check_collision(self, old_pacman, old_ghosts):
        for i in range(len(self.ghosts)):
            same_cell = self.ghosts[i] == self.pacman
            # yer değiştirip yanından geçerlerse de çarpmış sayılır
            swapped = self.ghosts[i] == old_pacman and old_ghosts[i] == self.pacman
            if same_cell or swapped:
                if self.power > 0:
                    self.score += GHOST_SCORE
                    self.ghosts[i] = self.ghost_starts[i]
                    self.ghost_wait[i] = GHOST_START_DELAY
                else:
                    self.game_over = True
