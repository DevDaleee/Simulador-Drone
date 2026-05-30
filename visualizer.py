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

        lx = self.w
        pygame.draw.rect(s, PN, (lx, 0, PANEL_W, self.h))
        pygame.draw.line(s, (40, 40, 90), (lx, 0), (lx, self.h), 2)

        def txt(text, x, y, color=WH, f=None):
            s.blit((f or self.font).render(text, True, color), (x, y))

        def sep(y):
            pygame.draw.line(s, (40,40,90), (lx+8, y), (lx+PANEL_W-8, y), 1)

        t = self.fontL.render("SIMULADOR DE DRONES", True, YL)
        s.blit(t, t.get_rect(center=(lx + PANEL_W//2, 18)))
        sep(34)

        hud = [
            (f"Passo   : {step}",                                          WH),
            (f"Em voo  : {sum(1 for d in drones if d.status=='em_voo')}",  FL),
            (f"Chegados: {sum(1 for d in drones if d.status=='chegou')}",  AR),
            (f"Colisoes: {sum(1 for d in drones if d.status=='colidiu')}", CO),
        ]
        for i, (t, c) in enumerate(hud):
            txt(t, lx+10, 42+i*22, c)
        sep(134)

        pygame.display.flip()
        self.clock.tick(self.fps)