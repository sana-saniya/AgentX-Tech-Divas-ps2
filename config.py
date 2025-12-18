# config.py
import pygame

# --- SCREEN & GRID ---
# We will use your full desktop resolution dynamically in main.py
# These control the logic grid size (Keep as Odd numbers for best results)
COLS = 31 
ROWS = 21

# --- CYBERPUNK COLORS ---
COLOR_BG = (10, 10, 20)           # Deep dark blue
COLOR_WALL_TOP = (0, 255, 136)    # Neon Green
COLOR_WALL_SIDE = (0, 150, 80)    # Darker Green (3D side)
COLOR_PATH = (40, 40, 50)         # Dark Floor
COLOR_AGENT = (0, 255, 255)       # Cyan Agent
COLOR_GOAL = (255, 215, 0)        # Gold Goal