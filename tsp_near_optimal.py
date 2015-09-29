import random
import math
import itertools
import copy
import matplotlib.pyplot as plt

def length(p1,p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def solve_tsp_dynamic(points):
    #calc all lengths
    all_distances = [[length(x,y) for y in points] for x in points]
    #initial value - just distance from 0 to every other point + keep the track of edges
    A = {(frozenset([0, idx+1]), idx+1): (dist, [0,idx+1]) for idx,dist in enumerate(all_distances[0][1:])}
    cnt = len(points)
    for m in range(2, cnt):
        B = {}
        for S in [frozenset(C) | {0} for C in itertools.combinations(range(1, cnt), m)]:
            for j in S - {0}:
                B[(S, j)] = min( [(A[(S-{j},k)][0] + all_distances[k][j], A[(S-{j},k)][1] + [j]) for k in S if k != 0 and k!=j])  #this will use 0th index of tuple for ordering, the same as if key=itemgetter(0) used
        A = B
    res = min([(A[d][0] + all_distances[0][d[1]], A[d][1]) for d in iter(A)])
    return res[1]

num_points = 10 # do not put large values - too much memory
max_point = 20
points = [[random.randint(1,max_point),random.randint(1,max_point)] for i in range(num_points)]
#print points
sol = solve_tsp_dynamic(points)
#print sol



#point_list = points
point_list = [
[60,200],
[180,200],
[80,180],
[140,180],
[20,160],
[100,160],
[200,160],
[140,140],
[40,120],
[100,120],
[180,100],
[60,80],
[120,80],
[180,60],
[20,40],
[100,40],
[200,40],
[20,20],
[60,20],
[160,20]
]
class chromozome:
    global point_list #list of [x,y] points
    def __init__(self,travel_order = [],random = True):
        self.list_len = len(point_list)
        #self.crossover = str_len/2 #default crossover is at mid of the string
        self.random = random
        self.travel_order = travel_order
        if self.random:
            #print "str set as random"
            self.travel_order = self.randomize()

    def randomize(self):
        #randomly generate a path using the given point_list
        #lis = range(0,self.list_len) #generes an array of 1..n #does not give optimal for 0 to nth path(read below)
        lis = range(1,self.list_len-1)
        #print lis
        random.shuffle(lis)
        return lis
    def get_len(self):
        return len(self.travel_order)
    def get_list(self):
        return self.travel_order

    def mate(self,parent2):
        #print "parent1:",self.travel_order
        #print "parent2:",parent2
        child1 = [-1]*len(self.travel_order)
        child2 = [-1]*len(self.travel_order)
        random_break_point1,random_break_point2 = 0,0
        while random_break_point2==random_break_point1:
            random_break_point1 = random.randint(1,len(self.travel_order)-2)
            #print random_break_point1
            random_break_point2 = random.randint(len(self.travel_order)-random_break_point1-1,len(self.travel_order)-2)
            #print random_break_point2
        start = min(random_break_point1,random_break_point2)
        end = max(random_break_point1,random_break_point2)

        #print "after filling only mid:"
        child1[start:end+1] = self.travel_order[start:end+1]
        #print child1
        child2[start:end+1] = parent2[start:end+1]
        #print child2

        #completing child1:
        filled = abs(start-end)+1
        not_filled = len(self.travel_order)-filled
        temp_start_child = end+1
        temp_start_parent = end+1
        #print "to be filled:",not_filled
        while not_filled > 0:
            temp_start_child = temp_start_child % len(self.travel_order)
            temp_start_parent = temp_start_parent % len(self.travel_order)

            if parent2[temp_start_parent] not in child1:
                child1[temp_start_child] = parent2[temp_start_parent]
                temp_start_child+=1
                not_filled-=1
            temp_start_parent+=1
        #print "after filling all:"
        #print child1

        not_filled = len(self.travel_order)-filled
        temp_start_child = end+1
        temp_start_parent = end+1
        #print "to be filled:",not_filled
        while not_filled > 0:
            temp_start_child = temp_start_child % len(self.travel_order)
            temp_start_parent = temp_start_parent % len(self.travel_order)

            if self.travel_order[temp_start_parent] not in child2:
                child2[temp_start_child] = self.travel_order[temp_start_parent]
                temp_start_child+=1
                not_filled-=1
            temp_start_parent+=1
        #print "after filling all:"
        #print child2
        #print len(child1),len(child2)
        return [chromozome(child1,False),chromozome(child2,False)]

    def mutate(self,chance):
        if random.random() < chance:
            randinex1 = random.randint(0,len(self.travel_order)-1)
            randinex2 = random.randint(0,len(self.travel_order)-1)
            self.travel_order[randinex2],self.travel_order[randinex1] = self.travel_order[randinex1],self.travel_order[randinex2]

class evolve:

    def __init__(self,point_list,max_generation):
        self.final = []
        #print self.final.get_str() ,"IS THE FINAL"
        self.start = chromozome()

        self.population = []

        self.max_generation =max_generation
        self.point_list = point_list
        self.populate()

    def length(self,p1,p2):
        return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

    def calculate_fitness(self,gene):
        #calculate the total of travelling in the given order
        gene_copy = copy.deepcopy(gene)
        gene_copy.append(max(gene)+1)
        gene_copy = [0]+gene_copy
        #print "gene:",gene_copy
        cost = 0
        for i in range(len(gene_copy)-1):
            cost += self.length(self.point_list[gene_copy[i]],self.point_list[gene_copy[i+1]])
        return cost

    def populate(self,n=30):
        #fill the population randomly
        #self.population.append(self.start)
        while n > 1:
            self.population.append(chromozome())
            n-=1


    def sort_by_cost(self):
        self.population = sorted(self.population,key = lambda x:self.calculate_fitness(x.get_list()))


    def print_str(self,population,print_len,print_all=False):
        print "-"*50
        if print_all:
            print_len = len(population)-1
        for x in population[0:print_len]:
            print x.get_str(),"len:   ",x.get_len(),"     Cost:",self.cost(x)
        print "-"*50

    def start_evolving(self):
        #each iteration, sort the population by cost and mate the top 2 members and put the children in back in the list by removing the bottom 2 members(highest cost)
        #and call this function recursively
        #print "before loop"
        #self.print_str(self.population,0,True)
        while self.max_generation > 0:
            self.sort_by_cost()
            childrenAB = self.population[0].mate(self.population[1].get_list())
            #childrenAB is a list of [childA,childB]
            self.population[len(self.population)-2:] = childrenAB

            for index in range(len(self.population)):
                #mutate it and check the cost
                #print "->",self.population[index]
                self.population[index].mutate(0.15) #mutate with a % chance
            self.max_generation -= 1
        print "lowest cost path after n generations:",[0]+self.population[0].get_list()+[19]
        print "lowest cost is:",self.calculate_fitness(self.population[0].get_list())
        return self.population[0].get_list()
        
e = evolve(point_list,1000)
sol = e.start_evolving()

actual_path = [point_list[x] for x in sol]


#optimal_sol = solve_tsp_dynamic(point_list)   #842.833082597 is the optimal solution
#print optimal_sol #[0, 4, 8, 11, 14, 17, 18, 15, 12, 19, 16, 13, 10, 6, 1, 3, 7, 9, 5, 2]

print "near-optimal solution:",sol,
print "cost:",e.calculate_fitness(sol)
