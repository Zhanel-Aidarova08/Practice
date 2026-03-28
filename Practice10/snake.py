# main.py — Snake Game (Practice 10)
# Features: wall collision, random food (not on snake/wall), levels,
#           speed increase per level, score & level counter, comments
#
# Run: python main.py
# Requires: pip install pygame

import sys
import random
import pygame

# ── Initialise ────────────────────────────────────────────────────────────────
pygame.init()

# ── Grid / window constants ───────────────────────────────────────────────────
CELL        = 20          # pixel size of one grid cell
COLS        = 30          # grid columns
ROWS        = 28          # grid rows
PANEL_H     = 60          # height of HUD panel above the grid
WIDTH       = COLS * CELL
HEIGHT      = ROWS * CELL + PANEL_H
screen      = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

# ── Colours ───────────────────────────────────────────────────────────────────
BLACK      = (0,   0,   0)
WHITE      = (255, 255, 255)
BG_COLOR   = (15,  15,  25)
GRID_COLOR = (25,  25,  40)
WALL_COLOR = (80,  80,  120)
SNAKE_HEAD = (50,  220, 80)
SNAKE_BODY = (30,  170, 60)
FOOD_COLOR = (220, 50,  50)
FOOD_GLOW  = (255, 120, 80)
PANEL_BG   = (20,  20,  35)
TEXT_COLOR = (200, 200, 220)
GOLD       = (255, 210, 0)
LEVEL_COLS = [(50, 220, 80), (80, 180, 255), (220, 100, 255),
              (255, 160, 30), (255, 60,  60)]

# ── Fonts ─────────────────────────────────────────────────────────────────────
font_sm  = pygame.font.SysFont("Arial", 16, bold=True)
font_md  = pygame.font.SysFont("Arial", 22, bold=True)
font_lg  = pygame.font.SysFont("Arial", 42, bold=True)

# ── Directions ────────────────────────────────────────────────────────────────
UP    = ( 0, -1)
DOWN  = ( 0,  1)
LEFT  = (-1,  0)
RIGHT = ( 1,  0)

# ── Level config ──────────────────────────────────────────────────────────────
FOOD_PER_LEVEL = 3     # foods needed to advance a level
BASE_SPEED     = 8     # FPS at level 1
SPEED_STEP     = 2     # extra FPS per level
MAX_SPEED      = 25    # FPS cap


# ══════════════════════════════════════════════════════════════════════════════
#  WALL GENERATION
# ══════════════════════════════════════════════════════════════════════════════

