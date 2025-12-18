import numpy as np
import random

class Agent:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.q_table = np.zeros((rows, cols, 4))
        
        # --- SPEED RUNNER SETTINGS ---
        self.learning_rate = 0.7    # High, but stable
        self.discount_factor = 0.99 # Maximum focus on the Goal
        self.epsilon = 1.0          # Start curious...
        self.epsilon_decay = 0.80   # ...but get smart VERY fast (was 0.90)
        self.min_epsilon = 0.01

    def get_action(self, state, valid_moves=None):
        r, c = state
        
        # 1. EXPLORE: Random action
        if np.random.rand() < self.epsilon:
            if valid_moves:
                return random.choice(valid_moves)
            return random.randint(0, 3)
            
        # 2. EXPLOIT: Choose best known action
        else:
            # Add tiny noise to break ties if values are equal
            values = self.q_table[r, c] + np.random.uniform(0, 1e-5, 4)
            return np.argmax(values)

    def learn(self, state, action, reward, next_state, done):
        r, c = state
        nr, nc = next_state
        
        old_value = self.q_table[r, c, action]
        
        if done:
            future_reward = 0
        else:
            future_reward = np.max(self.q_table[nr, nc])
            
        # Bellman Equation
        new_value = old_value + self.learning_rate * (reward + self.discount_factor * future_reward - old_value)
        self.q_table[r, c, action] = new_value

    def decay_epsilon(self):
        """Reduce randomness over time"""
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)