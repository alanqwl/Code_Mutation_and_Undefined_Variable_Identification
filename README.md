# Code_Mutation_and_Undefined_Variable_Identification

## Goal
This project performs various program manipulation with Python abstract syntax tree (AST). The main tasks of the project is to implement code mutation and undefined variable identification. Code mutation is a fundemental technique in software analysis/testing. It insert som e small faults into the original program in order to measure the ability of the test suite to detect them. This technique is widely used in mutation testing. Undefined variable identification aims to identify undefined variables statically (without running the program itself).

## Part 1: Code Mutation
### Mutation Strategies
In the project, the following basic code mutation strategies are used.

  * Negate Binary Operators: $+ \Longleftrightarrow -$, $* \Longleftrightarrow /$
  * Negate Comparison Operators: $>= \Longleftrightarrow <$, $<= \Longleftrightarrow >$
  * Delete Unused Function Definitions

### Input/Output Examples
The input is a string representing a Python code snippet. The output is the mutated program which is printed out in the console. In addition to mutate the program, all global variables are printed at the end of the output program.

Example Input 1:

    x = 1
    def foo1(x):
      y = x - 5
    foo1()

Example Output 1:

    x = 1
    def foo1(x):
      y = x + 5
    foo1()
    print(x)

Example Input 2:

    x = 1
    def foo1():
      x = 1
    def foo2():
      y = 6 + (3>=True)
    foo2()

Example Output 2:

    x = 1
    def foo2():
      y = 6 - (3>=True)
    foo2()
    print(x)

## Part 2: Undefined Variable Identification
In this part of the project, the program takes a string representing a Python code snippet as input. The output would be the number of undefinied variables in the input code.

### Input/Output Examples

Example Input 1:

    x = 1
    x = y + 2

Example Output 1:

    0

Example Input 2:

    x = 1
    def foo(y):
      x = 6
    foo(y)

Example Output 2:

    0

Example Input 3:

    x = 1
    x = y + 2
    z = x + 1

Example Output 3:

    2

Example Input 4:

    x = 1
    x = y + 2
    def foo(x):
      x = x + 1
    def func(z, x, y=6):
      x = y + z
      foo(x)
    func(x, 4, y=5)

Example Output 4:

    3





