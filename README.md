# AgentX-Tech-Divas-ps2
# AgentX: Adaptive Maze Runner (Gamified RL Simulation)

### 🚩 Problem Statement Chosen
**Problem Statement 2: Gamified Learning Environment for AgentX**
We have developed a high-fidelity simulation where an autonomous agent (**AgentX**) is placed in a complex, grid-based maze environment. The goal is to demonstrate intelligent behavior through evolved navigation strategies, using a reward-based economy to drive decision-making without manual reprogramming.

---

### 🧠 Approach Overview
The project implements a **Value-Based Reinforcement Learning** system utilizing the **Q-Learning** algorithm.

#### 1. The Agent (AgentX)
* **Observation**: The agent perceives its environment as a set of discrete coordinates $(r, c)$.
* **Action Space**: The agent can perform four discrete actions: Move **UP, DOWN, LEFT,** or **RIGHT**.
* **Memory (Q-Table)**: AgentX maintains an internal table where it stores and updates the "quality" (Q-value) of every possible action in every possible state.

#### 2. The Environment
* **Gamified Grid**: A $15 \times 15$ maze featuring purple obstacles and a high-value Green Goal.
* **Camera Manager**: A dynamic viewport that centers on the agent, providing a focused, immersive experience and allowing for larger world exploration.
* **Reward Economy**:
    * **Success (+100)**: Reaching the target.
    * **Collision Penalty (-10)**: Hitting a wall.
    * **Living Tax (-1)**: Every move costs a point, forcing the agent to find the *shortest* path.

#### 3. The Flow
1. **Exploration**: Initially, AgentX takes random actions to discover the environment (high Epsilon).
2. **Learning**: After every step, the agent updates its Q-Table based on the reward received.
3. **Exploitation**: Over time, the agent's randomness decays, and it begins to rely on its "learned" knowledge to navigate perfectly.



---


🛠️ Execution Instructions
Add this section to your README.md to guide the researchers through the process:

Execution Guide
Follow these steps to set up and run the AgentX simulation on your local machine.

1. Prerequisites
Ensure you have Python 3.8+ installed. You can verify this by running:

Bash

python --version
2. Set Up a Virtual Environment (Optional but Recommended)
It is best practice to run the project in an isolated environment to avoid conflicts with other libraries:

Bash

# Create the environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (Mac/Linux)
source venv/bin/activate
3. Install Required Libraries
Install the core dependencies (Pygame for the engine and NumPy for the Q-table math):

Bash

pip install pygame numpy
Note: If you have a requirements.txt file, you can simply run pip install -r requirements.txt.

4. Launch the Agent
Run the main script to start the learning simulation:

Bash

python main.py
🎮 In-Simulation Controls
Once the window opens, use these keys to interact with the environment:

+ / -: Adjust the Time Speed Multiplier (x0.1 to x10.0) to speed up training or slow down for analysis.

ESC: Safely exit the simulation.
