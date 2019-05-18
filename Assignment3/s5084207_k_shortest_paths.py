from collections import defaultdict
import operator
from more_itertools import unique_everseen
import string
import random
import copy

class Node:
    def __init__(self, value):
        self.key = value
        self.neighbours = {}

    def add_neighbour(self, node, weight=0):
        self.neighbours[node] = weight

    def get_neighbour(self):
        return self.neighbours

    def get_key(self):
        return self.key

    def get_weight(self, node):
        return self.neighbours[node]

    def __str__(self):
        return str(self.key) + " is directed to " + str([x.key for x in self.neighbours])

class Graph:
    def __init__(self):
        self.node_list = {}
        self.n_size = 0

    def add_vertex(self, value):
        self.n_size += 1
        new_node = Node(value)
        self.node_list[value] = new_node
        return new_node

    def add_edge(self, prev_node, next_node, weight=0):
        if prev_node not in self.node_list:
            self.add_vertex(prev_node)
        if next_node not in self.node_list:
            self.add_vertex(next_node)
        self.node_list[prev_node].add_neighbour(self.node_list[next_node], weight)

    def get_size(self):
        return self.n_size

    def get_vertex(self, node):
        if node in self.node_list:
            return self.node_list[node]
        else:
            return None

    def get_vertices(self):
        return self.node_list.copy()

    def copy_original(self):
        return copy.deepcopy(self)

    def remove_vertex(self, node):
        if node in self.node_list:
            del self.node_list[node.get_key()]

    def __iter__(self):
        return iter(self.node_list.values())

