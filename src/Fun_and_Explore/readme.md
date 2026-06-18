# Fun and Explore

This project demonstrates how a physical maze can be transformed into a digital representation and analyzed using graph-based pathfinding algorithms. Participants can create a digital twin of their maze from a photograph and then explore shortest-path planning techniques.

## Setup

Create and activate a Python virtual environment:

```bash
python -m venv venv_schueler
source venv_schueler/bin/activate
pip install -r requirements.txt
```

## Workflow

1. Take a photograph of your maze and save it as `Maze` (any common image format is supported).

   > **Important:**
   > Crop the image so that only the maze is visible. Additional objects, backgrounds, or large borders may interfere with the graph generation process. Examples can be found in the `Picture Example` folder.

2. Run 

   ```bash 
   python Erzeugen_Digital_Twin.py
   ```

   to generate a graph-based digital twin of the maze.

3. Run

   ```bash
   python Dijkstra_Multiple_Points.py
   ```

   to calculate and visualize the shortest path between multiple points within the maze.

   To view all available command-line arguments and configuration options, run:

   ```bash
   python Dijkstra_Multiple_Points.py -h
   ```
