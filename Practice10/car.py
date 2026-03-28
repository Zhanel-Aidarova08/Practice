# main.py — Racer Game (Practice 10)
# Based on coderslegacy.com pygame tutorial
# Extra features: coins on road, coin counter, comments throughout
#
# Run: python main.py
# Requires: pip install pygame

import sys
import random
import pygame

# ── Initialise ────────────────────────────────────────────────────────────────
pygame.init()

# ── Window / display settings ─────────────────────────────────────────────────
WIDTH, HEIGHT = 400, 600
screen        = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")
clock         = pygame.time.Clock()
FPS           = 60

# ── Colours ───────────────────────────────────────────────────────────────────
BLACK   = (0,   0,   0)
WHITE   = (255, 255, 255)
GREY    = (50,  50,  50)
RED     = (200, 30,  30)
YELLOW  = (255, 220, 0)
GREEN   = (50,  200, 80)
ORANGE  = (255, 140, 0)
ROAD_C  = (60,  60,  60)
MARK_C  = (200, 200, 200)

# ── Fonts ─────────────────────────────────────────────────────────────────────
font_small  = pygame.font.SysFont("Arial", 18, bold=True)
font_medium = pygame.font.SysFont("Arial", 28, bold=True)
font_large  = pygame.font.SysFont("Arial", 48, bold=True)

# ── Road geometry ─────────────────────────────────────────────────────────────
ROAD_LEFT  = 60    # left edge of road
ROAD_RIGHT = 340   # right edge of road
ROAD_W     = ROAD_RIGHT - ROAD_LEFT
LANE_W     = ROAD_W // 3   # three lanes

# ── Game constants ────────────────────────────────────────────────────────────
PLAYER_SPEED  = 5    # horizontal pixels per frame
CAR_W, CAR_H  = 50, 90
COIN_R        = 12   # coin radius
ENEMY_SPAWN_Y = -CAR_H
COIN_SPAWN_Y  = -COIN_R * 2


# ══════════════════════════════════════════════════════════════════════════════
#  HELPER: draw a simple car using rectangles & circles (no image file needed)
# ══════════════════════════════════════════════════════════════════════════════

def draw_car(surf, x, y, color):
    """Draw a top-down car at (x, y) — x,y = top-left corner."""
    # Body
    pygame.draw.rect(surf, color,   (x + 5,  y,      CAR_W - 10, CAR_H))
    # Windshields
    pygame.draw.rect(surf, (150, 220, 255), (x + 8,  y + 8,  CAR_W - 16, 18))  # front
    pygame.draw.rect(surf, (150, 220, 255), (x + 8,  y + 62, CAR_W - 16, 16))  # rear
    # Wheels
    wheel_color = (20, 20, 20)
    for wx, wy in [(x, y + 10), (x + CAR_W - 10, y + 10),
                   (x, y + 65), (x + CAR_W - 10, y + 65)]:
        pygame.draw.rect(surf, wheel_color, (wx, wy, 10, 20), border_radius=3)
    # Headlights
    pygame.draw.circle(surf, YELLOW, (x + 12, y + 6), 5)
    pygame.draw.circle(surf, YELLOW, (x + CAR_W - 12, y + 6), 5)


# ══════════════════════════════════════════════════════════════════════════════
#  CLASSES
# ══════════════════════════════════════════════════════════════════════════════

class PlayerCar:
    """The car controlled by the player."""

    def __init__(self):
        # Start horizontally centred on the road
        self.x = ROAD_LEFT + ROAD_W // 2 - CAR_W // 2
        self.y = HEIGHT - CAR_H - 20
        self.rect = pygame.Rect(self.x, self.y, CAR_W, CAR_H)

    def move(self, keys):
        """Move left/right with arrow keys; clamp to road boundaries."""
        if keys[pygame.K_LEFT]:
            self.x = max(ROAD_LEFT, self.x - PLAYER_SPEED)
        if keys[pygame.K_RIGHT]:
            self.x = min(ROAD_RIGHT - CAR_W, self.x + PLAYER_SPEED)
        self.rect.topleft = (self.x, self.y)

    def draw(self, surf):
        draw_car(surf, self.x, self.y, GREEN)


