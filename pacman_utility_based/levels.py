# haritalar
# # duvar, . yemek, o enerji topu, P pacman, G hayalet

# kör çıkmaz koridorlar yoktu, hayalet orada sıkıştırıyordu o yüzden duvarları açtım
LEVEL_1 = [
    "#####################",
    "#o.................o#",
    "#.###.##.#.#.##.###.#",
    "#...................#",
    "#.###.#.#####.#.###.#",
    "#.....#...#...#.....#",
    "#.###.#.......#.###.#",
    "#.......#.G.G.#.....#",
    "#.###.#.......#.###.#",
    "#.....#...#...#.....#",
    "#.###.#.#####.#.###.#",
    "#.........P.........#",
    "#.###.##.#.#.##.###.#",
    "#o.................o#",
    "#####################",
]

LEVELS = [LEVEL_1]


def parse_level(rows):
    walls = set()
    food = set()
    pellets = set()
    ghosts = []
    pacman = None

    for r in range(len(rows)):
        for c in range(len(rows[r])):
            ch = rows[r][c]
            if ch == "#":
                walls.add((r, c))
            elif ch == ".":
                food.add((r, c))
            elif ch == "o":
                pellets.add((r, c))
            elif ch == "P":
                pacman = (r, c)
            elif ch == "G":
                ghosts.append((r, c))

    return walls, food, pellets, pacman, ghosts


def check_level(rows):
    # tüm yemeklere pacman'den ulaşılabiliyor mu bakıyoruz (BFS)
    walls, food, pellets, pacman, ghosts = parse_level(rows)

    if pacman is None:
        raise ValueError("haritada P yok")
    if len(ghosts) < 2:
        raise ValueError("en az 2 hayalet olmalı")

    visited = [pacman]
    queue = [pacman]
    while len(queue) > 0:
        r, c = queue.pop(0)
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nxt = (r + dr, c + dc)
            if nxt not in walls and nxt not in visited:
                visited.append(nxt)
                queue.append(nxt)

    for pos in food | pellets:
        if pos not in visited:
            raise ValueError("ulaşılamayan yemek: " + str(pos))