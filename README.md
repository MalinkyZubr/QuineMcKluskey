# QuineMcKluskey.py
## Background
The Quine McKluskey algorithm is a standard mathematical process for minimizing large logical expressions, often involving tens of inputs that would be far too complex to be simplified efficiently using karnaugh maps or boolean algebra techniques. The Quine McKluskey algorithm takes a recursive, tabular approach to the problem, and scales up much more effectively to large digital circuits.


If you want to learn more about the algorithm, [this](https://youtu.be/l1jgq0R5EwQ) is the video I watched to learn about it. Neso Academy explains it in a straightforward, step by step way making it very easy to follow!


## Usage
The program is a simple command line utility which takes the path to a CSV file. Example CSV files are stored in ./example_tables. Each table can have an arbitrary number of input and output columns. Each column should have a single character as its headers. Listed below are reserved characters which may not be used as input headers.

### Illegal Input Header Characters

| Character | Reason                                                         |
|-----------|----------------------------------------------------------------|
| O         | Delineates output column                                       |
| !         | Represents logical not in output                               |
| ~         | Alternative representation of logical not (would be confusing) |
| &\|       | Boolean symbols (would be confusing)                           |
| ()        | Parentheses used for grouping by program                       |
| +         | represents an "or" condition in program                        |
| *         | Commonly used to represent and (would be confusing)            |


Each table will consist of two types of columns: input and output columns.
* Input columns contain boolean inputs, they can be headed by any character except those listed above
* Output columns contain output values. They must **ALL** be headed by O (capital o). For multiple outputs, number the headers: O1, O2, etc.


In cases where multiple outputs are specified, a separate expression will be generated from inputs for each output.


