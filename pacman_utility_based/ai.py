#utility based ajanı

# mantık şöyle: pacman her hamlede gidebileceği yönlerin hepsini oyunun kopyasında deniyor,
# denedikten sonra ortaya çıkan duruma bir fayda puanı veriyoruz, en yüksek puanlı yöne gidiyor
#
# fayda puanı şunlardan oluşuyor:
# 1. oyun puanı (yemek, enerji topu, hayalet yakalama artı / her hareket eksi)
# 2. en yakın yemeğe uzaklık, ne kadar yakınsa o kadar iyi
# 3. hayalet riski, enerji yokken hayalet yakınsa puan düşüyor
# 4. güvenli alan, pacman'in hayaletten önce ulaşabildiği hücre sayısı. çıkmaz sokağa
#    girince hayalet çıkışı kapatıyor ve bu sayı çok düşüyor, ilk başta sürekli oraya
#    girip yakalanıyordu bu yüzden ekledim
# 5. enerji varsa ve hayalete yetişebiliyorsak hayalete gitmek iyi
# 6. hayalet yakınsa enerji topuna gitmek iyi (hayaletten kurtulmak için)
# 7. yeni gittiği yerlere tekrar gitmesin diye ceza (yoksa ileri geri gidip duruyor)
# 8. sabır: uzun süre yemek yiyemezse (hayalet yüzünden bekliyorsa) tehlike ve güvenli alan
#    cezalarının etkisi yavaş yavaş azalıyor, yani risk almaya başlıyor. bunu eklemeden
#    son yemekler köşede kalınca sürekli bekleyip duruyordu
# oyun biterse +10000, hayalete yakalanırsa -10000

from ghosts import free_neighbors, chase_move
from settings import PELLET_SCORE

# ağırlıklar, denemelerle ayarladım
W_FOOD_DIST = 2       # yemeğe 1 adım yaklaşmak 2 puan
W_DANGER = 8          # tehlike cezası çarpanı
DANGER_RADIUS = 5     # hayalet 5 adımdan yakınsa tehlike say
W_SAFE = 20           # güvenli alan küçükse ceza çarpanı
SAFE_MIN = 15         # güvenli alan bundan küçükse ceza başlar
W_HUNT = 60           # enerji varken hayalete yaklaşma puanı
W_PELLET = 30         # hayalet yakınken enerji topuna yaklaşma puanı
PELLET_ALERT = 8      # hayalet 8 adımdan yakınsa enerji topu önemli olsun
W_REVISIT = 6         # geri dönme cezası
RESERVE_PELLETS = True # enerji toplarını tehlike anı için sakla
STALL_LIMIT = 30      # bu kadar hamle yemek yemezse sabır azalmaya başlar
STALL_RAMP = 40       # sabır bu kadar hamlede en aza iner
MIN_FEAR = 0.1        # korku çarpanının en düşük değeri
RECENT_LEN = 8        # son kaç hamleyi hatırlasın
WIN_BONUS = 10000
LOSE_PENALTY = -10000


def bfs_distances(game, start):
    # start noktasından her hücreye kaç adımda gidilir (BFS)
    dist = {start: 0}
    queue = [start]
    while len(queue) > 0:
        cur = queue.pop(0)
        for nxt in free_neighbors(game, cur):
            if nxt not in dist:
                dist[nxt] = dist[cur] + 1
                queue.append(nxt)
    return dist


def safe_area(game, dist):
    # pacman'in hayaletlerden önce ulaşabildiği hücrelerin sayısı
    # önce her hücreye en erken hangi hayalet kaç adımda gelir onu buluyoruz
    ghost_time = {}
    for i in range(len(game.ghosts)):
        gd = bfs_distances(game, game.ghosts[i])
        for pos in gd:
            t = gd[pos] + game.ghost_wait[i]
            if pos not in ghost_time or t < ghost_time[pos]:
                ghost_time[pos] = t

    count = 0
    for pos in dist:
        if dist[pos] < ghost_time.get(pos, 999):
            count = count + 1
    return count


