
from tilegamelib.screen import Screen
from tilegamelib.frame import Frame
from tilegamelib.tile_factory import TileFactory
from tilegamelib.vector import Vector, RIGHT
from pygame import Rect
import pygame
import time


class Move(object):
    """
    Moves a tile over a certain amount of steps in one direction.
    """
    def __init__(self, frame, tile, start_vector=None, direction=None, steps=0, when_finished=None):
        self.frame = frame
        self.tile = tile
        self.start_vector = start_vector or Vector(0, 0)
        self.steps = steps
        self.direction = direction or RIGHT
        self.current_vector = None
        self.finished = False
        self.callback = when_finished

    def update_current_vector(self):
        if self.current_vector is None:
            self.current_vector = self.start_vector
        self.current_vector += self.direction

    def move(self):
        if self.steps > 0:
            self.update_current_vector()
            self.steps -= 1
        if self.steps <= 0:
            self.finished = True
            if self.callback:
                self.callback()
        self.tile.draw(self.frame, self.current_vector)


def wait_for_move(move, screen=None, draw=None, delay=0.01):
    while not move.finished:
        if screen:
            screen.clear()
        if draw:
            draw()
        move.move()
        pygame.display.update()
        time.sleep(delay)


if __name__ == '__main__':
    screen = Screen(Vector(800,520), '../examples/data/background.png')
    frame = Frame(screen, Rect(64, 64, 320, 320))
    tile_factory = TileFactory('../examples/data/tiles.conf')
    pac = tile_factory.get('b.pac_right')
    move = Move(frame, pac, Vector(50, 50), RIGHT*2, 200)
    wait_for_move(move, screen)
    time.sleep(1)
