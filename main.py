import pygame
import random
import sys
import numpy as np
from config import *
from agent import Agent

# Increase recursion depth for complex mazes
sys.setrecursionlimit(5000)

pygame.init()
# Use native desktop resolution
infoObject = pygame.display.Info()
W_WIDTH, W_HEIGHT = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode((W_WIDTH, W_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Cyberpunk Maze: Tech Divas Edition")
clock = pygame.time.Clock()

# Fonts
font_sm = pygame.font.SysFont("Courier New", 18, bold=True)
font_md = pygame.font.SysFont("Verdana", 22, bold=True)
font_lg = pygame.font.SysFont("Verdana", 35, bold=True)

# --- HELPER FUNCTIONS ---
def get_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def solve_maze_bfs(maze, start, goal, rows, cols):
    """Calculates path for the Hint System"""
    queue = [(start, [start])]
    visited = {start}
    while queue:
        (r, c), path = queue.pop(0)
        if (r, c) == goal: return path
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0 and (nr, nc) not in visited:
                visited.add((nr, nc))
                new_path = list(path)
                new_path.append((nr, nc))
                queue.append(((nr, nc), new_path))
    return None

def generate_guaranteed_maze(rows, cols):
    while True:
        grid = [[1 for _ in range(cols)] for _ in range(rows)]
        def carve(r, c):
            grid[r][c] = 0
            directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
            random.shuffle(directions)
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[r + dr // 2][c + dc // 2] = 0
                    carve(nr, nc)
        carve(0, 0)
        grid[0][0] = 0; grid[0][1] = 0
        grid[rows-1][cols-1] = 0; grid[rows-1][cols-2] = 0
        # Check if solvable
        solution = solve_maze_bfs(grid, (0,0), (rows-1, cols-1), rows, cols)
        if solution: return grid, solution

# --- SETUP ---
CELL_SIZE = min(W_WIDTH // COLS, (W_HEIGHT - 100) // ROWS)
OFFSET_X = (W_WIDTH - (COLS * CELL_SIZE)) // 2
OFFSET_Y = (W_HEIGHT - (ROWS * CELL_SIZE)) // 2

maze, solution_path = generate_guaranteed_maze(ROWS, COLS)
agent = Agent(ROWS, COLS)

# --- VARIABLES ---
state = (0, 0)
goal = (ROWS - 1, COLS - 1)
episode = 1
stats = {"walls": 0, "explore": 0, "steps": 0, "score": 0, "result": "RUNNING"}
visited_episode = set()

# --- REVERSE CURRICULUM SETUP ---
# Start 10 steps away from the exit (instead of 1)
current_distance = 10 

path_len = len(solution_path)
start_index = max(0, path_len - 1 - current_distance)
state = solution_path[start_index]

# Game State Management
# States: "PLAYING", "DASHBOARD", "PLACEMENT"
game_state = "PLAYING" 

# Flags
is_test_mode = False 
show_hint = False
game_speed = 60
running = True

while running:
    
    # =================================================
    # STATE 1: DASHBOARD (Result Screen)
    # =================================================
    if game_state == "DASHBOARD":
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: running = False
                if event.key == pygame.K_SPACE: 
                    # Go to Placement Mode
                    game_state = "PLACEMENT"
                    episode += 1
                    
                    # Logic: If successful, move start point back
                    if stats["result"] == "SUCCESS":
                        current_distance += 1 # Increase difficulty
                    
                    if not is_test_mode: agent.decay_epsilon()
                    
                    # Reset stats but KEEP POSITIONS until user changes them
                    stats = {"walls": 0, "explore": 0, "steps": 0, "score": 0, "result": "RUNNING"}
                    visited_episode = set()
                    
                    # Auto-update start position based on new distance
                    path_len = len(solution_path)
                    start_index = max(0, path_len - 1 - current_distance)
                    # Only update state if we are NOT in god mode placement
                    state = solution_path[start_index]

        # Draw semi-transparent background
        overlay = pygame.Surface((W_WIDTH, W_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 230))
        screen.blit(overlay, (0, 0))
        
        # Draw Box
        bx, by, bw, bh = W_WIDTH//2 - 350, W_HEIGHT//2 - 250, 700, 500
        pygame.draw.rect(screen, (30, 30, 40), (bx, by, bw, bh))
        pygame.draw.rect(screen, COLOR_WALL_TOP, (bx, by, bw, bh), 4)
        
        # Title
        head_col = COLOR_GOAL if stats["result"] == "SUCCESS" else (255, 100, 100)
        screen.blit(font_lg.render(f"EPISODE {episode} COMPLETE", True, head_col), (bx+180, by+30))
        
        lines = [
            f"RESULT:        {stats['result']}",
            f"DISTANCE:      {current_distance} Steps from Exit",
            f"-------------------------------",
            f"Walls Hit:     {stats['walls']}  (-20 pts)",
            f"New Tiles:     {stats['explore']}  (+100 pts)",
            f"Steps Taken:   {stats['steps']}  (-10 pts)",
            f"-------------------------------",
            f"FINAL SCORE:   {stats['score']}"
        ]
        
        for i, line in enumerate(lines):
            screen.blit(font_md.render(line, True, (220, 220, 220)), (bx+50, by+100 + i*45))
        
        # Instruction
        pygame.draw.rect(screen, (0, 0, 0), (bx+50, by+bh-80, bw-100, 50))
        screen.blit(font_sm.render("[PRESS SPACE TO CHANGE POSITIONS]", True, (0, 255, 0)), (bx+160, by+bh-65))
        
        pygame.display.flip()
        clock.tick(10)
        continue

    # =================================================
    # STATE 2: PLACEMENT MODE (Edit Map Positions)
    # =================================================
    elif game_state == "PLACEMENT":
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: running = False
                if event.key == pygame.K_RETURN: # Start Game
                    game_state = "PLAYING"
                if event.key == pygame.K_r: # New Random Maze
                    maze, solution_path = generate_guaranteed_maze(ROWS, COLS)
                    current_distance = 10 # Reset distance on new map
                    path_len = len(solution_path)
                    state = solution_path[max(0, path_len - 1 - current_distance)]
                    goal = (ROWS-1, COLS-1)
                    
            # MOUSE HANDLING
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                c = (mx - OFFSET_X) // CELL_SIZE
                r = (my - OFFSET_Y) // CELL_SIZE
                
                if 0 <= r < ROWS and 0 <= c < COLS and maze[r][c] == 0:
                    if event.button == 1: # Left Click
                        state = (r, c)
                    elif event.button == 3: # Right Click
                        goal = (r, c)
                        solution_path = solve_maze_bfs(maze, state, goal, ROWS, COLS)

        # Draw Map
        screen.fill(COLOR_BG)
        for r in range(ROWS):
            for c in range(COLS):
                x, y = c * CELL_SIZE + OFFSET_X, r * CELL_SIZE + OFFSET_Y
                if maze[r][c] == 1:
                    pygame.draw.rect(screen, COLOR_WALL_TOP, (x, y, CELL_SIZE, CELL_SIZE))
                else:
                    pygame.draw.rect(screen, (40,40,50), (x, y, CELL_SIZE, CELL_SIZE))
                    pygame.draw.rect(screen, (60,60,70), (x, y, CELL_SIZE, CELL_SIZE), 1)

        # Draw Goal & Agent
        gr, gc = goal
        pygame.draw.rect(screen, COLOR_GOAL, (gc*CELL_SIZE+OFFSET_X, gr*CELL_SIZE+OFFSET_Y, CELL_SIZE, CELL_SIZE))
        ar, ac = state
        pygame.draw.circle(screen, COLOR_AGENT, (ac*CELL_SIZE+OFFSET_X+CELL_SIZE//2, ar*CELL_SIZE+OFFSET_Y+CELL_SIZE//2), CELL_SIZE//2 - 2)

        # Draw Mouse Highlight
        mx, my = pygame.mouse.get_pos()
        hr = (my - OFFSET_Y) // CELL_SIZE
        hc = (mx - OFFSET_X) // CELL_SIZE
        if 0 <= hr < ROWS and 0 <= hc < COLS:
            color = (0, 255, 0) if maze[hr][hc] == 0 else (255, 0, 0)
            pygame.draw.rect(screen, color, (hc*CELL_SIZE+OFFSET_X, hr*CELL_SIZE+OFFSET_Y, CELL_SIZE, CELL_SIZE), 3)

        # INSTRUCTION BOX
        ui_bg = pygame.Surface((500, 180))
        ui_bg.fill((0, 0, 0))
        screen.blit(ui_bg, (20, 20))
        pygame.draw.rect(screen, (255, 255, 0), (20, 20, 500, 180), 3)
        
        texts = [
            "PLACEMENT MODE ACTIVE",
            "-------------------------------",
            "LEFT CLICK  : Move Agent (Cyan)",
            "RIGHT CLICK : Move Exit (Gold)",
            "ENTER KEY   : START EPISODE",
            "R KEY       : New Random Maze"
        ]
        for i, txt in enumerate(texts):
            col = (255, 255, 0) if i == 0 else (255, 255, 255)
            screen.blit(font_md.render(txt, True, col), (40, 40 + i * 25))

        pygame.display.flip()
        clock.tick(60)
        continue

    # =================================================
    # STATE 3: PLAYING (Simulation)
    # =================================================
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: running = False
            if event.key == pygame.K_h: show_hint = not show_hint
            if event.key == pygame.K_t: 
                is_test_mode = not is_test_mode
                agent.epsilon = 0.0 if is_test_mode else 0.5
            if event.key == pygame.K_UP: game_speed += 30
            if event.key == pygame.K_DOWN: game_speed = max(30, game_speed - 30)

    # ... inside the main loop ...

    # AI LOGIC
    r, c = state
    valid = []
    if r > 0 and maze[r-1][c] == 0: valid.append(0)
    if r < ROWS-1 and maze[r+1][c] == 0: valid.append(1)
    if c > 0 and maze[r][c-1] == 0: valid.append(2)
    if c < COLS-1 and maze[r][c+1] == 0: valid.append(3)
    if not valid: valid = [0,1,2,3]

    action = agent.get_action(state, valid_moves=valid)
    dr, dc = {0:(-1,0), 1:(1,0), 2:(0,-1), 3:(0,1)}[action]
    nr, nc = r+dr, c+dc
    
    reward = 0
    done = False
    next_s = state
    
    # Calculate Distances
    dist_old = get_distance((r, c), goal)
    dist_new = get_distance((nr, nc), goal)

    # 1. CRASH (Hit Wall)
    if not (0 <= nr < ROWS and 0 <= nc < COLS) or maze[nr][nc] == 1:
        reward = -50          # MASSIVE PENALTY for hitting walls
        stats["walls"] += 1
        stats["score"] -= 50
        next_s = state        # Stay put
    
    # 2. SUCCESS (Goal)
    elif (nr, nc) == goal:
        reward = 5000         # JACKPOT
        stats["score"] += 5000
        stats["result"] = "SUCCESS"
        done = True
        next_s = (nr, nc)
        
    # 3. MOVE (Step)
    else:
        # Base cost of living (Time is money!)
        reward = -5 
        stats["steps"] += 1
        stats["score"] -= 5
        
        # LOGIC: Is this a NEW tile?
        if (nr, nc) not in visited_episode:
            visited_episode.add((nr, nc))
            stats["explore"] += 1
            
            # SUB-LOGIC: Is it getting CLOSER?
            if dist_new < dist_old:
                reward += 200     # MASSIVE REWARD: "Good Job! Closer!"
                stats["score"] += 200
            else:
                reward += 20      # SMALL REWARD: "Okay, new tile, but wrong way."
                stats["score"] += 20
                
        # LOGIC: Repeating a tile?
        else:
            reward -= 50          # MASSIVE PENALTY: "Stop walking in circles!"
            stats["score"] -= 50

        next_s = (nr, nc)

    if not is_test_mode:
        agent.learn(state, action, reward, next_s, done)
    
    state = next_s
    if done: game_state = "DASHBOARD"
    # RENDERING
    screen.fill(COLOR_BG)
    for r in range(ROWS):
        for c in range(COLS):
            x, y = c * CELL_SIZE + OFFSET_X, r * CELL_SIZE + OFFSET_Y
            if maze[r][c] == 1:
                pygame.draw.rect(screen, COLOR_WALL_SIDE, (x, y+5, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, COLOR_WALL_TOP, (x, y, CELL_SIZE, CELL_SIZE))
            else:
                q_val = np.max(agent.q_table[r, c])
                bright = max(0, min(255, int((q_val + 50) * 2))) 
                col = (0, bright, 0) if bright > 50 else COLOR_PATH
                pygame.draw.rect(screen, col, (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, (30,30,35), (x, y, CELL_SIZE, CELL_SIZE), 1)

    if show_hint and solution_path:
        for i in range(len(solution_path)-1):
            r1, c1 = solution_path[i]
            r2, c2 = solution_path[i+1]
            p1 = (c1*CELL_SIZE + OFFSET_X + CELL_SIZE//2, r1*CELL_SIZE + OFFSET_Y + CELL_SIZE//2)
            p2 = (c2*CELL_SIZE + OFFSET_X + CELL_SIZE//2, r2*CELL_SIZE + OFFSET_Y + CELL_SIZE//2)
            pygame.draw.line(screen, (255, 50, 50), p1, p2, 3)

    gr, gc = goal
    pygame.draw.rect(screen, COLOR_GOAL, (gc*CELL_SIZE+OFFSET_X+5, gr*CELL_SIZE+OFFSET_Y+5, CELL_SIZE-10, CELL_SIZE-10))
    ar, ac = state
    pygame.draw.circle(screen, COLOR_AGENT, (ac*CELL_SIZE+OFFSET_X+CELL_SIZE//2, ar*CELL_SIZE+OFFSET_Y+CELL_SIZE//2), CELL_SIZE//2 - 2)

    # UI PANEL
    ui_bg = pygame.Surface((350, 200)) # Larger box
    ui_bg.fill((0, 0, 0)) 
    screen.blit(ui_bg, (10, 10))
    pygame.draw.rect(screen, (0, 255, 255), (10, 10, 350, 200), 2)
    
    speed_x = game_speed / 60.0
    mode_txt = "TESTING (BRAIN)" if is_test_mode else "TRAINING (LEARN)"
    mode_col = (0, 255, 255) if is_test_mode else (255, 100, 100)
    
    controls = [
        f"SPEED: {speed_x:.1f}x",
        f"SCORE: {stats['score']}",
        f"MODE:  {mode_txt}",
        "---------------------",
        "[T] Toggle Brain/Train",
        "[H] Toggle Hint Path",
        "[UP/DOWN] Speed",
        "[ESC] Quit"
    ]
    for i, txt in enumerate(controls):
        c_color = mode_col if "MODE" in txt else (0, 255, 0) if "SPEED" in txt else (200, 200, 200)
        screen.blit(font_sm.render(txt, True, c_color), (25, 25 + i * 22))

    pygame.display.flip()
    if game_speed < 1000: clock.tick(game_speed)

pygame.quit()
sys.exit()