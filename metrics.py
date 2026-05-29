def compute(drones, total_steps, elapsed=0.0):
    arr  = [d for d in drones if d.status == "chegou"]
    col  = [d for d in drones if d.status == "colidiu"]
    inc  = [d for d in drones if d.status == "em_voo"]
    n    = len(drones)
    done = [d for d in arr + col if d.end_step is not None]

    return {
        "qtd_chegaram":        len(arr),
        "qtd_colidiram":       len(col),
        "qtd_nao_concluiram":  len(inc),
        "taxa_colisao":        len(col) / n * 100 if n else 0.0,
        "percentual_sucesso":  len(arr) / n * 100 if n else 0.0,
        "tempo_medio_missao":  sum(d.end_step for d in done) / len(done) if done else 0.0,
        "distancia_media":     sum(d.dist_traveled for d in drones) / n if n else 0.0,
        "total_steps":         total_steps,
        "tempo_real_segundos": elapsed,
    }
