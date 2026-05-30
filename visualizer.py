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

    def _cor(self, d):
        return FL if d.status == "em_voo" else AR if d.status == "chegou" else CO

    def update(self, drones, step, events=None):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        s = self.screen
        s.fill(BG)

        for d in drones:
            if d.status == "em_voo":
                pygame.draw.line(s, (30, 30, 65),
                                 (int(d.x),      int(d.y)),
                                 (int(d.dest_x), int(d.dest_y)), 1)

        for d in drones:
            x, y = int(d.dest_x), int(d.dest_y)
            pygame.draw.line(s, GR, (x-5,y-5),(x+5,y+5), 2)
            pygame.draw.line(s, GR, (x+5,y-5),(x-5,y+5), 2)

        for d in drones:
            px, py = int(d.x), int(d.y)
            pygame.draw.circle(s, self._cor(d), (px, py), 6)
            s.blit(self.font.render(str(d.id), True, WH), (px+8, py-6))

        pygame.display.flip()
        self.clock.tick(self.fps)