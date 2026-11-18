#giriş noktası, ana döngü, ekran akışı
#
# ekranlar sırayla:
# menu      -> seviye ve ilk oyuncu seçilir
# countdown -> oyuncu başlamadan önce 3 sn geri sayım (süre henüz işlemiyor)
# play      -> oyun oynanıyor
# turn_over -> tur bitti, sonucu gösterip sıradaki oyuncuyu bekliyoruz
# results   -> iki oyuncunun sonucu ve kazanan
#
# ikinci oyuncu için Game sıfırdan oluşturuluyor, yani harita, başlangıç konumları,
# yemekler, enerji topları, ayarlar ve hayaletlerin rastgele sayı üreticisi (seed) aynı

import sys
import pygame

from game import Game
from ai import Agent
from levels import LEVELS
from results import make_result, find_winner
from render import draw_map, draw_hud, draw_message, draw_menu, draw_results
from settings import *

KEY_DIRS = {
    pygame.K_UP: "UP", pygame.K_w: "UP",
    pygame.K_DOWN: "DOWN", pygame.K_s: "DOWN",
    pygame.K_LEFT: "LEFT", pygame.K_a: "LEFT",
    pygame.K_RIGHT: "RIGHT", pygame.K_d: "RIGHT",
}


class App:
    def __init__(self):
        pygame.init()
        # pencere en büyük haritaya göre
        rows = max(len(lv) for lv in LEVELS)
        cols = max(len(lv[0]) for lv in LEVELS)
        self.width = cols * CELL
        self.height = HUD_HEIGHT + rows * CELL
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pacman")
        self.big = pygame.font.SysFont("arial", 44, bold=True)
        self.font = pygame.font.SysFont("arial", 22, bold=True)
        self.small = pygame.font.SysFont("arial", 16)
        self.clock = pygame.time.Clock()

        self.state = "menu"
        self.level = 0
        self.first = "İnsan"
        self.order = []      # oynama sırası, örn ["İnsan", "AI"]
        self.turn = 0        # sıradaki oyuncunun order içindeki indeksi
        self.results = []

    def current_player(self):
        return self.order[self.turn]

    def start_turn(self, now):
        # oyunu sıfırla, her oyuncu tamamen aynı başlangıç durumuyla oynasın
        self.game = Game(self.level)
        self.agent = Agent()
        self.direction = None
        self.wanted = None
        self.facing = "RIGHT"
        self.countdown_start = now
        self.state = "countdown"
        pygame.display.set_caption("Pacman - " + self.current_player())

    def elapsed(self, now):
        if self.state == "countdown":
            return 0
        if self.end_time is not None:
            return (self.end_time - self.start) / 1000
        return (now - self.start) / 1000

    def handle_key(self, key, now):
        if key == pygame.K_ESCAPE:
            return False

        if self.state == "menu":
            if pygame.K_1 <= key < pygame.K_1 + len(LEVELS):
                self.level = key - pygame.K_1
            elif key == pygame.K_LEFT:
                self.level = (self.level - 1) % len(LEVELS)
            elif key == pygame.K_RIGHT:
                self.level = (self.level + 1) % len(LEVELS)
            elif key == pygame.K_h:
                self.first = "İnsan"
            elif key == pygame.K_a:
                self.first = "AI"
            elif key in (pygame.K_UP, pygame.K_DOWN, pygame.K_TAB):
                self.first = "AI" if self.first == "İnsan" else "İnsan"
            elif key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                if self.first == "İnsan":
                    self.order = ["İnsan", "AI"]
                else:
                    self.order = ["AI", "İnsan"]
                self.turn = 0
                self.results = []
                self.start_turn(now)

        elif self.state in ("countdown", "play"):
            # yön tuşları sadece insan oynarken dikkate alınır
            if self.current_player() == "İnsan" and key in KEY_DIRS:
                self.wanted = KEY_DIRS[key]

        elif self.state == "turn_over":
            if key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                if self.turn == 0:
                    self.turn = 1
                    self.start_turn(now)
                else:
                    self.state = "results"
                    self.winner, self.reason = find_winner(self.results[0], self.results[1])
                    pygame.display.set_caption("Pacman - Sonuçlar")

        elif self.state == "results":
            if key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                self.state = "menu"
                pygame.display.set_caption("Pacman")

        return True

    def update(self, now):
        if self.state == "countdown":
            if now - self.countdown_start >= COUNTDOWN:
                self.state = "play"
                self.start = now
                self.last_move = now
                self.end_time = None
            return

        if self.state != "play":
            return

        # belli aralıklarla bir hamle yap (insan ve AI için aynı hız)
        if now - self.last_move < MOVE_DELAY:
            return
        self.last_move = now

        game = self.game
        if self.current_player() == "AI":
            move = self.agent.choose_move(game)
        else:
            # istenen yöne dönülebiliyorsa dön, yoksa eski yönde devam et
            if self.wanted is not None and game.can_move(self.wanted):
                self.direction = self.wanted
            move = self.direction

        if move is not None and game.can_move(move):
            game.step(move)
            self.facing = move

        if game.is_finished():
            self.end_time = now
            self.results.append(make_result(self.current_player(), game, self.elapsed(now)))
            self.state = "turn_over"

    def draw(self, now):
        screen = self.screen
        if self.state == "menu":
            draw_menu(screen, self.big, self.font, self.small, self.width, self.height,
                      self.level, len(LEVELS), self.first)
        elif self.state == "results":
            draw_results(screen, self.big, self.font, self.small, self.width, self.height,
                         self.results, self.winner, self.reason, self.level)
        else:
            screen.fill(BLACK)
            player_text = "Oynayan: " + self.current_player() + " (" + str(self.turn + 1) + ". oyuncu)"
            draw_hud(screen, self.font, self.small, self.game, self.elapsed(now), self.width, player_text)
            draw_map(screen, self.game, self.facing, now)

            if self.state == "countdown":
                left = (COUNTDOWN - (now - self.countdown_start)) // 1000 + 1
                lines = [self.current_player() + " oynuyor", "Başlıyor: " + str(left)]
                if self.current_player() == "İnsan":
                    lines.append("Ok tuşları / WASD ile yönlendir")
                draw_message(screen, self.font, lines, self.width, self.height)

            elif self.state == "turn_over":
                r = self.results[-1]
                if r["completed"]:
                    title = "Seviye tamamlandı!"
                else:
                    title = "Yakalandı! (game over)"
                if self.turn == 0:
                    nxt = "ENTER: sıra " + self.order[1] + "'da"
                else:
                    nxt = "ENTER: sonuçları göster"
                lines = [r["name"] + ": " + title,
                         "Puan: " + str(r["score"]) + "   Süre: " + str(r["time"]) + " sn",
                         nxt]
                draw_message(screen, self.font, lines, self.width, self.height)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            now = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    running = self.handle_key(event.key, now) and running
            self.update(now)
            self.draw(now)
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    App().run()
