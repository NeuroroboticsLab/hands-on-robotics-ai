# Maze Navigation Task

The purpose of this task is to introduce participants to the fundamentals of algorithmic decision-making and logical problem-solving. Participants are required to implement the navigation logic that enables the robot to successfully traverse a maze. By developing and refining this logic, they will gain experience in working with conditions, control flow, and autonomous robot behavior. In the logic files, additional information about the required functionality and implementation details is provided.

## Contents

* `logic.c` – Reference implementation containing the correct navigation logic for the maze.
* `Student File/logic_students.c` – Template file containing the function definition that participants must complete.
* `logic_students.c` – File containing a participant's custom maze-solving implementation.
* `maze.c` – Main program implementation. This file should not be modified by participants.
* `weights.c` – Weight matrix used by the maze task. This file should not be modified by participants.

## Usage

Compile and upload the program using one of the following commands:

```bash
make program
```

Uploads the participant version using `logic_students.c`.

```bash
make program SOLUTION=1
```

Uploads the reference implementation using the navigation logic defined in `logic.c`.
