#oyun kuralları ve durum

from levels import LEVELS, parse_level, check_level
from settings import MOVE_COST, FOOD_SCORE, PELLET_SCORE, POWER_DURATION

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
 
    def step(self, direction):
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
 
        if self.food_left() == 0:
            self.completed = True
 
        return True
   