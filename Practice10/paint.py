# main.py — Paint Application (Practice 10)
# Based on nerdparadise.com/programming/pygame/part6
# Extra features: rectangle tool, circle tool, eraser, colour picker
#
# Run: python main.py
# Requires: pip install pygame

import sys
import math
import pygame

# ── Initialise ────────────────────────────────────────────────────────────────
pygame.init()

# ── Window ────────────────────────────────────────────────────────────────────
WIDTH, HEIGHT  = 900, 650
TOOLBAR_H      = 70          # height of top toolbar
CANVAS_TOP     = TOOLBAR_H   # canvas starts below toolbar
screen         = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
clock          = pygame.time.Clock()
FPS            = 60

# ── Colours ───────────────────────────────────────────────────────────────────
WHITE      = (255, 255, 255)
BLACK      = (0,   0,   0)
GREY       = (180, 180, 180)
DARK_GREY  = (60,  60,  60)
TOOLBAR_BG = (40,  40,  55)
PANEL_LINE = (80,  80,  110)

PALETTE = [
    (0,   0,   0),    # black
    (255, 255, 255),  # white
    (200, 30,  30),   # red
    (30,  180, 30),   # green
    (30,  80,  220),  # blue
    (255, 200, 0),    # yellow
    (255, 120, 0),    # orange
    (180, 0,   180),  # purple
    (0,   200, 200),  # cyan
    (180, 100, 50),   # brown
    (255, 150, 180),  # pink
    (100, 100, 100),  # grey
]

# ── Fonts ─────────────────────────────────────────────────────────────────────
font_sm = pygame.font.SysFont("Arial", 13, bold=True)
font_md = pygame.font.SysFont("Arial", 16, bold=True)

# ── Tools ─────────────────────────────────────────────────────────────────────
TOOLS = ["Pencil", "Line", "Rect", "Circle", "Eraser"]
TOOL_ICONS = {
    "Pencil": "✏",
    "Line":   "╱",
    "Rect":   "▭",
    "Circle": "○",
    "Eraser": "⬜",
}

# ── Brush sizes ───────────────────────────────────────────────────────────────
BRUSH_SIZES = [2, 5, 10, 18, 30]


# ══════════════════════════════════════════════════════════════════════════════
#  TOOLBAR
# ══════════════════════════════════════════════════════════════════════════════

