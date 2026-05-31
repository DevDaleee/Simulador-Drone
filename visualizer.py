import sys
import pygame
import config

class Visualizer:
    def __init__(self, w=config.W, h=config.H, fps=config.FPS):
        pygame.init()
        self.w   = w
        self.h   = h
        self.fps = fps

        self.tw = self.w + config.PANEL_W
        self.screen = pygame.display.set_mode((self.tw, self.h))
        pygame.display.set_caption("Simulador de Drones")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Courier", 13)
        self.fontB = pygame.font.SysFont("Courier", 15, bold=True)

    def _txt(self, t, x, y, cor=None, bold=False):
        self.screen.blit((self.fontB if bold else self.font).render(t, True, cor or config.CORES["texto"]), (x, y))

    def update(self, drones, step, events=None):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        s = self.screen
        s.fill(config.CORES["bg"])

        for d in drones:
            dx, dy = int(d.dest_x), int(d.dest_y)
            pygame.draw.line(s, config.CORES["dim"], (dx-5,dy-5), (dx+5,dy+5), 2)
            pygame.draw.line(s, config.CORES["dim"], (dx+5,dy-5), (dx-5,dy+5), 2)
            pygame.draw.circle(s, config.CORES[d.status], (int(d.x), int(d.y)), 6)
            self._txt(str(d.id), int(d.x)+8, int(d.y)-6)

        lx = self.w
        pygame.draw.rect(s, config.CORES["painel"], (lx, 0, config.PANEL_W, self.h))
        titulo = self.fontB.render("SIMULADOR DE DRONES", True, config.CORES["titulo"])
        s.blit(titulo, titulo.get_rect(center=(lx + config.PANEL_W//2, 18)))

        for i, (lbl, st) in enumerate([("Em voo","em_voo"),("Chegados","chegou"),("Colisoes","colidiu")]):
            qtd = sum(1 for d in drones if d.status == st)
            self._txt(f"{lbl}: {qtd}", lx+10, 42+i*22, config.CORES[st])
        self._txt(f"Passo : {step}", lx+10, 110, config.CORES["dim"])

        pygame.display.flip()
        self.clock.tick(self.fps)

    def show_final_metrics(self, m):
        linhas = [
            ("Chegaram ao destino", f"{m['qtd_chegaram']}", "chegou"),
            ("Colidiram", f"{m['qtd_colidiram']}", "colidiu"),
            ("Nao concluiram", f"{m['qtd_nao_concluiram']}", "em_voo"),
            ("Taxa de colisao", f"{m['taxa_colisao']:.1f}%", "texto"),
            ("Perc. de sucesso", f"{m['percentual_sucesso']:.1f}%", "chegou"),
            ("Tempo medio missao", f"{m['tempo_medio_missao']:.1f} passos", "texto"),
            ("Distancia media", f"{m['distancia_media']:.1f} px", "texto"),
            ("Total de passos", f"{m['total_steps']}", "texto"),
            ("Tempo real", f"{m['tempo_real_segundos']:.2f}s", "titulo"),
        ]
        while True:
            for e in pygame.event.get():
                if e.type in (pygame.QUIT, pygame.KEYDOWN):
                    pygame.quit(); return

            s = self.screen
            s.fill(config.CORES["bg"])
            t = self.fontB.render("RESULTADO FINAL DA SIMULACAO", True, config.CORES["titulo"])
            s.blit(t, t.get_rect(center=(self.tw//2, 36)))
            pygame.draw.line(s, config.CORES["titulo"], (80, 54), (self.tw-80, 54), 1)

            cx, cv = self.tw//2 - 270, self.tw//2 + 90
            for i, (lbl, val, st) in enumerate(linhas):
                y = 66 + i*50
                if i % 2 == 0:
                    pygame.draw.rect(s, (10,10,32), (cx-10, y-4, 600, 42))
                self._txt(f"{lbl}:", cx, y+8, config.CORES["dim"])
                self._txt(val, cv, y+8, config.CORES[st])

            self._txt("Pressione qualquer tecla para sair", self.tw//2 - 140, self.h-28, config.CORES["dim"])
            pygame.display.flip()
            self.clock.tick(30)
