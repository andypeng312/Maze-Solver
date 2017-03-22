# README
## Description of Project
This is an app that draws a maze using a user-selected maze generation
algorithm. The maze then solves the maze using a user-selected maze solving
algorithm.

The maze is displayed using the PyGame module and as the program is solving, an
animated blue dot traces a red path through the maze. When it finds the end of
the maze the shortest path found is highlighted in green.

Currently the maze generation algorithms that are available are:
<ol start="0">
  <li> Binary tree algorithm</li>
  <li> Depth-first search starting from upper right corner</li>
  <li> Depth-first search starting from random location</li>
  <li> Kruskal's algorithm</li>
  <li> Prim's algorithm starting from upper right corner</li>
  <li> Prim's algorithm search starting from random location</li>
</ol>

The maze solving algorithms are:
<ol start="0">
  <li> Depth-first search</li>
  <li> A*</li>
</ol>

To run the program:
1. Run `maze.py` or `OOP_maze.py`
2. The python program will prompt for a maze generation algorithm. Indicate
the desired algorithm by typing it's list index from the above section and
pressing the enter key
3. The python program will prompt for a maze solving algorithm. Indicate
the desired algorithm by typing it's list index from the above section and
pressing the enter key

## Contents
* **`maze.py`**- an older version of the program
* **`OOP_maze.py`**- a newer version of the program that uses Python classes
and inheritance
* **`screen_recording`**- contains a screen recording of the maze solver in
action
---
**Technologies Used:** Python, Object-oriented programming, PyGame, Graph
algorithms, Graph search algorithms
**Estimated Lines of Code:** 600

![](/screen_recording/screen_recording.gif)
Generating algorithm: 1, Solving algorithm: 0