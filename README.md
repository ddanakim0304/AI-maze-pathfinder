# Pygame Maze Solving Simulation with A* Algorithm

## Overview

This project is a Pygame-based simulation that demonstrates the rational behavior of a maze-solving agent using the A* (A-star) search algorithm. The simulation simplifies the classic Micromouse problem and was developed as part of an academic assignment.

## How It Works

- The maze is randomly generated using a depth-first search algorithm, and the starting position is chosen randomly from one of the four corners, with the goal set at the center.
- The **A* search algorithm** is used to find the optimal path. It uses a priority queue (implemented with a heap) to explore cells efficiently by calculating `Fn = Gn + Hn`, where:
  - `Gn` is the actual cost from the start to the current cell.
  - `Hn` is the heuristic estimate (Manhattan distance) from the current cell to the goal.

## Visualization

- **Visited Cells:** Yellow cells represent cells that have been visited, and their `Fn` values have been calculated.
- **Frontier Cells:** Purple cells represent the frontier—cells adjacent to visited ones that haven’t been explored yet.
- **Optimal Path:** The blue path shows the current best path from the start to the most recently explored cell. This path is updated dynamically whenever a better route is found.

## Path Construction

Once the goal cell is selected from the frontier, the algorithm backtracks from the goal to the start to construct the final optimal path, shown in blue. This ensures the path is dynamic and updates if a better route is found during the search process.

## Final Result

The final blue path represents the optimal solution found using the A* algorithm. 

## Demo

You can watch a demo of the simulation on YouTube: [Maze Solving Simulation Demo](https://youtu.be/vsP_LOAWR_Q)

## Requirements

- Python 3.x
- Pygame

## Installation

1. Clone this repository.
2. Install the dependencies using:
    ```bash
    pip install pygame
    ```
3. Run the simulation:
    ```bash
    python maze_simulation.py
    ```

## License

This project is licensed under the MIT License.

## Acknowledgements

This project was created as part of an academic assignment for demonstrating maze-solving behavior using A* search.

