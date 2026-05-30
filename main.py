import random
from drone import Drone
from simulation import run
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


if __name__ == "__main__":
    drones = create_drones()
    viz    = Visualizer(W, H, FPS)
    run(drones, viz)