def utility(game, recent, pellet_total, fear):
    # oyun bitmişse direkt karar ver
    if game.game_over:
        return LOSE_PENALTY
    if game.completed:
        return WIN_BONUS + game.score

    dist = bfs_distances(game, game.pacman)

    # oyun puanı zaten hareket cezasını ve yemek puanlarını içeriyor
    u = game.score

    # enerji topunu boşuna yemesin, tehlike gelince lazım olacak diye saklıyoruz
    # o yüzden toplardan gelen 50 puanı burada saymıyorum (hayalet gelince güvenli alan
    # ve tehlike cezaları kalktığı için yine de yiyor)
    if RESERVE_PELLETS:
        eaten = pellet_total - len(game.pellets)
        u = u - PELLET_SCORE * eaten

    # en yakın yemeği bul (enerji toplarını da yemek sayıyorum, onlar da bitmeli)
    nearest_food = 999
    targets = game.food | game.pellets
    if RESERVE_PELLETS and len(game.food) > 0:
        targets = game.food   # normal yemek bitmeden toplara gitme
    for pos in targets:
        if pos in dist and dist[pos] < nearest_food:
            nearest_food = dist[pos]
    u = u - W_FOOD_DIST * nearest_food

    # hayaletlere bakıyoruz
    closest_ghost = 999
    for i in range(len(game.ghosts)):
        d = dist.get(game.ghosts[i], 999)
        d = d + game.ghost_wait[i]   # hala bekliyorsa geç gelir

        if game.power > d:
            # enerji bitmeden yetişebiliriz, hayalet artık av
            u = u + W_HUNT / (d + 1)
        else:
            if d < closest_ghost:
                closest_ghost = d
            if d <= DANGER_RADIUS:
                # hayalet yaklaştıkça ceza çok hızlı artsın diye kare aldım
                u = u - fear * W_DANGER * (DANGER_RADIUS - d + 1) * (DANGER_RADIUS - d + 1)

    # güvenli alan küçükse (çıkmaz sokak, köşeye sıkışma) ceza
    # enerji varken hayalet zararsız olduğu için bakmıyorum
    if game.power == 0:
        area = safe_area(game, dist)
        if area < SAFE_MIN:
            u = u - fear * W_SAFE * (SAFE_MIN - area)

    # hayalet yakında ve enerji yoksa enerji topuna doğru gitsin
    if game.power == 0 and closest_ghost <= PELLET_ALERT and len(game.pellets) > 0:
        nearest_pellet = 999
        for pos in game.pellets:
            if pos in dist and dist[pos] < nearest_pellet:
                nearest_pellet = dist[pos]
        u = u + W_PELLET / (nearest_pellet + 1)

    # son gittiği yerlere tekrar gitmesin
    u = u - W_REVISIT * recent.count(game.pacman)

    return u


def worst_case_ghosts(sim):
    # kopyada hayaletleri en kötü ihtimalle oynatıyoruz: hepsi pacman'e doğru 1 adım gelsin
    # (gerçekte biri rastgele ama temkinli olmak daha iyi)
    # enerji varsa hayaletler kaçıyor zaten, oynatmıyorum
    if sim.power > 0 or sim.is_finished():
        return
    old_pacman = sim.pacman
    old_ghosts = list(sim.ghosts)
    for i in range(len(sim.ghosts)):
        if sim.ghost_wait[i] > 0:
            sim.ghost_wait[i] -= 1
        else:
            sim.ghosts[i] = chase_move(sim, sim.ghosts[i])
    sim.check_collision(old_pacman, old_ghosts)


class Agent:
    def __init__(self):
        self.recent = []   # son gittiği hücreler
        self.pellet_total = None   # başta kaç enerji topu vardı
        self.stall = 0             # kaç hamledir yemek yemedi
        self.last_food = None

    def choose_move(self, game):
        if self.pellet_total is None:
            self.pellet_total = len(game.pellets)

        # yemek yiyebildi mi? yemediyse sabır azalıyor
        left = game.food_left()
        if self.last_food is not None and left < self.last_food:
            self.stall = 0
        else:
            self.stall = self.stall + 1
        self.last_food = left

        fear = 1.0
        if self.stall > STALL_LIMIT:
            fear = 1.0 - (self.stall - STALL_LIMIT) / STALL_RAMP
            if fear < MIN_FEAR:
                fear = MIN_FEAR

        best_move = None
        best_u = None

        for move in game.valid_moves():
            sim = game.copy()
            # hayaletlerin nereye gideceğini önceden bilemeyiz (rastgele),
            # o yüzden kopyada pacman'i oynatıp hayaletleri en kötü ihtimalle hareket ettiriyorum
            sim.step(move, ghosts_move=False)
            worst_case_ghosts(sim)
            u = utility(sim, self.recent, self.pellet_total, fear)

            if best_u is None or u > best_u:
                best_u = u
                best_move = move

        # bulunduğu yeri hatırla
        self.recent.append(game.pacman)
        if len(self.recent) > RECENT_LEN:
            self.recent.pop(0)

        return best_move
