# ball.py
# Ball entity: position, radius, movement with boundary checking

class Ball:
    RADIUS = 25
    STEP   = 20

    def __init__(self, screen_w: int, screen_h: int):
        self.screen_w = screen_w
        self.screen_h = screen_h
        # Start at centre
        self.x = screen_w // 2
        self.y = screen_h // 2

    def move(self, dx: int, dy: int):
        """Move by (dx, dy) pixels — stays inside screen bounds."""
        new_x = self.x + dx
        new_y = self.y + dy

        # Only apply if the ball stays fully inside the screen
        if self.RADIUS <= new_x <= self.screen_w - self.RADIUS:
            self.x = new_x
        if self.RADIUS <= new_y <= self.screen_h - self.RADIUS:
            self.y = new_y

    def move_up(self):    self.move(0, -self.STEP)
    def move_down(self):  self.move(0,  self.STEP)
    def move_left(self):  self.move(-self.STEP, 0)
    def move_right(self): self.move( self.STEP, 0)

    def draw(self, surf):
        import pygame
        # Shadow
        pygame.draw.circle(surf, (180, 50, 50),
                           (self.x + 3, self.y + 3), self.RADIUS)
        # Main ball
        pygame.draw.circle(surf, (220, 40, 40),
                           (self.x, self.y), self.RADIUS)
        # Shine highlight
        pygame.draw.circle(surf, (255, 120, 120),
                           (self.x - 8, self.y - 8), 8)
