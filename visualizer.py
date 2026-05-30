import sys
import pygame

BG=(0,0,0); FL=(60,120,255); AR=(50,200,80); CO=(220,60,60)
WH=(255,255,255); YL=(255,210,50); GR=(120,120,120); PN=(0,0,22)

PANEL_W = 210

class Visualizer:
    def __init__(self, w=800, h=600, fps=60):
        pygame.init()
        self.w, self.h = w, h
        self.tw = w + PANEL_W
        self.screen = pygame.display.set_mode((self.tw, h))
        pygame.display.set_caption("Simulador de Drones")
        self.clock = pygame.time.Clock()
        self.font  = pygame.font.SysFont("Courier", 13)
        self.fontL = pygame.font.SysFont("Courier", 15, bold=True)
        self.fps   = fps