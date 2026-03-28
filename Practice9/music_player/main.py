# main.py  —  Music Player with Keyboard Controller
# Controls:
#   P = Play / Pause toggle
#   S = Stop
#   N = Next track
#   B = Previous (Back)
#   Q / Escape = Quit
#
# Put your .mp3 / .wav / .ogg files into the music/ folder.
# Run: python main.py

import sys
import pygame
from player import MusicPlayer


# ── Constants ────────────────────────────────────────────────────────────────
WIDTH, HEIGHT = 520, 340
FPS           = 30
BG            = (18,  18,  28)
PANEL         = (28,  28,  45)
ACCENT        = (100, 180, 255)
TEXT_MAIN     = (230, 230, 240)
TEXT_DIM      = (110, 110, 140)
GREEN         = (80,  200, 120)
RED           = (220, 80,  80)
BAR_BG        = (50,  50,  70)
BAR_FG        = ACCENT


# ── UI helpers ────────────────────────────────────────────────────────────────

def draw_rounded_rect(surf, color, rect, radius=12):
    pygame.draw.rect(surf, color, rect, border_radius=radius)


def draw_progress_bar(surf, x, y, w, h, fraction, bg=BAR_BG, fg=BAR_FG):
    draw_rounded_rect(surf, bg, (x, y, w, h), 6)
    if fraction > 0:
        draw_rounded_rect(surf, fg, (x, y, int(w * fraction), h), 6)


def render(surf, fonts, player: MusicPlayer, elapsed: float):
    surf.fill(BG)

    f_title, f_track, f_status, f_hint = fonts

    # ── Player panel ─────────────────────────────────────────────────────────
    draw_rounded_rect(surf, PANEL, (30, 20, WIDTH - 60, HEIGHT - 40))

    # Title
    title = f_title.render("♫  Music Player", True, ACCENT)
    surf.blit(title, (60, 42))

    # Track name
    track_name = player.current_track_name()
    if len(track_name) > 40:
        track_name = track_name[:37] + "..."
    track_surf = f_track.render(track_name, True, TEXT_MAIN)
    surf.blit(track_surf, (60, 95))

    # Status
    status_color = GREEN if player.is_playing else RED
    status_surf  = f_status.render(player.status(), True, status_color)
    surf.blit(status_surf, (60, 135))

    # Elapsed time
    mins = int(elapsed) // 60
    secs = int(elapsed) % 60
    time_surf = f_status.render(f"Time: {mins:02d}:{secs:02d}", True, TEXT_DIM)
    surf.blit(time_surf, (60, 165))

    # Progress bar (visual only — pygame doesn't expose track length easily)
    frac = min((elapsed % 60) / 60, 1.0)   # loops every 60 s as visual demo
    draw_progress_bar(surf, 60, 200, WIDTH - 120, 10, frac)

    # Keyboard hints
    hints = [
        ("P", "Play/Pause"),
        ("S", "Stop"),
        ("N", "Next"),
        ("B", "Back"),
        ("Q", "Quit"),
    ]
    hx = 60
    for key, label in hints:
        k_surf = f_hint.render(f"[{key}]", True, ACCENT)
        l_surf = f_hint.render(label, True, TEXT_DIM)
        surf.blit(k_surf, (hx, 230))
        surf.blit(l_surf, (hx, 252))
        hx += 85

    pygame.display.flip()


# ── Main loop ─────────────────────────────────────────────────────────────────

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Music Player")
    clock  = pygame.time.Clock()

    fonts = (
        pygame.font.SysFont("Arial", 26, bold=True),   # title
        pygame.font.SysFont("Arial", 18),               # track
        pygame.font.SysFont("Arial", 16),               # status
        pygame.font.SysFont("Arial", 14),               # hints
    )

    player = MusicPlayer(music_dir="music")

    if not player.playlist:
        print("[INFO] No tracks found in music/ folder.")
        print("       Add .mp3 / .wav / .ogg files and restart.")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_p:
                    if not player.is_playing:
                        player.play()
                    else:
                        player.toggle_pause()
                elif event.key == pygame.K_s:
                    player.stop()
                elif event.key == pygame.K_n:
                    player.next_track()
                elif event.key == pygame.K_b:
                    player.prev_track()

        elapsed = player.position_sec() if player.is_playing else 0.0
        render(screen, fonts, player, elapsed)
        clock.tick(FPS)


if __name__ == "__main__":
    main()
