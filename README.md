# AgentX: Adaptive Maze Runner (Gamified RL Simulation)

> **Play it live →** `https://<your-github-username>.github.io/AgentX-Tech-Divas-ps2/`  
> *(URL becomes active after your first push to `main` and GitHub Pages is enabled)*

---

### 🚩 Problem Statement
**Problem Statement 2: Gamified Learning Environment for AgentX**  
An autonomous agent (AgentX) navigates a complex cyberpunk maze using Q-Learning reinforcement learning — demonstrating intelligent behavior through evolved navigation strategies and a reward-based economy.

---

### 🧠 Approach

**Value-Based Reinforcement Learning using Q-Learning**

- **Observation**: Agent perceives discrete grid coordinates (r, c)
- **Action Space**: UP, DOWN, LEFT, RIGHT
- **Memory (Q-Table)**: Stores and updates quality values for every state-action pair
- **Reward Economy**:
  - `+5000` — Reaching the goal
  - `+200` — New tile, moving closer to goal
  - `+20`  — New tile, moving away from goal
  - `-5`   — Each step taken (time cost)
  - `-50`  — Hitting a wall
  - `-50`  — Revisiting a tile (anti-loop penalty)

---

### 🎮 Controls

| Key | Action |
|-----|--------|
| `T` | Toggle Training / Testing mode |
| `H` | Toggle hint path overlay |
| `↑ / ↓` | Increase / decrease simulation speed |
| `SPACE` | Continue to next episode (on dashboard) |
| `R` | Generate new random maze (in placement mode) |
| `ENTER` | Start episode (in placement mode) |
| `ESC` | Quit |

---

### 🚀 Hosting — GitHub Pages via Pygbag (WebAssembly)

This project is compiled to WebAssembly using [Pygbag](https://pygame-web.github.io/) and hosted free on GitHub Pages.

#### One-time GitHub setup (do this once):

1. Push this repo to GitHub:
   ```bash
   git add .
   git commit -m "initial commit"
   git push origin main
   ```

2. Go to your repo on GitHub → **Settings** → **Pages**

3. Under **Source**, select **GitHub Actions**

4. That's it. The workflow in `.github/workflows/deploy.yml` will automatically build and deploy on every push to `main`.

5. Your live URL will be:
   ```
   https://<your-github-username>.github.io/AgentX-Tech-Divas-ps2/
   ```

#### Run locally (optional):

```bash
# Install dependencies
pip install pygame==2.5.2 numpy==1.26.4 pygbag==0.9.2

# Run locally in browser (opens at http://localhost:8000)
pygbag .

# Or run as a normal desktop app
python main.py
```

---

### 🛠️ Local Desktop Setup

```bash
# Clone the repo
git clone https://github.com/<your-username>/AgentX-Tech-Divas-ps2.git
cd AgentX-Tech-Divas-ps2

# Optional: create a virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

---

### 📁 Project Structure

```
AgentX-Tech-Divas-ps2/
├── main.py          # Game loop (async, pygbag-compatible)
├── agent.py         # Q-Learning agent
├── config.py        # Grid size, colors
├── requirements.txt # Python dependencies
├── favicon.png      # Browser tab icon
└── .github/
    └── workflows/
        └── deploy.yml   # Auto-deploy to GitHub Pages
```
