# KAKURO SOLVER USING CSP

Kakuro is a kind of logic puzzle that is often referred to as a mathematical transliteration of the crossword. Each puzzle consists of a blank grid with sum-clues in various places. The objective is to fill all empty squares using numbers 1 to 9 so the sum of each horizontal block equals the clue on its left, and the sum of each vertical block equals the clue on its top. In addition, no number may be used in the same block more than once. Lack of duplication of any entry makes creating Kakuro puzzles with unique solutions possible.

The goal of this project is to implement a Kakuro solver that treats the puzzle as a constraint satisfaction problem.

![Puzzle](https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Kakuro_black_box.svg/1024px-Kakuro_black_box.svg.png)    ![Solution](https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Kakuro_black_box_solution.svg/1024px-Kakuro_black_box_solution.svg.png)


## Formulation of Kakuro puzzle as a constraint satisfaction problem

Variables : Blocks which are to be filled by digits 1 to 9 (can be represented by X<small> i,j</small> where i,j are the row and column number respectively). <br />
Domain of X<small> i,j</small> : { 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 } <br />
Constraints : Sum of different variables equal to its respected clue according to puzzle ( Example : X<small> 2,2</small> + X<small> 2,3</small> = 16 in the above puzzle ) <br />
These contraints contains n variables where n can vary. First we have to convert n-ary constraints into binary constraints.

## Conversion of n-ary constraints into binary constraints

We can convert above n-ary constraints into binary constraints by adding a new constraint variable (say U<small>k</small> where k is constraint number) in such a way that domain of U<small>k</small> has permutations of numbers(1 to 9) satisfying constraint k. 
<br />(Eg : In above puzzle X<small> 2,2</small> + X<small> 2,3</small> = 16. Lets add a new constraint variable U1 such that domain of U1 as {(7,9) , (9,7)}
<br />Now constraints are first co-ordinate of U1 is X<small> 2,2</small> and second co-ordinate of U1 is X<small> 2,3</small> which are binary constraints)
<br />

## Arc Consistency 

Two variables X,Y are said to arc consistent (X -> Y) iff for every value x of X there is some allowable value y of Y.
<br />Intially arcList is prepared which contains pairs of variables of all binary constraints and AC3 algorithm is applied by which we can reduce our variable domains by removing inconsistent values according to arc consistency.

## Generic Backtracking Search

In this backtracking search all unassigned variables will be assigned values. While assigning a value to a unassigned variable , we have to check whether this has no conflicts with previously assigned variables. If there is no conflict then continue calling Backtracking search for assigning remaining unassigned variables. But if there is a conflict then backtrack by removing that particular assignment to that variable and try assigning another value for that variable and continue the process until all variables are assigned without any conflicts.

## Backtracing Search using Maintaining Arc Consistency(MAC) 

In addition to generic backtracking search , here we call AC3 after a variable X is assigned a value with arcs (X,Y) for all Y that are unassigned variables that are neighbours of X and if any variable domain reduced to &Phi; AC3 resturns a failure which means there exist conflicts with this assignment so we backtrack and proceed as per generic backtracking search.

## How to execute the codes in this project

* To solve Kakuro using generic backtracking search  :<pre>  $ python3 genericBS.py \<input file path> \<output file path> </pre>

* To solve Kakuro using backtracking search with MAC : <pre>  $ python3 MAC_BS.py \<input file path> \<output file path> </pre>

## Contributors

* 112001009 - A Lakshmi Nikhitha - [github profile](https://github.com/nikhi9603)

* 112001052 - Yukta Salunkhe - [github profile](https://github.com/YuktaS14)
