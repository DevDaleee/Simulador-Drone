# Simulador de Drones

Simulador computacional 2D de drones em movimento com posições e destinos gerados aleatoriamente a cada execução. Detecta colisões em tempo real, coleta métricas e exibe a simulação visualmente via Pygame.

## Instalação

```bash
pip install pygame numpy
```

## Como executar

```bash
python main.py
```

## Parâmetros configuráveis (`main.py`)

| Parâmetro | Padrão | Descrição |
|---|---|---|
| `W`, `H` | 800, 600 | Dimensões da janela em pixels |
| `N` | 15 | Número de drones na simulação |
| `MARGIN` | 60 | Distância mínima das bordas para posições e destinos |
| `FPS` | 60 | Frames por segundo da visualização |

O parâmetro `COLLISION_DIST` (padrão `15` px) e `MAX_STEPS` (padrão `2000`) ficam em `simulation.py`.

## Métricas geradas

| Métrica | Descrição |
|---|---|
| `qtd_chegaram` | Drones que alcançaram o destino com sucesso |
| `qtd_colidiram` | Drones envolvidos em colisão |
| `qtd_nao_concluiram` | Drones ainda em voo ao fim dos 2000 passos |
| `taxa_colisao` | `(colidiram / total) × 100` em % |
| `percentual_sucesso` | `(chegaram / total) × 100` em % |
| `tempo_medio_missao` | Média de passos até encerrar (chegada ou colisão) |
| `distancia_media` | Média de pixels percorridos por drone |
| `total_steps` | Total de passos executados até o fim |
| `tempo_real_segundos` | Tempo de CPU da simulação em segundos |

## Detecção e tratamento de colisões

A cada passo, após mover todos os drones, o simulador verifica todos os pares em voo usando a **distância euclidiana**:

```
d = ||pos1 - pos2||  =  sqrt((x2-x1)² + (y2-y1)²)
```

Se `d < COLLISION_DIST` (15 px), ambos têm status alterado para `"colidiu"` e param de se mover. O evento é registrado com o passo e os IDs dos drones envolvidos.

## Fórmula de movimento

O deslocamento de cada drone usa o **vetor unitário de direção** — mesma equação usada em controladores de voo UAV reais (PX4, ArduPilot):

```
v⃗  =  (dest - pos) / ||dest - pos||  ×  speed
pos = pos + v⃗
```

A normalização garante velocidade constante independente da direção.