def build_walls(level: int) -> set:
    """
    Return a set of (col, row) wall cells.
    Level 1 = border only.
    Higher levels add inner obstacles.
    """
    walls = set()

    # Border wall (always present)
    for c in range(COLS):
        walls.add((c, 0))
        walls.add((c, ROWS - 1))
    for r in range(ROWS):
        walls.add((0, r))
        walls.add((COLS - 1, r))

    # Extra inner walls for levels 2+
    if level >= 2:
        for c in range(5, 10):
            walls.add((c, ROWS // 2))
        for c in range(COLS - 10, COLS - 5):
            walls.add((c, ROWS // 2))

    if level >= 3:
        for r in range(5, 12):
            walls.add((COLS // 2, r))

    if level >= 4:
        for c in range(8, 14):
            walls.add((c, 8))
        for c in range(COLS - 14, COLS - 8):
            walls.add((c, ROWS - 9))

    return walls


# ══════════════════════════════════════════════════════════════════════════════
#  FOOD PLACEMENT
# ══════════════════════════════════════════════════════════════════════════════

def random_food(snake: list, walls: set) -> tuple:
    """
    Pick a random cell that is NOT occupied by the snake or a wall.
    Guaranteed to find a spot because the grid is much larger than the snake.
    """
    occupied = set(snake) | walls
    while True:
        pos = (random.randint(1, COLS - 2), random.randint(1, ROWS - 2))
        if pos not in occupied:
            return pos


# ══════════════════════════════════════════════════════════════════════════════
#  DRAWING
# ══════════════════════════════════════════════════════════════════════════════

def cell_rect(col, row):
    """Convert grid coordinates to pixel Rect (offset by PANEL_H)."""
    return pygame.Rect(col * CELL, row * CELL + PANEL_H, CELL, CELL)


def draw_grid(surf):
    """Faint grid lines for visual reference."""
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(surf, GRID_COLOR,
                             cell_rect(c, r), 1)


def draw_walls(surf, walls):
    """Draw each wall cell as a filled rectangle with a border."""
    for (c, r) in walls:
        rect = cell_rect(c, r)
        pygame.draw.rect(surf, WALL_COLOR, rect)
        pygame.draw.rect(surf, (110, 110, 160), rect, 1)


def draw_snake(surf, snake, level):
    """Draw snake body segments; head is brighter."""
    body_color = LEVEL_COLS[(level - 1) % len(LEVEL_COLS)]
    head_color = tuple(min(255, v + 60) for v in body_color)

    for i, (c, r) in enumerate(snake):
        color = head_color if i == 0 else body_color
        rect  = cell_rect(c, r).inflate(-2, -2)
        pygame.draw.rect(surf, color, rect, border_radius=4)

        # Eyes on the head
        if i == 0:
            pygame.draw.circle(surf, BLACK,
                               (c * CELL + 6,  r * CELL + PANEL_H + 6), 3)
            pygame.draw.circle(surf, BLACK,
                               (c * CELL + 14, r * CELL + PANEL_H + 6), 3)


def draw_food(surf, food):
    """Draw food as a glowing circle."""
    c, r  = food
    cx    = c * CELL + CELL // 2
    cy    = r * CELL + PANEL_H + CELL // 2
    pygame.draw.circle(surf, FOOD_GLOW, (cx, cy), CELL // 2 - 1)
    pygame.draw.circle(surf, FOOD_COLOR, (cx, cy), CELL // 2 - 3)


def draw_hud(surf, score, level, food_in_level):
    """Draw the top panel with score, level, and progress bar."""
    pygame.draw.rect(surf, PANEL_BG, (0, 0, WIDTH, PANEL_H))
    pygame.draw.line(surf, WALL_COLOR, (0, PANEL_H), (WIDTH, PANEL_H), 2)

    # Score
    sc_surf = font_md.render(f"Score: {score}", True, TEXT_COLOR)
    surf.blit(sc_surf, (12, 10))

    # Level
    lv_color = LEVEL_COLS[(level - 1) % len(LEVEL_COLS)]
    lv_surf  = font_md.render(f"Level: {level}", True, lv_color)
    surf.blit(lv_surf, (WIDTH // 2 - lv_surf.get_width() // 2, 10))

    # Food progress bar (foods eaten this level / FOOD_PER_LEVEL)
    bar_x, bar_y, bar_w, bar_h = WIDTH - 160, 10, 140, 18
    pygame.draw.rect(surf, GRID_COLOR, (bar_x, bar_y, bar_w, bar_h), border_radius=5)
    fill_w = int(bar_w * (food_in_level / FOOD_PER_LEVEL))
    if fill_w:
        pygame.draw.rect(surf, lv_color,
                         (bar_x, bar_y, fill_w, bar_h), border_radius=5)
    pygame.draw.rect(surf, WALL_COLOR, (bar_x, bar_y, bar_w, bar_h), 2, border_radius=5)

    prog_label = font_sm.render(
        f"{food_in_level}/{FOOD_PER_LEVEL}", True, TEXT_COLOR)
    surf.blit(prog_label, (bar_x + bar_w // 2 - prog_label.get_width() // 2,
                           bar_y + 1))


def draw_overlay(surf, title, lines):
    """Semi-transparent overlay for game-over / level-up messages."""
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 170))
    surf.blit(overlay, (0, 0))

    title_surf = font_lg.render(title, True, GOLD)
    surf.blit(title_surf, title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 70)))

    for i, line in enumerate(lines):
        ls = font_md.render(line, True, TEXT_COLOR)
        surf.blit(ls, ls.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 10 + i * 36)))


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN GAME LOOP
# ══════════════════════════════════════════════════════════════════════════════

def run_game():
    level         = 1
    score         = 0
    food_in_level = 0          # foods eaten in current level
    speed         = BASE_SPEED

    walls = build_walls(level)

    # Snake starts in the middle, 3 segments long, moving right
    start_col = COLS // 2
    start_row = ROWS // 2
    snake      = [(start_col, start_row),
                  (start_col - 1, start_row),
                  (start_col - 2, start_row)]
    direction  = RIGHT
    next_dir   = RIGHT

    food = random_food(snake, walls)

    game_over   = False
    level_up    = False
    clock       = pygame.time.Clock()

    while True:
        clock.tick(speed)

        # ── Events ────────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                # Restart
                if (game_over or level_up) and event.key == pygame.K_r:
                    return
                # Direction: prevent reversing
                if event.key == pygame.K_UP    and direction != DOWN:
                    next_dir = UP
                if event.key == pygame.K_DOWN  and direction != UP:
                    next_dir = DOWN
                if event.key == pygame.K_LEFT  and direction != RIGHT:
                    next_dir = LEFT
                if event.key == pygame.K_RIGHT and direction != LEFT:
                    next_dir = RIGHT

        if game_over or level_up:
            # Just redraw overlay and wait for R
            if game_over:
                draw_overlay(screen, "GAME OVER",
                             [f"Score: {score}  Level: {level}",
                              "Press R to restart"])
            else:
                draw_overlay(screen, f"LEVEL {level}!",
                             [f"Score: {score}",
                              "Press R to continue"])
            pygame.display.flip()
            continue

        # ── Move snake ─────────────────────────────────────────────────────────
        direction = next_dir
        head_c, head_r = snake[0]
        new_head = (head_c + direction[0], head_r + direction[1])

        # ── Wall collision ─────────────────────────────────────────────────────
        if new_head in walls:
            game_over = True
            continue

        # ── Self collision ─────────────────────────────────────────────────────
        if new_head in snake:
            game_over = True
            continue

        # Advance snake
        snake.insert(0, new_head)

        # ── Food collision ─────────────────────────────────────────────────────
        if new_head == food:
            score        += 10 * level    # higher levels = more points
            food_in_level += 1
            food = random_food(snake, walls)   # spawn new food (not on snake/wall)

            # ── Level up ──────────────────────────────────────────────────────
            if food_in_level >= FOOD_PER_LEVEL:
                level         += 1
                food_in_level  = 0
                speed          = min(BASE_SPEED + (level - 1) * SPEED_STEP, MAX_SPEED)
                walls          = build_walls(level)   # new walls for new level
                # Make sure food is not inside new walls
                food = random_food(snake, walls)
                level_up = True
                continue
        else:
            snake.pop()   # no food eaten — remove tail to keep length

        # ── Draw ──────────────────────────────────────────────────────────────
        screen.fill(BG_COLOR)
        draw_grid(screen)
        draw_walls(screen, walls)
        draw_food(screen, food)
        draw_snake(screen, snake, level)
        draw_hud(screen, score, level, food_in_level)
        pygame.display.flip()


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    while True:
        run_game()