#Wang et al., 2018, Razali and Geraghty, 2011
class GeneticAlgorithm:
    def __init__(self, graph_passed, origin, destination):
        self.graph = graph_passed
        self.g_size = self.graph.get_size()
        self.origin = origin
        self.destination = destination
        self.population = []
        self.pop_size = self.g_size*5
        self.pop_with_fitness = []

    def random_initialisation(self, graph):
        while True:
            curr_node = graph.get_vertex(self.origin)
            #add origin into path
            one_path = list()
            one_path.append(curr_node)
            #randomly select a neighbour
            neighbours = list(curr_node.get_neighbour())
            while neighbours is not None or len(neighbours)!=0:
                rd_selected_neighbour = random.choice(neighbours)
                if rd_selected_neighbour in one_path:
                    neighbours.remove(rd_selected_neighbour)
                if rd_selected_neighbour not in one_path:
                    curr_node = rd_selected_neighbour
                    neighbours = list(curr_node.get_neighbour())
                    one_path.append(curr_node)
                    if curr_node.get_key()==self.destination:
                        return one_path

    #one of initialisation method - Bellman Ford
    def bellman_ford_initialisation(self):
        #initialise graph nodes to infinity except for the origin that has 0
        distance = {string.ascii_uppercase[index+2]: float("inf") for index in range(6)}
        distance[self.origin] = 0
        prev_node = {string.ascii_uppercase[node_key_index+2]: None for node_key_index in range(6)}

        #try all edges v-1 times
        for graph_vertex in range(self.graph.get_size()-1):
            for u in self.graph:
                for v in u.get_neighbour():
                    # print(u.get_key(), v.get_key(), u.get_weight(v))
                    if (distance[u.get_key()] != float("inf")) and (distance[u.get_key()] + u.get_weight(v) < distance[v.get_key()]):
                        distance[v.get_key()] = distance[u.get_key()] + u.get_weight(v)
                        prev_node[v.get_key()] = u.get_key()
        bf_best_path = list()
        bf_best_path.append(self.graph.get_vertex(self.destination))
        curr_node = self.destination
        while curr_node!=self.origin:
            bf_best_path.insert(0,self.graph.get_vertex(prev_node[curr_node]))
            curr_node = prev_node[curr_node]
        return bf_best_path

    #check duplicate returns true or false
    def is_duplicate(self, path, total_population):
        path_keys = [x.get_key() for x in path]
        for pop_path in total_population:
            pop_path_keys = [x.get_key() for x in pop_path]
            if path_keys==pop_path_keys:
                return True
        return False

    #create the number of poplution = 5*graph size
    def initialise_population(self):
        #first parent population Bellman-Ford
        bf_path = self.bellman_ford_initialisation()
        self.population.append(bf_path)
        #rest parents filled with random initialisation
        for num_population in range(self.pop_size-1):
            path = self.random_initialisation(self.graph)
            if not self.is_duplicate(path, self.population):
                self.population.append(path)

    #Wang et al., 2018
    def construct_genepool(self, option):
        #random selection of two parents
        parent1 = random.choice(self.population)
        # print([x.get_key() for x in parent1])
        if option=="crossover":
            parent2 = random.choice(self.population)
        else:
            parent2 = self.random_initialisation(self.graph)
        # print([x.get_key() for x in parent2])
        gene_pool = list(set(parent1).union(parent2))
        #make the list into a graph
        graph = self.graph.copy_original()
        for node in graph:
            if node not in gene_pool:
                graph.remove_vertex(node)
        # print([x.get_key() for x in graph])
        return graph

    def crossover(self):
        for crossover_times in range(len(self.population)):
            gene_pool_graph = self.construct_genepool("crossover")
            # print([x.get_key() for x in gene_pool_graph])
            child = self.random_initialisation(gene_pool_graph)
            # print([x.get_key() for x in child])
            if not self.is_duplicate(child, self.population):
                self.population.append(child)

    def mutation(self, mutant_percent):
        for mutation_times in range(int(mutant_percent*len(self.population))):
            gene_pool_graph = self.construct_genepool("mutation")
            mutant = self.random_initialisation(gene_pool_graph)
            if not self.is_duplicate(mutant, self.population):
                self.population.append(mutant)

    #calculate total distance - addition of weights
    def cal_total_distance(self):
        for path in self.population:
            total_distance = 0
            l_path = len(path)
            path = iter(path)
            curr_node = next(path)
            for length_of_path in range(l_path-1):
                next_node = next(path)
                total_distance += curr_node.get_weight(next_node)
                curr_node = next_node
            self.pop_with_fitness.append(total_distance)

    #sort based on fitness score i.e. addition of weights
    def sort_fit_score(self):
        self.pop_with_fitness, self.population = zip(*[(fitness, path) for fitness, path in sorted(zip(self.pop_with_fitness,  self.population), key=lambda x: x[0])])
        self.pop_with_fitness = list(self.pop_with_fitness)
        self.population = list(self.population)

    # def remove_duplicate(self):
    #     population = []
    #     # print([x.get_key() for path in self.population for x in path])
    #     for path in self.population:
    #         path_key = [x.get_key() for x in path]
    #         population.append(path_key)
    #
    #     # fit_pop = zip(self.pop_with_fitness, population)
    #     # fit_pop_unique = unique_everseen(fit_pop, key=itemgetter(1))
    #     # fitness, pop = zip(*fit_pop_unique)
    #     # self.pop_with_fitness = list(fitness)
    #     # self.population = list(pop)

    #Razali and Geraghty, 2011
    #use tournament strategy if a graph is small
    def tournament_selection(self, tournament_sz, elite_sz):
        # pop_size = len(self.population)
        #best paths from sorted population are preserved for the size of elite
        # pop_fitness, next_population = self.pop_with_fitness[:elite_sz], self.population[:elite_sz]
        next_population = self.population[:elite_sz]

        self.pop_with_fitness = []
        #remaining population is filled with tournament selection
        for num_selection in range(0, self.pop_size - elite_sz):
            #select random paths from sorted population
            in_tournament = random.sample(self.population, tournament_sz)
            in_tournament_population = random.choice(in_tournament)
            if not self.is_duplicate(in_tournament_population, next_population):
                next_population.append(in_tournament_population)
            # in_tournament = random.sample(list(zip(self.pop_with_fitness, self.population)), tournament_sz)
            # in_tournament_fitness, in_tournament_population = zip(*[random.choice(in_tournament)])
            # if not self.is_duplicate(in_tournament_population[0], next_population):
            #     next_population.append(in_tournament_population[0])
            #     pop_fitness.append(int(in_tournament_fitness[0]))
        self.population = next_population
        # print([x.get_key() for path in self.population for x in path])
        self.cal_total_distance()
        # print(self.pop_with_fitness)

    #Razali and Geraghty, 2011
    #use rank-based roulette wheel if a graph is large
    #calculation of ranks for rank-based roulette wheel
    def cal_rank(self):
        # key_fitness = list_fitness_score(paths)
        # sorted_fitness = sorted(key_fitness, key=operator.itemgetter(1), reverse=True)
        key_rank = []
        selective_pressure = 0.5
        # print(self.pop_with_fitness)
        # get the scaled rank value for each path: formula per Razali and Geraghty (2011)
        for fitness_index in range(0, len(self.pop_with_fitness)):
            key_rank.append((2 - selective_pressure) + (
            2.0 * (selective_pressure - 1) * (fitness_index - 1) / (len(self.pop_with_fitness) - 1)))
        # print(self.pop_with_fitness)
        # print(key_rank)
        return key_rank

    # calculate cumulative value of key rank
    def cal_cum_rank(self, key_rank):
        cum_key_rank = []
        cum_sum = 0.0
        for index in range(0, len(key_rank)):
            cum_sum += key_rank[index]
            cum_key_rank.append(cum_sum)
        # print(cum_key_rank)
        return cum_key_rank

    def rank_roulette_wheel_selection(self, elite_sz):
        #best paths from sorted population are preserved for the size of elite
        next_population = self.population[:elite_sz]

        #calculate each rank and total rank
        key_rank = self.cal_rank()
        total_rank = sum(rank_value for rank_value in key_rank)
        cum_key_rank = self.cal_cum_rank(key_rank)
        # print(cum_key_rank)

        #remaining population is filled with rank-based roulette wheel selection
        for num_selection in range(0, self.pop_size - elite_sz):
            roulette_random = random.uniform(0.0, 100.0)
            for pop_index in range(0, len(self.population)):
                percent = cum_key_rank[pop_index] / total_rank * 100
                if percent >= roulette_random:
                    if not self.is_duplicate(self.population[pop_index], next_population):
                        next_population.append(self.population[pop_index])
                else:
                    if not self.is_duplicate(self.population[0], next_population):
                        next_population.append(self.population[0])
        self.population = next_population
        self.cal_total_distance()

    def select_k_shortest_path(self, kth):
        self.sort_fit_score()
        print([x.get_key() for path in self.population for x in path])
        return self.pop_with_fitness[:kth]

