import random
from drone import Drone
from visualizer import Visualizer

W, H   = 800, 600
N      = 15
MARGIN = 60
FPS    = 60

if __name__ == "__main__":
    viz = Visualizer(W, H, FPS)
    import pygame, sys
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        viz.screen.fill((0,0,0))
        pygame.display.flip()
        viz.clock.tick(FPS)