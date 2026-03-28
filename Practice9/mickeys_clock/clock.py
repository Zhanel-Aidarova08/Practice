# clock.py
# Clock logic: angle calculations for minute and second hands

import datetime
import math


def get_time():
    """Return current (minutes, seconds) as integers."""
    now = datetime.datetime.now()
    return now.minute, now.second


def seconds_angle(seconds: int) -> float:
    """
    Angle in degrees for the seconds hand.
    0 sec = pointing up (−90°), rotates clockwise.
    pygame.transform.rotate rotates counter-clockwise,
    so we negate the angle.
    """
    return -(seconds / 60) * 360


def minutes_angle(minutes: int, seconds: int) -> float:
    """
    Angle in degrees for the minutes hand.
    Smooth: includes fractional position based on seconds.
    """
    total = minutes + seconds / 60
    return -(total / 60) * 360


def rotate_hand(surface, angle):
    """
    Rotate a pygame Surface around its centre.
    Returns (rotated_surface, rect_centred_on_pivot).
    """
    import pygame
    rotated = pygame.transform.rotate(surface, angle)
    return rotated
