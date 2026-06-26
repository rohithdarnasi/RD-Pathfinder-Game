"""
pathfinding.py — Python reference implementation
=================================================
This is the Python brain behind the visual simulator.
Shows the same algorithms running in pure Python — great for
understanding the logic, testing, and your portfolio README.

Run:
    python pathfinding.py

Or import and use in your own code:
    from pathfinding import astar, dijkstra, bfs
"""

import heapq
from collections import deque
from typing import Optional


# ── Grid type ─────────────────────────────────────────────────────────────
Grid = list[list[int]]   # 0 = empty, 1 = wall
Point = tuple[int, int]  # (row, col)


def neighbors(grid: Grid, r: int, c: int) -> list[Point]:
    """Return walkable 4-directional neighbors."""
    rows, cols = len(grid), len(grid[0])
    result = []
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr, nc = r+dr, c+dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
            result.append((nr, nc))
    return result


def reconstruct(came_from: dict, node: Point) -> list[Point]:
    """Walk back through came_from to build the path."""
    path = []
    while node in came_from:
        node = came_from[node]
        path.append(node)
    return list(reversed(path))


# ── A* ────────────────────────────────────────────────────────────────────
def astar(grid: Grid, start: Point, end: Point) -> Optional[list[Point]]:
    """
    A* Search — optimal + heuristic-guided.
    Uses Manhattan distance as the heuristic h(n).
    Time: O(E log V)  |  Space: O(V)
    """
    def h(r, c):
        return abs(r - end[0]) + abs(c - end[1])

    g_score = {start: 0}
    f_score = {start: h(*start)}
    came_from = {}
    open_heap = [(f_score[start], start)]
    visited = set()

    while open_heap:
        _, current = heapq.heappop(open_heap)
        if current in visited:
            continue
        visited.add(current)

        if current == end:
            return reconstruct(came_from, end)

        for nb in neighbors(grid, *current):
            tentative_g = g_score[current] + 1
            if tentative_g < g_score.get(nb, float('inf')):
                came_from[nb] = current
                g_score[nb]   = tentative_g
                f_score[nb]   = tentative_g + h(*nb)
                heapq.heappush(open_heap, (f_score[nb], nb))

    return None  # no path


# ── Dijkstra ──────────────────────────────────────────────────────────────
def dijkstra(grid: Grid, start: Point, end: Point) -> Optional[list[Point]]:
    """
    Dijkstra's Algorithm — optimal, no heuristic.
    Explores uniformly in all directions.
    Time: O(E log V)  |  Space: O(V)
    """
    dist = {start: 0}
    came_from = {}
    heap = [(0, start)]
    visited = set()

    while heap:
        d, current = heapq.heappop(heap)
        if current in visited:
            continue
        visited.add(current)

        if current == end:
            return reconstruct(came_from, end)

        for nb in neighbors(grid, *current):
            new_d = d + 1
            if new_d < dist.get(nb, float('inf')):
                dist[nb]      = new_d
                came_from[nb] = current
                heapq.heappush(heap, (new_d, nb))

    return None


# ── BFS ───────────────────────────────────────────────────────────────────
def bfs(grid: Grid, start: Point, end: Point) -> Optional[list[Point]]:
    """
    Breadth-First Search — optimal on unweighted grids.
    Explores layer-by-layer (nearest cells first).
    Time: O(V + E)  |  Space: O(V)
    """
    queue = deque([start])
    visited = {start}
    came_from = {}

    while queue:
        current = queue.popleft()
        if current == end:
            return reconstruct(came_from, end)

        for nb in neighbors(grid, *current):
            if nb not in visited:
                visited.add(nb)
                came_from[nb] = current
                queue.append(nb)

    return None


# ── DFS ───────────────────────────────────────────────────────────────────
def dfs(grid: Grid, start: Point, end: Point) -> Optional[list[Point]]:
    """
    Depth-First Search — NOT optimal, but fast.
    Dives deep before backtracking.
    Time: O(V + E)  |  Space: O(V)
    """
    stack = [start]
    visited = set()
    came_from = {}

    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)

        if current == end:
            return reconstruct(came_from, end)

        for nb in neighbors(grid, *current):
            if nb not in visited:
                came_from[nb] = current
                stack.append(nb)

    return None


# ── Greedy Best-First ─────────────────────────────────────────────────────
def greedy(grid: Grid, start: Point, end: Point) -> Optional[list[Point]]:
    """
    Greedy Best-First — fast but NOT always optimal.
    Only considers h(n), ignores actual cost g(n).
    """
    def h(r, c):
        return abs(r - end[0]) + abs(c - end[1])

    came_from = {}
    heap = [(h(*start), start)]
    visited = set()

    while heap:
        _, current = heapq.heappop(heap)
        if current in visited:
            continue
        visited.add(current)

        if current == end:
            return reconstruct(came_from, end)

        for nb in neighbors(grid, *current):
            if nb not in visited:
                came_from[nb] = current
                heapq.heappush(heap, (h(*nb), nb))

    return None


# ── Pretty print helper ───────────────────────────────────────────────────
def print_grid(grid: Grid, path: list[Point], start: Point, end: Point):
    rows, cols = len(grid), len(grid[0])
    path_set = set(map(tuple, path))
    symbols = {0:'.', 1:'█'}
    for r in range(rows):
        row = ''
        for c in range(cols):
            if (r,c) == start:      row += 'S'
            elif (r,c) == end:      row += 'E'
            elif (r,c) in path_set: row += '★'
            else:                   row += symbols[grid[r][c]]
        print(row)


# ── Demo ──────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    import time

    # 10×20 test maze (0=open, 1=wall)
    MAZE = [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,0],
        [0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0],
        [0,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,0],
        [0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
        [0,1,0,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0],
        [0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,1,0],
        [0,1,1,1,0,1,0,1,0,1,1,1,1,1,1,1,0,0,1,0],
        [0,0,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,1,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    ]

    START = (0, 0)
    END   = (9, 19)

    algos = {
        'A*':       astar,
        'Dijkstra': dijkstra,
        'BFS':      bfs,
        'DFS':      dfs,
        'Greedy':   greedy,
    }

    print('=' * 50)
    print('  Pathfinding Algorithm Comparison')
    print('=' * 50)

    for name, fn in algos.items():
        t0   = time.perf_counter()
        path = fn(MAZE, START, END)
        ms   = (time.perf_counter() - t0) * 1000

        if path:
            print(f'\n{name}  →  path length: {len(path)}  |  {ms:.3f} ms')
            print_grid(MAZE, path, START, END)
        else:
            print(f'\n{name}  →  NO PATH FOUND')

    print('\nDone.')