def evolve_genes(genetic_algo, num_gen, selection, elite_sz, kshortest):
    genetic_algo.initialise_population()
    for evolution in range(num_gen):
        genetic_algo.crossover()
        genetic_algo.mutation(0.5)
        genetic_algo.cal_total_distance()
        genetic_algo.sort_fit_score()
        tournament = 3
        if selection=="tournament":
            genetic_algo.tournament_selection(tournament, elite_sz)
        if selection=="rank_roulette":
            genetic_algo.rank_roulette_wheel_selection(elite_sz)
    return genetic_algo.select_k_shortest_path(kshortest)

if __name__=="__main__":
    g = Graph()
    for i in range(6):
        g.add_vertex(string.ascii_uppercase[i + 2])

    g.add_edge('C', 'D', 3)
    g.add_edge('C', 'E', 2)
    g.add_edge('D', 'F', 4)
    g.add_edge('E', 'D', 1)
    g.add_edge('E', 'F', 2)
    g.add_edge('E', 'G', 3)
    g.add_edge('F', 'G', 2)
    g.add_edge('F', 'H', 1)
    g.add_edge('G', 'H', 2)

    #instantiate genetic algorithm
    genetic_algorithm = GeneticAlgorithm(g, 'C', 'H')
    #parameters for genetic algorithm
    num_evolution = 100
    elite_size = 2
    selection_method = "rank_roulette"
    k = 3
    #run k_shortest algorithm
    k_shortest = evolve_genes(genetic_algorithm, num_evolution, selection_method, elite_size, k)
    print(k_shortest)