import random
from drone      import Drone
from simulation import run
from metrics    import compute
from visualizer import Visualizer

W, H   = 800, 600
N      = 15
MARGIN = 60
FPS    = 60


def create_drones():
    drones = []
    for i in range(N):
        x      = random.uniform(MARGIN, W - MARGIN)
        y      = random.uniform(MARGIN, H - MARGIN)
        dest_x = random.uniform(MARGIN, W - MARGIN)
        dest_y = random.uniform(MARGIN, H - MARGIN)
        speed  = round(random.uniform(1.5, 3.5), 2)
        drones.append(Drone(i, x, y, dest_x, dest_y, speed))
    return drones


def print_metrics(m, events):
    sep = "=" * 48
    print(f"\n{sep}\n  METRICAS FINAIS\n{sep}")
    print(f"  Chegaram ao destino  : {m['qtd_chegaram']}")
    print(f"  Colidiram            : {m['qtd_colidiram']}")
    print(f"  Nao concluiram       : {m['qtd_nao_concluiram']}")
    print(f"  Taxa de colisao      : {m['taxa_colisao']:.1f}%")
    print(f"  Percentual de sucesso: {m['percentual_sucesso']:.1f}%")
    print(f"  Tempo medio de missao: {m['tempo_medio_missao']:.1f} passos")
    print(f"  Distancia media      : {m['distancia_media']:.1f} px")
    print(f"  Total de passos      : {m['total_steps']}")
    print(f"  Tempo real           : {m['tempo_real_segundos']:.2f}s")
    arrs = [e for e in events if e["type"] == "chegada"]
    cols = [e for e in events if e["type"] == "colisao"]
    if arrs: print(f"\n  Chegadas ({len(arrs)}): " +
                   ", ".join(f"D{e['drone_id']} p.{e['step']}" for e in arrs))
    if cols: print(f"  Colisoes ({len(cols)}): " +
                   ", ".join(f"D{e['drones']} p.{e['step']}" for e in cols))
    print(sep)


if __name__ == "__main__":
    drones = create_drones()
    viz    = Visualizer(W, H, FPS)
    result = run(drones, viz)
    m      = compute(drones, result["total_steps"], result["elapsed"])
    print_metrics(m, result["events"])