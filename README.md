# 🧭 Pathfinder AI — Visual Algorithm Simulator

An interactive web app where you draw walls on a grid and watch AI search algorithms find the shortest path in real time. Built to showcase Python algorithmic thinking with a slick, deployable web frontend.

**Live demo:** [vercel.app](https://rd-pathfinder-game.vercel.app/)

---

## What it does

- Paint walls on a 40×26 grid with your mouse (or finger on mobile)
- Move the Start and End points anywhere
- Pick an algorithm and watch it explore cell by cell
- See live stats: cells explored, path length, compute time

---

## Algorithms included

| Algorithm | Optimal? | Uses heuristic? | Best for |
|---|---|---|---|
| **A\*** | ✅ Yes | ✅ Yes (Manhattan) | Most cases — fast & optimal |
| **Dijkstra's** | ✅ Yes | ❌ No | Weighted graphs, guaranteed shortest |
| **BFS** | ✅ Yes | ❌ No | Unweighted grids, simple mazes |
| **DFS** | ❌ No | ❌ No | Fast exploration, not shortest path |
| **Greedy BFS** | ❌ No | ✅ Yes | Speed over optimality |

---

## Tech stack

```
Frontend   →  HTML + CSS + Canvas API (vanilla, zero dependencies)
AI logic   →  JavaScript (same algorithm as pathfinding.py)
Reference  →  Python (pathfinding.py — the same logic in pure Python)
Deploy     →  Vercel (static, one click)
```

The Python file (`pathfinding.py`) is the reference implementation — same algorithms, runnable locally, showing the clean algorithmic logic without any browser overhead.

---

## Run locally

```bash
# Just open the HTML — no server needed
open index.html

# Or serve with Python
python -m http.server 3000
# then open http://localhost:3000
```

To run the Python reference:
```bash
python pathfinding.py
```

---

## Deploy to Vercel (30 seconds)

1. Push this repo to GitHub
2. Go to [vercel.com](https://vercel.com) → New Project → Import your repo
3. Framework preset: **Other**
4. Root directory: `/` (leave default)
5. Click **Deploy**

That's it. No build step, no config, no environment variables.

---

## How A* works

```
f(n) = g(n) + h(n)

g(n) = actual cost from start to node n
h(n) = estimated cost from n to goal  (Manhattan distance)
f(n) = total estimated cost of path through n
```

The priority queue always expands the node with the lowest `f(n)` first. This guarantees the optimal path while being dramatically faster than Dijkstra on most grids because the heuristic steers the search toward the goal.

---

## Project structure

```
pathfinder/
├── index.html       ← entire app (HTML + CSS + JS, self-contained)
├── pathfinding.py   ← Python reference implementation
└── README.md
```

---

## Portfolio talking points

- **A\* from scratch** — understands heuristics, priority queues, and optimal search
- **5 algorithms side by side** — can explain trade-offs between them
- **No frameworks** — raw Canvas API, shows JS fundamentals
- **Python ↔ JS parity** — same logic in both languages, demonstrating transferability
- **Instant Vercel deploy** — single static HTML file, zero config
