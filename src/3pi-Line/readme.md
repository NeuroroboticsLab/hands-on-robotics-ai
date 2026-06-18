# Line Following Task

The purpose of this task is to provide a basic understanding of how AI systems make decisions. Participants will adjust the ten weights that connect the robot's sensors to its motors by trail-and-error. The values should be between 10 and 100, otherwise there will be no or incorrect behaviour. By modifying these weights, they can influence the robot's behavior and observe how different configurations affect its ability to follow a line.

## Contents

* `weights.c` – Definition of the weight matrix used in the reference solution.
* `Student File/weights_students.c` – Template file containing a weight matrix initialized with zeros.
* `weights_students.c` – File containing a participant's custom weight matrix.
* `line.c` – Main program implementation. This file should not be modified by participants.

## Usage

Compile and upload the program using one of the following commands:

```bash
make program
```

Uploads the participant version using `weights_students.c`.

```bash
make program SOLUTION=1
```

Uploads the reference implementation using the predefined weight matrix from `weights.c`.
