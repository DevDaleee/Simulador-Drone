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

        txt("LEGENDA", lx+10, 140, GR)
        for i, (lbl, col) in enumerate([("Em voo", FL), ("Chegou", AR), ("Colidiu", CO)]):
            pygame.draw.circle(s, col, (lx+18, 162+i*22), 5)
            txt(lbl, lx+30, 155+i*22, col)
        sep(228)

        txt("EVENTOS", lx+10, 234, GR)
        if events:
            for i, ev in enumerate(events[-8:]):
                if ev["type"] == "chegada":
                    line, col = f"D{ev['drone_id']} chegou  p.{ev['step']}", AR
                else:
                    ids = ",".join(str(x) for x in ev["drones"])
                    line, col = f"D{ids} col.  p.{ev['step']}", CO
                txt(line, lx+10, 252+i*20, col)

        pygame.display.flip()
        self.clock.tick(self.fps)

    def show_final_metrics(self, m):
        waiting = True
        while waiting:
            for e in pygame.event.get():
                if e.type in (pygame.QUIT, pygame.KEYDOWN):
                    waiting = False
            s = self.screen
            s.fill(BG)
            t = self.fontL.render("RESULTADO FINAL DA SIMULACAO", True, YL)
            s.blit(t, t.get_rect(center=(self.tw//2, 36)))
            pygame.draw.line(s, YL, (80, 54), (self.tw-80, 54), 1)

            rows = [
                ("Chegaram ao destino", f"{m['qtd_chegaram']}",                 AR),
                ("Colidiram",           f"{m['qtd_colidiram']}",                 CO),
                ("Nao concluiram",      f"{m['qtd_nao_concluiram']}",            FL),
                ("Taxa de colisao",     f"{m['taxa_colisao']:.1f}%",             WH),
                ("Perc. de sucesso",    f"{m['percentual_sucesso']:.1f}%",       AR),
                ("Tempo medio missao",  f"{m['tempo_medio_missao']:.1f} passos", WH),
                ("Distancia media",     f"{m['distancia_media']:.1f} px",        WH),
                ("Total de passos",     f"{m['total_steps']}",                   WH),
                ("Tempo real",          f"{m['tempo_real_segundos']:.2f}s",      YL),
            ]
            cl = self.tw//2 - 270
            cr = self.tw//2 + 90
            for i, (lbl, val, col) in enumerate(rows):
                y = 66 + i*50
                if i % 2 == 0:
                    pygame.draw.rect(s, (10,10,32), (cl-10, y-4, 600, 42))
                s.blit(self.font.render(lbl+":", True, (150,150,150)), (cl, y+8))
                s.blit(self.font.render(val,     True, col),           (cr, y+8))

            h = self.font.render("Pressione qualquer tecla para sair", True, GR)
            s.blit(h, h.get_rect(center=(self.tw//2, self.h-28)))
            pygame.display.flip()
            self.clock.tick(30)
        pygame.quit()