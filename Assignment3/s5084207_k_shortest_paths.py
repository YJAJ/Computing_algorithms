import time
import random
from heapq import heapify, heappop, heappush

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

    def add_neighbour(self, node, weight=0.0):
        self.neighbours[node] = weight

    def __str__(self):
        return str(self.key) + " is directed to " + str([x.key for x in self.neighbours])

class Graph:
    def __init__(self):
        self.node_list = {}
        self.n_size = 0

    def get_vertex(self, node):
        if node in self.node_list:
            return self.node_list[node]
        else:
            return None

    def get_vertices(self):
        return self.node_list

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

    def __iter__(self):
        return iter(self.node_list.values())

class K_Shortest:
    def __init__(self, graph_passed, origin, destination, k):
        self.graph = graph_passed
        self.origin = origin
        self.destination = destination
        self.population = []
        self.k_size = k
        self.pop_size = k*200
        self.pop_with_fitness = []
        self.selected_nodes = []

    def dijkstra_initialisation(self, source, target, complete=False):
        #initialise the origin to 0
        distance = {source: 0}
        prev_node = {source: None}
        priority_queue = [(distance[source], source)]
        heapify(priority_queue)

        while priority_queue:
            (d, u) = heappop(priority_queue)
            if u==target:
                self.target_distance = distance
                if complete:
                    d_best_path = list()
                    d_best_path.append(self.graph.get_vertex(target))
                    curr_node = target
                    while curr_node != source:
                        d_best_path.insert(0, self.graph.get_vertex(prev_node[curr_node]))
                        curr_node = prev_node[curr_node]
                    self.d_path = d_best_path
                # print([x.get_key() for x in self.d_path])
                return distance[target]
            u = self.graph.get_vertex(u)
            for v in u.get_neighbours():
                if (v.get_key() not in distance) or (distance[v.get_key()] > (distance[u.get_key()] + u.get_weight(v))):
                    distance[v.get_key()] = distance[u.get_key()] + u.get_weight(v)
                    heappush(priority_queue, (distance[v.get_key()], v.get_key()))
                    prev_node[v.get_key()] = u.get_key()


    def random_dijkstra(self):
        # print(len(self.d_path))
        mid = random.choice(self.d_path)#random.choice(self.selected_nodes) #random.choice(list(self.graph.get_vertices()))
        self.d_list = [x.get_key() for x in self.d_path]
        mid_key = mid.get_key()
        # print(mid_key)
        if mid_key in self.target_distance:
            target1 = self.target_distance[mid_key]
        else:
            target1 = self.dijkstra_initialisation(self.origin, mid_key)
        neighbours = mid.get_neighbours()
        random_val = random.choice(list(neighbours.values()))
        inter = {k: v for k, v in neighbours.items() if (k not in self.d_list) and v==random_val}
        # print(float([x for x in inter.values()][0]))
        # print(target1)
        # target1 = self.dijkstra_initialisation(self.origin, mid)
        # print(inter.keys())
        target2 = self.dijkstra_initialisation(self.destination, [x for x in inter.keys()][0].get_key())
        if target1 and target2:
            target_distance = target1+target2+float([x for x in inter.values()][0])
            # print(target_distance)
            return target_distance

    #create the number of poplution = 5*graph size
    def initialise_population(self):
        #first distance original Dijkstra
        self.population.append(round(self.dijkstra_initialisation(self.origin, self.destination, True),2))

        #rest distances filled with random Dijkstra
        for num_population in range(self.pop_size-1):
            path = self.random_dijkstra()
            if path and round(path,2) not in self.population:
                self.population.append(round(path,2))

    def select_k_shortest_path(self):
        return sorted(self.population)[:self.k_size]

def hello_world():
    basic_time = time.process_time()
    print("Hello World Time taken (secs) = ", basic_time)
    return basic_time

if __name__=="__main__":

    hello_world_time = hello_world()

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
            elif count_line==num_lines-1:
                origin, destination, k = line.split()
                origin = int(origin)
                destination = int(destination)
                k = int(k)
            else:
                prev, nxt, weight = line.split()
                g.add_edge(int(prev), int(nxt), float(weight))
            count_line += 1

    k = 10
    #instantiate genetic algorithm
    k_shortest = K_Shortest(g, origin, destination, k)

    k_shortest.initialise_population()
    distances = k_shortest.select_k_shortest_path()
    print(distances)

    actual_time = time.process_time()
    print("Whole Time taken (secs) = ", actual_time-hello_world_time)