class EnemyCar:
    """An oncoming enemy car that scrolls downward."""

    COLORS = [(200, 30, 30), (30, 80, 200), (180, 80, 200), (200, 130, 30)]

    def __init__(self, speed):
        # Pick a random lane (left / centre / right)
        lane = random.randint(0, 2)
        self.x = ROAD_LEFT + lane * LANE_W + (LANE_W - CAR_W) // 2
        self.y = ENEMY_SPAWN_Y
        self.speed = speed
        self.color = random.choice(self.COLORS)
        self.rect  = pygame.Rect(self.x, self.y, CAR_W, CAR_H)

    def update(self):
        """Scroll down by speed pixels each frame."""
        self.y    += self.speed
        self.rect.y = self.y

    def draw(self, surf):
        draw_car(surf, self.x, self.y, self.color)

    def off_screen(self):
        return self.y > HEIGHT


class Coin:
    """A golden coin that appears randomly on the road."""

    def __init__(self, speed):
        # Random horizontal position within road bounds (avoid edges)
        self.x = random.randint(ROAD_LEFT + COIN_R, ROAD_RIGHT - COIN_R)
        self.y = COIN_SPAWN_Y
        self.speed = speed
        self.rect  = pygame.Rect(self.x - COIN_R, self.y - COIN_R,
                                 COIN_R * 2, COIN_R * 2)

    def update(self):
        self.y    += self.speed
        self.rect.y = self.y - COIN_R

    def draw(self, surf):
        # Outer gold ring
        pygame.draw.circle(surf, ORANGE, (self.x, int(self.y)), COIN_R)
        # Inner highlight
        pygame.draw.circle(surf, YELLOW, (self.x, int(self.y)), COIN_R - 4)
        # "$" symbol
        label = font_small.render("$", True, ORANGE)
        surf.blit(label, label.get_rect(center=(self.x, int(self.y))))

    def off_screen(self):
        return self.y > HEIGHT


# ══════════════════════════════════════════════════════════════════════════════
#  ROAD DRAWING
# ══════════════════════════════════════════════════════════════════════════════

# Road markings: dashed white lines between lanes — stored as y offsets
mark_y_offsets = [i * 80 for i in range(10)]

def draw_road(surf, scroll_offset):
    """Draw road background, grass verges, and scrolling lane markings."""
    # Grass on both sides
    surf.fill((34, 139, 34))

    # Road surface
    pygame.draw.rect(surf, ROAD_C, (ROAD_LEFT, 0, ROAD_W, HEIGHT))

    # Kerb strips (red/white alternating)
    for i in range(0, HEIGHT, 20):
        color = RED if (i // 20) % 2 == 0 else WHITE
        pygame.draw.rect(surf, color, (ROAD_LEFT - 10, i, 10, 20))
        pygame.draw.rect(surf, color, (ROAD_RIGHT,      i, 10, 20))

    # Scrolling lane dashes
    for offset in mark_y_offsets:
        y = (offset + scroll_offset) % HEIGHT
        # Two dividers (between lane 0-1 and lane 1-2)
        for lane_x in [ROAD_LEFT + LANE_W, ROAD_LEFT + LANE_W * 2]:
            pygame.draw.rect(surf, MARK_C, (lane_x - 2, y, 4, 40))


# ══════════════════════════════════════════════════════════════════════════════
#  HUD
# ══════════════════════════════════════════════════════════════════════════════

def draw_hud(surf, score, coins):
    """Display score (top-left) and coin count (top-right)."""
    # Score
    score_surf = font_small.render(f"Score: {score}", True, WHITE)
    surf.blit(score_surf, (ROAD_LEFT + 5, 8))

    # Coin count — top-right corner
    coin_surf = font_small.render(f"Coins: {coins}", True, YELLOW)
    surf.blit(coin_surf, (WIDTH - coin_surf.get_width() - 10, 8))

    # Coin icon next to counter
    pygame.draw.circle(surf, ORANGE, (WIDTH - coin_surf.get_width() - 22, 17), 8)
    pygame.draw.circle(surf, YELLOW, (WIDTH - coin_surf.get_width() - 22, 17), 5)


def draw_game_over(surf, score, coins):
    """Overlay game-over screen."""
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    surf.blit(overlay, (0, 0))

    go   = font_large.render("GAME OVER", True, RED)
    sc   = font_medium.render(f"Score: {score}", True, WHITE)
    co   = font_medium.render(f"Coins: {coins}", True, YELLOW)
    rest = font_small.render("Press R to restart  |  Q to quit", True, WHITE)

    surf.blit(go,   go.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80)))
    surf.blit(sc,   sc.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
    surf.blit(co,   co.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)))
    surf.blit(rest, rest.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70)))


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN GAME LOOP
# ══════════════════════════════════════════════════════════════════════════════

