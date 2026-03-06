# Simulated Paint Spraying on a Wall Mesh with Isaac Warp and OpenUSD

## Overview

A simulation that demonstrates spray painting a vertical wall surface. The simulation models a spray nozzle emitting paint in a triangular fan pattern and updates the wall surface over time to reflect paint accumulation.

## Scenario

- A single vertical cuboid mesh represents the wall
- A spray nozzle moves in front of the wall
- The spray has a triangular fan pattern with configurable parameters
- Over time, paint accumulates where the spray impacts the wall

## Project Structure
```
config.py          - Configurable spray parameters
wall.py            - Task 1: Cuboid wall mesh (OpenUSD)
spray.py           - Task 2: Spray simulation (Isaac Warp kernels)
paint.py           - Task 3: Paint accumulation
nozzle_path.py     - Task 5: Nozzle animation path
main.py            - Task 4: Visualization and main simulation
```

## Installation
```bash
pip install warp-lang
pip install usd-core
pip install numpy
```

## How to Run
```bash
python3 main.py
```

## View Results
```bash
usdview output/wall_initial.usda
usdview output/wall_midway.usda
usdview output/wall_final.usda
usdview output/spray_animation.usda
```

Press 4 in usdview to remove wireframe, then click Play for animation.

## Screenshots

### Initial State (before spraying)
![Initial](screenshots/initial.png)

### Intermediate Step
![Midway](screenshots/midway.png)

### Final Fully Painted Wall
![Final](screenshots/final.png)

### Animation Video
[Screencast from 03-06-2026 08:46:48 PM.webm](https://github.com/user-attachments/assets/790f0d30-d924-4dab-8a2a-2af74680c3ae)



