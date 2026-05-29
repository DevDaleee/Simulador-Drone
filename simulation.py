import time
import math

COLLISION_DIST = 15
MAX_STEPS      = 300

def run(drones, viz):
    events, total_steps = [], 0
    t0 = time.perf_counter()

    for step in range(1, MAX_STEPS + 1):
        flying = [d for d in drones if d.status == "em_voo"]
        if not flying:
            break

        for d in flying:
            d.move(step)
            if d.status == "chegou":
                events.append({"step": step, "type": "chegada", "drone_id": d.id})

        airborne = [d for d in drones if d.status == "em_voo"]
        for i in range(len(airborne)):
            for j in range(i + 1, len(airborne)):
                d1, d2 = airborne[i], airborne[j]
                dist = math.sqrt((d2.x - d1.x)**2 + (d2.y - d1.y)**2)
                if dist < COLLISION_DIST:
                    for d in [d1, d2]:
                        if d.status == "em_voo":
                            d.status, d.end_step = "colidiu", step
                    events.append({"step": step, "type": "colisao", "drones": [d1.id, d2.id]})

        viz.update(drones, step, events)
        total_steps = step

    return {"total_steps": total_steps, "events": events, "elapsed": time.perf_counter() - t0}