def run_game():
    player        = PlayerCar()
    enemies       = []
    coins         = []

    score         = 0        # frames survived (converted to points)
    coin_count    = 0        # collected coins
    game_over     = False

    scroll_offset = 0        # road marking scroll position
    enemy_speed   = 4        # enemy cars start at speed 4
    coin_speed    = 3

    # Timers for spawning (in milliseconds)
    last_enemy_spawn = pygame.time.get_ticks()
    last_coin_spawn  = pygame.time.get_ticks()
    ENEMY_INTERVAL   = 1200  # ms between enemy spawns
    COIN_INTERVAL    = 2000  # ms between coin spawns

    while True:
        dt  = clock.tick(FPS)
        now = pygame.time.get_ticks()

        # ── Events ───────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit(); sys.exit()
                if game_over and event.key == pygame.K_r:
                    return   # restart by re-calling run_game()

        if game_over:
            draw_game_over(screen, score, coin_count)
            pygame.display.flip()
            continue

        # ── Input ────────────────────────────────────────────────────────────
        keys = pygame.key.get_pressed()
        player.move(keys)

        # ── Spawn enemies ─────────────────────────────────────────────────────
        if now - last_enemy_spawn > ENEMY_INTERVAL:
            enemies.append(EnemyCar(enemy_speed))
            last_enemy_spawn = now

        # ── Spawn coins ───────────────────────────────────────────────────────
        if now - last_coin_spawn > COIN_INTERVAL:
            coins.append(Coin(coin_speed))
            last_coin_spawn = now

        # ── Update objects ────────────────────────────────────────────────────
        scroll_offset = (scroll_offset + enemy_speed) % HEIGHT

        for enemy in enemies:
            enemy.update()
        enemies = [e for e in enemies if not e.off_screen()]

        for coin in coins:
            coin.update()
        coins = [c for c in coins if not c.off_screen()]

        # ── Collision: player vs enemy ────────────────────────────────────────
        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                game_over = True

        # ── Collision: player vs coin ─────────────────────────────────────────
        remaining_coins = []
        for coin in coins:
            if player.rect.colliderect(coin.rect):
                coin_count += 1   # collect coin
            else:
                remaining_coins.append(coin)
        coins = remaining_coins

        # ── Score & difficulty ────────────────────────────────────────────────
        score += 1
        # Every 500 points increase speed slightly
        if score % 500 == 0:
            enemy_speed = min(enemy_speed + 1, 12)
            coin_speed  = min(coin_speed  + 1, 10)
            ENEMY_INTERVAL = max(600, ENEMY_INTERVAL - 50)

        # ── Draw ──────────────────────────────────────────────────────────────
        draw_road(screen, scroll_offset)

        for enemy in enemies:
            enemy.draw(screen)
        for coin in coins:
            coin.draw(screen)

        player.draw(screen)
        draw_hud(screen, score, coin_count)

        pygame.display.flip()


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    while True:
        run_game()
