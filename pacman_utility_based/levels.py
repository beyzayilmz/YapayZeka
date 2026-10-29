#haritalar ve doğrulama

from collections import deque

LEVEL_1 = [
    "#####################",
    "#o.......#.#.......o#",
    "#.###.##.#.#.##.###.#",
    "#...................#",
    "#.###.#.#####.#.###.#",
    "#.....#...#...#.....#",
    "#####.#.......#.#####",
    "#.......#.G.G.#.....#",
    "#####.#.......#.#####",
    "#.....#...#...#.....#",
    "#.###.#.#####.#.###.#",
    "#.........P.........#",
    "#.###.##.#.#.##.###.#",
    "#o.......#.#.......o#",
    "#####################",
]

LEVELS = [LEVEL_1]

WALKABLE = ".oPG "


def parse_level(rows):
    """Haritayı ayrıştırır; (duvarlar, yemekler, toplar, pacman, hayaletler) döner.

    Konumlar (satır, sütun) biçimindedir.
    """
    walls, food, pellets, ghosts = set(), set(), set(), []
    pacman = None
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
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


def validate_level(rows):
    """Tüm yemek ve enerji toplarının Pacman'den erişilebilir olduğunu doğrular."""
    widths = {len(r) for r in rows}
    if len(widths) != 1:
        raise ValueError("Harita satırları aynı uzunlukta değil")
    walls, food, pellets, pacman, ghosts = parse_level(rows)
    if pacman is None:
        raise ValueError("Haritada Pacman (P) yok")
    if len(ghosts) < 2:
        raise ValueError("En az iki hayalet (G) gerekli")

    seen = {pacman}
    queue = deque([pacman])
    while queue:
        r, c = queue.popleft()
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nxt = (r + dr, c + dc)
            if nxt in walls or nxt in seen:
                continue
            if not (0 <= nxt[0] < len(rows) and 0 <= nxt[1] < len(rows[0])):
                continue
            seen.add(nxt)
            queue.append(nxt)

    unreachable = (food | pellets) - seen
    if unreachable:
        raise ValueError(f"Erişilemeyen yemekler var: {sorted(unreachable)}")
    return True