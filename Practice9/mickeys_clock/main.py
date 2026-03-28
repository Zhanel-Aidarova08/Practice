# main.py  —  Mickey's Clock
# Shows a clock face inspired by the Mickey Mouse clock.
# Mickey's RIGHT hand = minutes, LEFT hand = seconds.
# Since we don't ship a real Mickey image, we draw hands as
# white-gloved Mickey-style hands using pygame drawing primitives.
#
# Run: python main.py
# Requires: pip install pygame

import sys
import math
import datetime
import pygame
from Practice.Practice9.mickeys_clock.clock import get_time, seconds_angle, minutes_angle


# ── Constants ────────────────────────────────────────────────────────────────
WIDTH, HEIGHT   = 500, 500
FPS             = 30
CENTER          = (WIDTH // 2, HEIGHT // 2)
CLOCK_RADIUS    = 190
HAND_MIN_LEN    = 150   # minutes hand length
HAND_SEC_LEN    = 170   # seconds hand length

# Colour palette matching the reference image
BG_COLOR        = (245, 230, 180)   # warm cream
FACE_COLOR      = (245, 230, 180)
RAY_COLOR       = (255, 240, 200)
RIM_COLOR       = (200, 200, 205)
TICK_COLOR      = (80,  80,  90)
NUM_COLOR       = (40,  40,  50)
BODY_RED        = (200, 30,  30)
MICKEY_BLACK    = (20,  20,  20)
GLOVE_WHITE     = (255, 255, 255)
HAND_OUTLINE    = (30,  30,  30)
MIN_HAND_COLOR  = (240, 240, 240)   # right hand (minutes) — white glove
SEC_HAND_COLOR  = (240, 80,  60)    # left hand  (seconds) — red accent


# ── Drawing helpers ───────────────────────────────────────────────────────────

def angle_to_vec(angle_deg: float, length: float):
    """Convert clock angle (0=up, CW) to (dx, dy) vector."""
    rad = math.radians(angle_deg - 90)
    return math.cos(rad) * length, math.sin(rad) * length


def draw_sunrays(surf):
    cx, cy = CENTER
    for i in range(60):
        angle = math.radians(i * 6)
        x1 = cx + math.cos(angle) * 30
        y1 = cy + math.sin(angle) * 30
        x2 = cx + math.cos(angle) * CLOCK_RADIUS
        y2 = cy + math.sin(angle) * CLOCK_RADIUS
        pygame.draw.line(surf, RAY_COLOR, (x1, y1), (x2, y2), 1)


def draw_ticks(surf, font_small, font_large):
    cx, cy = CENTER
    for i in range(60):
        angle = math.radians(i * 6 - 90)
        if i % 5 == 0:
            # Hour tick + number
            x1 = cx + math.cos(angle) * (CLOCK_RADIUS - 5)
            y1 = cy + math.sin(angle) * (CLOCK_RADIUS - 5)
            x2 = cx + math.cos(angle) * (CLOCK_RADIUS - 20)
            y2 = cy + math.sin(angle) * (CLOCK_RADIUS - 20)
            pygame.draw.line(surf, TICK_COLOR, (int(x1), int(y1)), (int(x2), int(y2)), 3)

            hour = i // 5
            if hour == 0:
                hour = 12
            label = font_large.render(str(hour), True, NUM_COLOR)
            nx = cx + math.cos(angle) * (CLOCK_RADIUS - 42)
            ny = cy + math.sin(angle) * (CLOCK_RADIUS - 42)
            surf.blit(label, label.get_rect(center=(int(nx), int(ny))))
        else:
            x1 = cx + math.cos(angle) * (CLOCK_RADIUS - 5)
            y1 = cy + math.sin(angle) * (CLOCK_RADIUS - 5)
            x2 = cx + math.cos(angle) * (CLOCK_RADIUS - 13)
            y2 = cy + math.sin(angle) * (CLOCK_RADIUS - 13)
            pygame.draw.line(surf, TICK_COLOR, (int(x1), int(y1)), (int(x2), int(y2)), 1)


def draw_mickey_body(surf):
    """Draw a simplified Mickey silhouette in the centre."""
    cx, cy = CENTER

    # ── Ears ────────────────────────────────────────────────────────────────
    pygame.draw.circle(surf, MICKEY_BLACK, (cx - 38, cy - 78), 30)
    pygame.draw.circle(surf, MICKEY_BLACK, (cx + 38, cy - 78), 30)

    # ── Head ────────────────────────────────────────────────────────────────
    pygame.draw.circle(surf, MICKEY_BLACK, (cx, cy - 55), 42)

    # ── Eyes ────────────────────────────────────────────────────────────────
    pygame.draw.ellipse(surf, GLOVE_WHITE, (cx - 20, cy - 70, 16, 18))
    pygame.draw.ellipse(surf, GLOVE_WHITE, (cx + 4,  cy - 70, 16, 18))
    pygame.draw.circle(surf, MICKEY_BLACK, (cx - 13, cy - 63), 5)
    pygame.draw.circle(surf, MICKEY_BLACK, (cx + 11, cy - 63), 5)

    # ── Nose & mouth ────────────────────────────────────────────────────────
    pygame.draw.ellipse(surf, MICKEY_BLACK, (cx - 10, cy - 47, 20, 12))
    pygame.draw.arc(surf, MICKEY_BLACK, (cx - 15, cy - 42, 30, 18),
                    math.pi, 2 * math.pi, 3)

    # ── Body (red shorts) ───────────────────────────────────────────────────
    pygame.draw.ellipse(surf, MICKEY_BLACK, (cx - 28, cy - 15, 56, 50))
    pygame.draw.ellipse(surf, BODY_RED,     (cx - 26, cy - 5,  52, 45))

    # ── Buttons ─────────────────────────────────────────────────────────────
    pygame.draw.circle(surf, GLOVE_WHITE, (cx, cy + 8),  4)
    pygame.draw.circle(surf, GLOVE_WHITE, (cx, cy + 20), 4)

    # ── Legs ────────────────────────────────────────────────────────────────
    pygame.draw.rect(surf, MICKEY_BLACK, (cx - 22, cy + 35, 14, 30), border_radius=4)
    pygame.draw.rect(surf, MICKEY_BLACK, (cx + 8,  cy + 35, 14, 30), border_radius=4)

    # ── Shoes ───────────────────────────────────────────────────────────────
    pygame.draw.ellipse(surf, MICKEY_BLACK, (cx - 32, cy + 60, 30, 16))
    pygame.draw.ellipse(surf, MICKEY_BLACK, (cx + 4,  cy + 60, 30, 16))


def draw_glove_hand(surf, cx, cy, angle_deg, length, color, outline):
    """Draw a Mickey-style gloved arm as a rounded hand pointer."""
    rad   = math.radians(angle_deg - 90)
    tip_x = cx + math.cos(rad) * length
    tip_y = cy + math.sin(rad) * length

    # Arm line (thick)
    pygame.draw.line(surf, outline, (cx, cy), (int(tip_x), int(tip_y)), 10)
    pygame.draw.line(surf, color,   (cx, cy), (int(tip_x), int(tip_y)), 6)

    # Glove circle at tip
    pygame.draw.circle(surf, outline, (int(tip_x), int(tip_y)), 14)
    pygame.draw.circle(surf, color,   (int(tip_x), int(tip_y)), 11)

    # Finger bumps
    for offset in (-20, 0, 20):
        bump_rad = math.radians(angle_deg - 90 + offset)
        bx = tip_x + math.cos(bump_rad) * 10
        by = tip_y + math.sin(bump_rad) * 10
        pygame.draw.circle(surf, color, (int(bx), int(by)), 7)


def draw_digital_time(surf, font, minutes, seconds):
    """Show MM:SS in the lower portion of the clock."""
    text = f"{minutes:02d}:{seconds:02d}"
    label = font.render(text, True, MICKEY_BLACK)
    cx, cy = CENTER
    surf.blit(label, label.get_rect(center=(cx, cy + 105)))


# ── Main loop ────────────────────────────────────────────────────────────────

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mickey's Clock")
    clock  = pygame.time.Clock()

    font_large   = pygame.font.SysFont("Arial", 22, bold=True)
    font_digital = pygame.font.SysFont("Courier", 28, bold=True)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        minutes, seconds = get_time()
        min_angle = -(minutes_angle(minutes, seconds))   # negate: pygame rotates CCW
        sec_angle = -(seconds_angle(seconds))

        # Convert back to CW degrees for our draw helper
        min_draw = minutes_angle(minutes, seconds) * -1   # already CW
        sec_draw = seconds_angle(seconds) * -1

        # ── Background & rim ─────────────────────────────────────────────
        screen.fill((230, 230, 235))
        pygame.draw.circle(screen, RIM_COLOR,  CENTER, CLOCK_RADIUS + 18)
        pygame.draw.circle(screen, FACE_COLOR, CENTER, CLOCK_RADIUS)

        draw_sunrays(screen)
        draw_ticks(screen, font_large, font_large)

        # ── Mickey body ──────────────────────────────────────────────────
        draw_mickey_body(screen)

        # ── Hands (draw before body centre dot) ─────────────────────────
        cx, cy = CENTER
        # Minutes hand — right arm — white glove
        draw_glove_hand(screen, cx, cy - 10, min_draw, HAND_MIN_LEN,
                        MIN_HAND_COLOR, HAND_OUTLINE)
        # Seconds hand — left arm — red
        draw_glove_hand(screen, cx, cy - 10, sec_draw, HAND_SEC_LEN,
                        SEC_HAND_COLOR, HAND_OUTLINE)

        # Centre pivot
        pygame.draw.circle(screen, MICKEY_BLACK, (cx, cy - 10), 8)

        draw_digital_time(screen, font_digital, minutes, seconds)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
