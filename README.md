# Python Solving NP Problems Using Genetic Algorithm

Exploring different ways of solving NP-Hard problems using genetic algorithms.
[This is a repo of few experiments done to figure out different/better ways of crossovers, mutations and representation of inputs in genetic algorithms.]  

## Travelling Salesman Problem  
Dynamic programming solution runtime: O((n^2)*(2^n))  
Genetic Programming solution runtime: O(m*(nlogn)) (where m is the maximum number of generations)   

For n = 20 points, Dynamic Programming solutions take about 2-3 mins to run, whereas the Genetic Programming solutions only take about a few seconds and give a solution that is + or - 50 of the optimal solution.

TSP TODO:
- Specific starting and ending points
- plot of graph of no. of generations vs optimal solutions range

Overall TODO:
- Plot graphs for various crosover methods and their solutions.
- try solving other NP-[X] algos!

References(so far):  
http://ijcopi.org/ojs/index.php?journal=ijcopi&page=article&op=download&path%5B%5D=44&path%5B%5D=80  
http://www.ceng.metu.edu.tr/~ucoluk/research/publications/tsp.pdf  
