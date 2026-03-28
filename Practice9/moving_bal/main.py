# main.py  —  Moving Ball Game
# Move the red ball with arrow keys.
# Ball cannot leave the screen.
# Press Escape or close window to quit.
#
# Run: python main.py

import sys
import pygame
from ball import Ball


# ── Constants ────────────────────────────────────────────────────────────────
WIDTH, HEIGHT = 600, 500
FPS           = 60
BG_COLOR      = (245, 245, 250)
GRID_COLOR    = (225, 225, 235)
TEXT_COLOR    = (80,  80,  100)


# ── Helpers ───────────────────────────────────────────────────────────────────

def draw_grid(surf):
    """Light grid for visual reference."""
    for x in range(0, WIDTH, 40):
        pygame.draw.line(surf, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, 40):
        pygame.draw.line(surf, GRID_COLOR, (0, y), (WIDTH, y))


def draw_hud(surf, font, ball: Ball):
    pos_text = f"Position: ({ball.x}, {ball.y})"
    label = font.render(pos_text, True, TEXT_COLOR)
    surf.blit(label, (10, 10))

    hint = "Arrow keys to move  |  ESC to quit"
    hint_surf = font.render(hint, True, TEXT_COLOR)
    surf.blit(hint_surf, (10, HEIGHT - 28))


# ── Main loop ─────────────────────────────────────────────────────────────────

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Moving Ball")
    clock  = pygame.time.Clock()
    font   = pygame.font.SysFont("Arial", 16)

    ball   = Ball(WIDTH, HEIGHT)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_UP:
                    ball.move_up()
                elif event.key == pygame.K_DOWN:
                    ball.move_down()
                elif event.key == pygame.K_LEFT:
                    ball.move_left()
                elif event.key == pygame.K_RIGHT:
                    ball.move_right()

        # ── Render ───────────────────────────────────────────────────────
        screen.fill(BG_COLOR)
        draw_grid(screen)
        ball.draw(screen)
        draw_hud(screen, font, ball)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
