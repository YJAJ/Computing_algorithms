from collections import defaultdict
import operator
# from more_itertools import unique_everseen
import string
import itertools
import time
import heapq
import random
import copy
import multiprocessing as mp
import queue
# import resource
import sys

class Node:
    def __init__(self, value):
        self.key = value
        self.neighbours = {}

    def get_neighbours(self):
        return self.neighbours

    def get_key(self):
        return self.key

    def get_weight(self, node):
        return self.neighbours[node]

    def add_neighbour(self, node, weight=0):
        self.neighbours[node] = weight

    def __str__(self):
        return str(self.key) + " is directed to " + str([x.key for x in self.neighbours])

class Graph:
    def __init__(self):
        self.node_list = {}
        self.n_size = 0

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

    def remove_vertex(self, node):
        if node in self.node_list:
            del self.node_list[node.get_key()]

    def sample_graph(self, size):
        new_graph = {k: 0 for k in random.sample(list(self.node_list), size)}
        return new_graph

    def __iter__(self):
        return iter(self.node_list.values())

class PriorityQueue:

    def __init__(self, source_node, priority):
        self.pq = [source_node, source_node]
        self.priority = priority
        self.size = 0

    #checks whether a queue is empty, first element in the queue is reserved not to be used
    def is_empty(self):
        return len(self.pq) == 1

    #return length of the current queue
    def length(self):
        return len(self.pq)

    def get_pq(self):
        return self.pq

    #return the front value i.e. min which is in the queue’s second index
    def front(self):
        return self.priority[1]

    #return the ball object in the queue’s second index
    def front_node(self):
        return self.pq[1]

    def second_node(self):
        return self.pq[self.get_min_child(1)]

    # util function swap – swapping two nodes x and y
    def swap(self, x, y):
        temp = self.pq[y]
        self.pq[y] = self.pq[x]
        self.pq[x] = temp

    # heapify  up makes the ball goes up to meet the min heap property
    # where a parent node must be smaller than child nodes.
    def heapify_up(self, size):
        while size // 2 > 0:
            # parent node > child node then swap based on the value
            if self.priority[size // 2] < self.priority[size]:
                self.swap(size // 2, size)
            # reduce index size to half to do the same process until the max heap property is met
            size = size // 2

    def get_min_child(self, index):
        # if the right child does not exist, return the left child index (heap fills left before right)
        if index * 2 + 1 > self.size:
            return index * 2
        else:
            # left node < right node then return left node
            if self.priority[index * 2] < self.priority[index * 2 + 1]:
                return index * 2
            else:
                return index * 2 + 1

    # heapify down method makes a parent node that is smaller than child nodes
    # to be placed at the right position in the queue
    def heapify_down(self, c_index):
        # while current index is smaller than the size of the queue
        while (c_index * 2) <= len(self.pq)-1:
            # get the child node with a larger value based on the priority
            min_child_index = self.get_min_child(c_index)
            # if the value of the current index < the value of the max_child_index then swap
            if self.priority[c_index] < self.priority[min_child_index]:
                self.swap(c_index, min_child_index)
            # current index goes down to the max_child_index to meet max heap property
            c_index = min_child_index

    # insert the ball and build the heap, followed by heapify
    def insert(self, node):
        self.pq.append(node)
        # self.size += 1
        self.heapify_up(len(self.pq)-1)

    # extract and return max_addition and heapify down to ensure the heap property
    def delete(self):
        if self.is_empty():
            print("Priority queue is empty.")
            return -1
        min_deleted = self.front_node()
        # remove the element by assigning the least value and reduce the size of the heap
        if len(self.pq)>2:
            # print(len(self.pq))
            self.pq[1] = self.pq[len(self.pq)-1]
        self.pq.pop()
        # self.size -= 1
        # heapify down to ensure the heap property is still met
        self.heapify_down(1)
        return min_deleted

    def delete_second(self):
        if self.is_empty():
            print("Priority queue is empty.")
            return -1
        self.delete()
        min_deleted = self.front_node()
        # remove the element by assigning the least value and reduce the size of the heap
        if len(self.pq)>2:
            # print(len(self.pq))
            self.pq[1] = self.pq[len(self.pq)-1]
        self.pq.pop()
        # self.size -= 1
        # heapify down to ensure the heap property is still met
        self.heapify_down(1)
        return min_deleted


#Wang et al., 2018 and Razali and Geraghty, 2011
class GeneticAlgorithm:
    def __init__(self, graph_passed, origin, destination, k):
        self.graph = graph_passed
        self.g_size = self.graph.get_size()
        self.origin = origin
        self.destination = destination
        self.population = []
        self.k_size = k
        self.pop_size = k*2
        self.pop_with_fitness = []
        self.target_distance = set()

    # def random_initialisation(self, graph):
    #     while True:
    #         # print(graph.get_vertex(self.origin))
    #         curr_node = graph.get_vertex(self.origin)
    #         #add origin into path
    #         one_path = list()
    #         one_path.append(curr_node)
    #         #randomly select a neighbour
    #         neighbours = list(curr_node.get_neighbours())
    #         # save_neighbours = list(curr_node.get_neighbours())
    #         while neighbours is not None or len(neighbours)!=0:
    #             if len(neighbours)==0:
    #                 # rd_selected_neighbour = random.choice(save_neighbours)
    #                 break
    #             else:
    #                 rd_selected_neighbour = random.choice(neighbours)
    #             if rd_selected_neighbour in one_path:
    #                 neighbours.remove(rd_selected_neighbour)
    #             print(len(one_path))
    #             if rd_selected_neighbour not in one_path:
    #                 curr_node = rd_selected_neighbour
    #                 neighbours = list(curr_node.get_neighbours())
    #                 # save_neighbours = neighbours.copy()
    #                 one_path.append(curr_node)
    #                 if curr_node.get_key()==self.destination:
    #                     return one_path

    def random_path(self, existing_path, index):
        while True:
            neighbours = list(existing_path[index].get_neighbours())
            while neighbours is not None or len(neighbours)!=0:
                rd_selected_neighbour = random.choice(neighbours)
                path_keys = [x.get_key() for x in existing_path]
                if rd_selected_neighbour in path_keys:
                    while rd_selected_neighbour.get_key() in path_keys:
                        neighbours.remove(rd_selected_neighbour)
                # print("select again")
                rd_selected_neighbour = random.choice(neighbours)
                if rd_selected_neighbour not in path_keys:
                    curr_node = rd_selected_neighbour
                    neighbours = list(curr_node.get_neighbours())
                    existing_path.append(curr_node)
                    if curr_node.get_key()==self.destination:
                        return existing_path

            # while curr_node.get_key()!=self.destination:
            #     neighbours = curr_node.get_neighbours()
            #     min_neighbour = min(neighbours, key=neighbours.get)
            #     if min_neighbour.get_key() not in one_path:
            #         curr_node = min_neighbour
            #         one_path.append(curr_node)
            #     else:
            #         if len(neighbours)!=0:
            #             neighbours.pop(min_neighbour, None)
            #         else:
            #             break

    def random_initialisation(self):
        # print(len(self.bf_path))
        bf_path = self.d_path.copy()
        # print(bf_path[-2].get_neighbours().keys())
        for i in range(self.k_size-2, self.k_size-2-k, -1):
            neighbours = list(bf_path[i].get_neighbours().keys())
            the_other_node = random.choice(neighbours)

            del bf_path[-1]
            while True:
                the_other_node = random.choice(neighbours)
                print(the_other_node.get_key())
                if the_other_node.get_key() not in self.d_list:
                    del bf_path[-1]
                    bf_path.append(the_other_node)
                    final_path = self.random_path(bf_path, i)
                    if final_path!=-1:
                        return final_path
                    else:
                        break
                else:
                    neighbours.remove(the_other_node)

    def change_path(self):

        return
    #one of initialisation method - Bellman Ford
    # def bellman_ford_initialisation(self):
    #     #initialise graph nodes to infinity except for the origin that has 0
    #     distance = {index: float("inf") for index in range(self.g_size)}
    #     distance[self.origin] = 0
    #     prev_node = {node_key_index: None for node_key_index in range(self.g_size)}
    #
    #     #try all edges v-1 times
    #     for graph_vertex in range(self.graph.get_size()-1):
    #         for u in self.graph:
    #             for v in u.get_neighbours():
    #                 # print(u.get_key(), v.get_key(), u.get_weight(v))
    #                 if (distance[u.get_key()] != float("inf")) and (distance[u.get_key()] + u.get_weight(v) < distance[v.get_key()]):
    #                     distance[v.get_key()] = distance[u.get_key()] + u.get_weight(v)
    #                     prev_node[v.get_key()] = u.get_key()
    #                     self.target_distance.add(distance[self.destination])
    #     bf_best_path = list()
    #     bf_best_path.append(self.graph.get_vertex(self.destination))
    #     curr_node = self.destination
    #     while curr_node!=self.origin:
    #         bf_best_path.insert(0,self.graph.get_vertex(prev_node[curr_node]))
    #         curr_node = prev_node[curr_node]
    #     self.d_path = bf_best_path
    #     print("BF population Time taken (secs) = ", time.process_time())

    def dijkstra_initialisation(self):
        #initialise graph nodes to infinity except for the origin that has 0
        distance = {index: float("inf") for index in range(self.g_size)}
        distance[self.origin] = 0
        prev_node = {node_key_index: None for node_key_index in range(self.g_size)}
        list_node = {node_key_index: None for node_key_index in range(self.g_size)}
        previous_distance = 0

        priority_queue = PriorityQueue(self.graph.get_vertex(self.origin), distance)
        # print(len(priority_queue.get_pq()))
        # print(priority_queue.get_pq()[0].get_key())
        # print(priority_queue.length())
        count = 0
        while priority_queue.length()!=1:
            u = priority_queue.delete()
            if count%1000==0 and priority_queue.length()!=1:
                u = priority_queue.delete()
            for v in u.get_neighbours():
                # print(u.get_key(), v.get_key(), u.get_weight(v))
                if (distance[v.get_key()] > (distance[u.get_key()] + u.get_weight(v))):
                    distance[v.get_key()] = distance[u.get_key()] + u.get_weight(v)
                    prev_node[v.get_key()] = u.get_key()
                    priority_queue.insert(v)
                    self.target_distance.add(distance[self.destination])
                    if distance[self.destination]!=previous_distance:
                        list_node = prev_node.copy()
                    previous_distance = distance[self.destination]
            count += 1
        # print(target_distance)
        print("d population Time taken (secs) = ", time.process_time())
        d_best_path = list()
        d_best_path.append(self.graph.get_vertex(self.destination))
        curr_node = self.destination
        while curr_node!=self.origin:
            d_best_path.insert(0,self.graph.get_vertex(prev_node[curr_node]))
            curr_node = prev_node[curr_node]
        self.d_path = d_best_path
        self.d_list = [x.get_key() for x in self.d_path]
        self.change_path()

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
        self.dijkstra_initialisation()
        self.population.append(self.d_path)
        #rest parents filled with random initialisation
        # for num_population in range(self.pop_size-1):
        #     print(num_population)
        # path = self.random_initialisation()
        # if not self.is_duplicate(path, self.population):
        #     self.population.append(path)
        print("Initialise population Time taken (secs) = ", time.process_time())

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
        print("construct genepool Time taken (secs) = ", time.process_time())
        return graph

    def crossover(self):
        for crossover_times in range(len(self.population)):
            gene_pool_graph = self.construct_genepool("crossover")
            # print([x.get_key() for x in gene_pool_graph])
            child = self.random_initialisation(gene_pool_graph)
            # print([x.get_key() for x in child])
            if not self.is_duplicate(child, self.population):
                self.population.append(child)
        print("crossover Time taken (secs) = ", time.process_time())

    def mutation(self, mutant_percent):
        for mutation_times in range(int(mutant_percent*len(self.population))):
            gene_pool_graph = self.construct_genepool("mutation")
            mutant = self.random_initialisation(gene_pool_graph)
            if not self.is_duplicate(mutant, self.population):
                self.population.append(mutant)
        print("mutation Time taken (secs) = ", time.process_time())

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
        print("calculate distance Time taken (secs) = ", time.process_time())

    #sort based on fitness score i.e. addition of weights
    def sort_fit_score(self):
        self.pop_with_fitness, self.population = zip(*[(fitness, path) for fitness, path in sorted(zip(self.pop_with_fitness,  self.population), key=lambda x: x[0])])
        self.pop_with_fitness = list(self.pop_with_fitness)
        self.population = list(self.population)
        print("sort fit score Time taken (secs) = ", time.process_time())

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
        print("rank selection Time taken (secs) = ", time.process_time())

    def select_k_shortest_path(self, kth):
        # self.sort_fit_score()
        # print([x.get_key() for path in self.population for x in path])
        # return self.pop_with_fitness[:kth]
        return sorted(self.target_distance)[:kth]

def evolve_genes(genetic_algo, num_gen, selection, elite_sz, kshortest):
    genetic_algo.initialise_population()
    # for evolution in range(num_gen):
    #     genetic_algo.crossover()
    #     genetic_algo.mutation(0.5)
    # genetic_algo.cal_total_distance()
    #     genetic_algo.sort_fit_score()
    #     tournament = 3
    #     if selection=="tournament":
    #         genetic_algo.tournament_selection(tournament, elite_sz)
    #     if selection=="rank_roulette":
    #         genetic_algo.rank_roulette_wheel_selection(elite_sz)
    # ks = genetic_algo.select_k_shortest_path(kshortest)
    # output.put(ks)
    return genetic_algo.select_k_shortest_path(kshortest)

if __name__=="__main__":

    # max_rec = 0x100000
    #
    # sys.setrecursionlimit(max_rec)
    # output = mp.Queue()
    g = Graph()
    g1 = Graph()
    file_name = "finalInput.txt"
    num_lines = sum(1 for line in open(file_name))
    count_line = 0
    origin = None
    destination = None

    with open(file_name) as f:
        for line in f:
            if count_line==0:
                n_nodes, n_edges = line.split()
                for node in range(int(n_nodes)):
                    g.add_vertex(node)
                    g1.add_vertex(node)
            elif count_line==num_lines-1:
                origin, destination, k = line.split()
                origin = int(origin)
                destination = int(destination)
                k = int(k)
            else:
                prev, nxt, weight = line.split()

                g.add_edge(int(prev), int(nxt), float(weight))
                if count_line%2:
                    # print(prev, nxt, weight)
                    g1.add_edge(int(prev), int(nxt), float(weight))
            count_line += 1
        print("input Time taken (secs) = ", time.process_time())
    # print(g1.get_size())
    # for i in range(6):
    #     g.add_vertex(string.ascii_uppercase[i + 2])
    #
    # g.add_edge('C', 'D', 3)
    # g.add_edge('C', 'E', 2)
    # g.add_edge('D', 'F', 4)
    # g.add_edge('E', 'D', 1)
    # g.add_edge('E', 'F', 2)
    # g.add_edge('E', 'G', 3)
    # g.add_edge('F', 'G', 2)
    # g.add_edge('F', 'H', 1)
    # g.add_edge('G', 'H', 2)
    k = 5
    #instantiate genetic algorithm
    genetic_algorithm = GeneticAlgorithm(g, origin, destination, k)

    #parameters for genetic algorithm
    num_evolution = 1
    elite_size = 2
    selection_method = "rank_roulette"

    # processes = [mp.Process(target=evolve_genes, args=(genetic_algorithm, num_evolution, selection_method, elite_size, k)) for p in range(3)]
    # for p in processes:
    #     p.start()
    # for p in processes:
    #     p.join()
    # results = [output.get() for p in processes]
    # print(results)
    #run k_shortest algorithm
    k_shortest = evolve_genes(genetic_algorithm, num_evolution, selection_method, elite_size, k)
    print(k_shortest)