class Toolbar:
    def __init__(self):
        self.current_tool  = "Pencil"
        self.draw_color    = BLACK
        self.brush_size    = 5
        self.tool_rects    = {}      # tool name → Rect
        self.color_rects   = {}      # color tuple → Rect
        self.size_rects    = {}      # size value → Rect
        self._build_layout()

    def _build_layout(self):
        """Pre-compute all clickable rects in the toolbar."""
        # Tools (left side)
        x = 10
        for tool in TOOLS:
            rect = pygame.Rect(x, 8, 60, 54)
            self.tool_rects[tool] = rect
            x += 66

        # Colour palette (middle)
        px = x + 10
        for i, color in enumerate(PALETTE):
            col = i % 6
            row = i // 6
            rect = pygame.Rect(px + col * 28, 8 + row * 27, 24, 24)
            self.color_rects[color] = rect

        # Brush sizes (right of palette)
        sx = px + 6 * 28 + 14
        for size in BRUSH_SIZES:
            rect = pygame.Rect(sx, 8, 36, 54)
            self.size_rects[size] = rect
            sx += 42

    def draw(self, surf):
        # Background
        pygame.draw.rect(surf, TOOLBAR_BG, (0, 0, WIDTH, TOOLBAR_H))
        pygame.draw.line(surf, PANEL_LINE, (0, TOOLBAR_H), (WIDTH, TOOLBAR_H), 2)

        # ── Tool buttons ─────────────────────────────────────────────────────
        for tool, rect in self.tool_rects.items():
            active = (tool == self.current_tool)
            bg     = (80, 80, 120) if active else (55, 55, 75)
            pygame.draw.rect(surf, bg, rect, border_radius=6)
            pygame.draw.rect(surf, PANEL_LINE, rect, 2, border_radius=6)

            icon  = font_md.render(TOOL_ICONS[tool], True, WHITE)
            label = font_sm.render(tool, True, (200, 200, 220))
            surf.blit(icon,  icon.get_rect(center=(rect.centerx, rect.top + 18)))
            surf.blit(label, label.get_rect(center=(rect.centerx, rect.bottom - 12)))

        # ── Colour palette ────────────────────────────────────────────────────
        for color, rect in self.color_rects.items():
            pygame.draw.rect(surf, color, rect, border_radius=4)
            if color == self.draw_color:
                pygame.draw.rect(surf, WHITE, rect, 2, border_radius=4)
            else:
                pygame.draw.rect(surf, DARK_GREY, rect, 1, border_radius=4)

        # ── Brush size buttons ────────────────────────────────────────────────
        for size, rect in self.size_rects.items():
            active = (size == self.brush_size)
            bg     = (80, 80, 120) if active else (55, 55, 75)
            pygame.draw.rect(surf, bg, rect, border_radius=6)
            pygame.draw.rect(surf, PANEL_LINE, rect, 2, border_radius=6)
            # Show dot proportional to size
            r = min(size // 2, 14)
            pygame.draw.circle(surf, WHITE, rect.center, r)

    def click(self, pos):
        """Handle a mouse click on the toolbar. Returns True if handled."""
        for tool, rect in self.tool_rects.items():
            if rect.collidepoint(pos):
                self.current_tool = tool
                return True
        for color, rect in self.color_rects.items():
            if rect.collidepoint(pos):
                self.draw_color = color
                return True
        for size, rect in self.size_rects.items():
            if rect.collidepoint(pos):
                self.brush_size = size
                return True
        return False


# ══════════════════════════════════════════════════════════════════════════════
#  CANVAS
# ══════════════════════════════════════════════════════════════════════════════

class Canvas:
    def __init__(self):
        self.surface = pygame.Surface((WIDTH, HEIGHT - CANVAS_TOP))
        self.surface.fill(WHITE)

    def clear(self):
        self.surface.fill(WHITE)

    def draw_to(self, surf):
        surf.blit(self.surface, (0, CANVAS_TOP))

    def canvas_pos(self, screen_pos):
        """Convert screen coordinates to canvas coordinates."""
        return (screen_pos[0], screen_pos[1] - CANVAS_TOP)


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN LOOP
# ══════════════════════════════════════════════════════════════════════════════

def main():
    toolbar   = Toolbar()
    canvas    = Canvas()

    drawing   = False       # mouse button held down
    last_pos  = None        # previous mouse position (for pencil lines)
    start_pos = None        # start position for line/rect/circle tools
    preview   = None        # preview surface for shape tools

    while True:
        clock.tick(FPS)

        mouse_pos  = pygame.mouse.get_pos()
        on_canvas  = mouse_pos[1] >= CANVAS_TOP

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                # C = clear canvas
                if event.key == pygame.K_c:
                    canvas.clear()

            # ── Mouse button DOWN ─────────────────────────────────────────────
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not on_canvas:
                    toolbar.click(mouse_pos)
                else:
                    drawing   = True
                    start_pos = canvas.canvas_pos(mouse_pos)
                    last_pos  = start_pos

            # ── Mouse button UP ───────────────────────────────────────────────
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if drawing and on_canvas:
                    end_pos = canvas.canvas_pos(mouse_pos)
                    tool    = toolbar.current_tool
                    color   = toolbar.draw_color
                    size    = toolbar.brush_size

                    # Commit shape to canvas
                    if tool == "Line":
                        pygame.draw.line(canvas.surface, color,
                                         start_pos, end_pos, size)
                    elif tool == "Rect":
                        rx = min(start_pos[0], end_pos[0])
                        ry = min(start_pos[1], end_pos[1])
                        rw = abs(end_pos[0] - start_pos[0])
                        rh = abs(end_pos[1] - start_pos[1])
                        pygame.draw.rect(canvas.surface, color,
                                         (rx, ry, rw, rh), size)
                    elif tool == "Circle":
                        dx  = end_pos[0] - start_pos[0]
                        dy  = end_pos[1] - start_pos[1]
                        rad = max(1, int(math.hypot(dx, dy)))
                        pygame.draw.circle(canvas.surface, color,
                                           start_pos, rad, size)

                drawing   = False
                start_pos = None
                last_pos  = None
                preview   = None

            # ── Mouse MOTION ──────────────────────────────────────────────────
            if event.type == pygame.MOUSEMOTION and drawing and on_canvas:
                cur_pos = canvas.canvas_pos(mouse_pos)
                tool    = toolbar.current_tool
                color   = toolbar.draw_color
                size    = toolbar.brush_size

                if tool == "Pencil":
                    # Draw continuous line segments for smooth strokes
                    if last_pos:
                        pygame.draw.line(canvas.surface, color,
                                         last_pos, cur_pos, size)
                    last_pos = cur_pos

                elif tool == "Eraser":
                    # Eraser = draw white circle
                    pygame.draw.circle(canvas.surface, WHITE, cur_pos, size * 2)

                # For Line/Rect/Circle we build a live preview (don't commit yet)
                elif tool in ("Line", "Rect", "Circle"):
                    preview = (tool, start_pos, cur_pos)

        # ── Render ────────────────────────────────────────────────────────────
        screen.fill(TOOLBAR_BG)
        canvas.draw_to(screen)

        # Draw live shape preview on top of canvas (not committed)
        if preview and drawing:
            p_tool, p_start, p_end = preview
            color  = toolbar.draw_color
            size   = toolbar.brush_size
            p_cur  = canvas.canvas_pos(mouse_pos)

            # Temporary surface so preview doesn't dirty the canvas
            tmp = canvas.surface.copy()

            if p_tool == "Line":
                pygame.draw.line(tmp, color, p_start, p_cur, size)
            elif p_tool == "Rect":
                rx = min(p_start[0], p_cur[0])
                ry = min(p_start[1], p_cur[1])
                rw = abs(p_cur[0] - p_start[0])
                rh = abs(p_cur[1] - p_start[1])
                pygame.draw.rect(tmp, color, (rx, ry, rw, rh), size)
            elif p_tool == "Circle":
                dx  = p_cur[0] - p_start[0]
                dy  = p_cur[1] - p_start[1]
                rad = max(1, int(math.hypot(dx, dy)))
                pygame.draw.circle(tmp, color, p_start, rad, size)

            screen.blit(tmp, (0, CANVAS_TOP))

        toolbar.draw(screen)

        # Cursor crosshair on canvas
        if on_canvas:
            pygame.draw.line(screen, DARK_GREY,
                             (mouse_pos[0] - 8, mouse_pos[1]),
                             (mouse_pos[0] + 8, mouse_pos[1]), 1)
            pygame.draw.line(screen, DARK_GREY,
                             (mouse_pos[0], mouse_pos[1] - 8),
                             (mouse_pos[0], mouse_pos[1] + 8), 1)

        # Hint bar at the bottom
        hint = font_sm.render(
            "C = Clear  |  ESC = Quit  |  Click palette to change colour  |  Click size to change brush",
            True, (150, 150, 170))
        screen.blit(hint, (10, HEIGHT - 20))

        pygame.display.flip()


if __name__ == "__main__":
    main()
