# City Route Planner (BFS)

**Graph Search & Object-Oriented Design**

## Overview
This project is a command-line city route planner implemented in Python. It models a network of U.S. cities as a graph and uses **Breadth-First Search (BFS)** to find a valid route between a starting city and a destination city. The project was completed as a class assignment to practice graph-based problem solving, object-oriented programming, and search algorithms.

Rather than relying on external libraries or APIs, this project focuses on building the core logic from scratch to demonstrate an understanding of how routing and pathfinding systems work under the hood.



## Key Concepts Demonstrated
- Graph representation using custom Python classes
- Breadth-First Search (BFS) for pathfinding
- Object-oriented design (`City` and `Map` classes)
- Command-line argument parsing with `argparse`
- Structured data modeling using dictionaries and tuples



## How It Works
- Each city is represented as a node in a graph.
- Roads between cities are edges containing distance and interstate information.
- BFS is used to find a path with the **fewest number of city-to-city hops**.
- Once a path is found, step-by-step driving instructions are printed to the console.

> **Note:** BFS minimizes the number of stops, not total mileage. Distances are included for instruction output but are not used to optimize the route.



## Running the Program

From the project directory, run:

```bash
python3 gps.py --starting_city Baltimore --destination_city Miami
