#hayalet stratejileri
# 0. hayalet (ve çift sayılılar): pacman'i takip eder
# 1. hayalet (ve tek sayılılar): rastgele gezer

from settings import CHASE_CHANCE

DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def free_neighbors(game, pos):
    # bir hücrenin duvar olmayan komşuları
    result = []
    for dr, dc in DIRS:
        r = pos[0] + dr
        c = pos[1] + dc
        if r < 0 or r >= game.height or c < 0 or c >= game.width:
            continue
        if (r, c) not in game.walls:
            result.append((r, c))
    return result


def random_move(game, pos):
    options = free_neighbors(game, pos)
    return game.rng.choice(options)


def chase_move(game, pos):
    # BFS ile pacman'e giden en kısa yolun ilk adımını bul
    if pos == game.pacman:
        return pos

    came_from = {pos: None}
    queue = [pos]
    while len(queue) > 0:
        cur = queue.pop(0)
        if cur == game.pacman:
            break
        for nxt in free_neighbors(game, cur):
            if nxt not in came_from:
                came_from[nxt] = cur
                queue.append(nxt)

    if game.pacman not in came_from:
        return pos

    cur = game.pacman
    while came_from[cur] != pos:
        cur = came_from[cur]
    return cur


def move_ghosts(game):
    for i in range(len(game.ghosts)):
        # başlangıçta ve yakalanınca biraz bekliyorlar
        if game.ghost_wait[i] > 0:
            game.ghost_wait[i] -= 1
            continue

        pos = game.ghosts[i]
        if game.power > 0:
            # enerji varken korkup rastgele kaçıyorlar
            new_pos = random_move(game, pos)
        elif i % 2 == 0 and game.rng.random() < CHASE_CHANCE:
            new_pos = chase_move(game, pos)
        else:
            new_pos = random_move(game, pos)
        game.ghosts[i] = new_pos
