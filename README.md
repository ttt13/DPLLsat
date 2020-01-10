# DPLLsat

An implementation of the Davis-Putnam-Logemann-Loveland (DPLL) algorithm for the satisfiability (SAT) problem. This algorithm takes a logical statement that is in Conjunctive Normal Form (CNF) as input and outputs an assignment of true or false to each propositional symbol.

## Conjunctive Normal Form
A boolean expression that is written in CNF consists of:
* Clauses joined by AND.
* Each clause consists of literals joined by OR.
* Each literal is only a positive literal or a negative literal (a literal preceded by NOT). 

## Definitions
**Unit clause**: A clause with only one literal.
**Empty clause**: A clause with no literals.
**Pure literal**: A literal is pure if it always has the same sign (positive or negative) in every clause. 

## Using DPLL to solve a satisfiability problem
The motivation for an SAT solver is to determine if there is a possible assignment of true and false to a boolean formula, such that the entire formula evaluates to true. 

There are three main components to the DPLL algorithm: recursive backtracking, unit clause propagation, and pure literal propagation.

### Recursive backtracking
The algorithm picks some variable to branch on. It guesses the variable to be true, then recursively determines if the subproblem is satisfiable. If the subproblem is unsatisfiable, the algorithm guesses the variable to be false and tries again.

### Unit clause propagation
If a clause is a unit clause, the only way for the formula to be satisfiable is for that variable to be consistently assigned with its sign in that clause. Using this knowledge, we know that variable must take on that assignment, so any clause with that literal are also satisfied. Additionally, clauses that contain the negation of the literal can also be removed .

### Pure literal elimination
If a literal is pure, then any clause that it appears in can be satisfied by assigning the variable consistent to the sign it appears with.

## Output specification and testing
The program will print "UNSAT" if the formula is unsatisfiable and "SAT" if it is satisfiable. If verbosity is set to true, the program will also print the list of true literals if the formula is satisfiable.

To test the algorithm, use the following command:

``` python DPLLsat.py -i <inputCNFfile>
```
or
``` python DPLLsat.py -i <inputCNFfile> -v ```
if you want to see the solution.
