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

    def add_neighbour(self, node, neighbour_weight=0.0):
        self.neighbours[node] = neighbour_weight

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

    def add_edge(self, prev_node, next_node, node_weight=0.0):
        if prev_node not in self.node_list:
            self.add_vertex(prev_node)
        if next_node not in self.node_list:
            self.add_vertex(next_node)
        self.node_list[prev_node].add_neighbour(self.node_list[next_node], node_weight)

    def __iter__(self):
        return iter(self.node_list.values())

class KShortest:
    def __init__(self, graph_passed, from_node, to_node, k_num):
        self.graph = graph_passed
        self.origin = from_node
        self.destination = to_node
        self.k_size = k_num
        self.pop_size = k*50
        self.d_path = list()
        self.d_list = list()
        self.population = list()
        self.target_distance = {}

    def dijkstra_initialisation(self, source, target, complete=False):
        #initialise the origin to 0
        distance = {source: 0}
        prev_node = {source: None}
        priority_queue = [(distance[source], source)]
        heapify(priority_queue)

        while priority_queue:
            (d, u) = heappop(priority_queue)
            if u==target:
                if complete:
                    self.target_distance = distance
                    d_best_path = list()
                    d_best_path.append(self.graph.get_vertex(target))
                    curr_node = target
                    while curr_node != source:
                        d_best_path.insert(0, self.graph.get_vertex(prev_node[curr_node]))
                        curr_node = prev_node[curr_node]
                    self.d_path = d_best_path
                    self.d_list = [x.get_key() for x in self.d_path]
                return distance[target]
            u = self.graph.get_vertex(u)
            for v in u.get_neighbours():
                if (v.get_key() not in distance) or (distance[v.get_key()] > (distance[u.get_key()] + u.get_weight(v))):
                    distance[v.get_key()] = distance[u.get_key()] + u.get_weight(v)
                    heappush(priority_queue, (distance[v.get_key()], v.get_key()))
                    prev_node[v.get_key()] = u.get_key()

    def random_dijkstra(self):
        #random mid vertex from the shortest path found by Dijkstra
        mid_vertex = random.choice(self.d_path)
        #get the key and index for the random mid vertex
        mid_key = mid_vertex.get_key()
        mid_index = self.d_path.index(mid_vertex)
        #extract the first section of the path so that loop can be checked later
        d_list = self.d_list[:mid_index]
        #get the shortest distance from origin to the mid vertex from the established collection of distances
        target1 = self.target_distance[mid_key]
        #get the neighbours of the mid vertex and select a random value of the neighbour
        neighbours = mid_vertex.get_neighbours()
        random_val = random.choice(list(neighbours.values()))
        #find a key for the random value of the neighbour
        inter_random_neighbour = {node: v for node, v in neighbours.items() if (node not in self.d_list) and v==random_val}
        #initiliase the second section of the path with infinity
        target2 = float('inf')
        #the new neighbour key must not be in the first section to have loopless shorest paths
        inter_random_neighbour_key = [x for x in inter_random_neighbour.keys()][0].get_key()
        if  inter_random_neighbour_key not in d_list:
            #find a reverse path distance between destination and the random neighbour selected
            target2 = self.dijkstra_initialisation(self.destination, inter_random_neighbour_key)
        #if target 1 and target2 exist i.e. the paths exist
        if target1 and target2:
            #the total target distance is
            target_distance = target1+target2+float([x for x in inter_random_neighbour.values()][0])
            return target_distance

    #create the collection of distances = 10*graph size
    def initialise_population(self):
        #first distance original Dijkstra
        self.population.append(round(self.dijkstra_initialisation(self.origin, self.destination, True),2))

        #rest distances filled with random Dijkstra
        for num_population in range(self.pop_size-1):
            path = self.random_dijkstra()
            if path and round(path,2) not in self.population:
                self.population.append(round(path,2))

    #select only k number of shortest paths from the collection of distances
    def select_k_shortest_path(self):
        return sorted(self.population)[:self.k_size]

#unitility function to identify the base processing time
def base_processing_time():
    base_time_measured = time.process_time()
    print("Basic processing Time taken (secs) = ", base_time_measured)
    return base_time_measured

if __name__=="__main__":
    #calculate base processing time and subtract it later
    base_time = base_processing_time()
    #instantiate graph class
    g = Graph()
    #input file name
    file_name = "finalInput.txt"
    #number of lines in the input file
    num_lines = sum(1 for line in open(file_name))
    #count lines to seperate the first and the very last line from the input contents
    count_line = 0
    #set origin and destination None and k = 1 i.e. the shortest path
    origin = None
    destination = None
    k = 1
    #go through each input contents line by line and read in
    with open(file_name) as f:
        for line in f:
            #first line of the input is for number of vertices and edges, but this information is not used in my algorithm
            if count_line==0:
                n_nodes, n_edges = line.split()
            #last line of the input specifies origin, destination and the number of shortest paths required
            elif count_line==num_lines-1:
                origin, destination, k = line.split()
                origin = origin
                destination = destination
                k = int(k)
            #all other lines provides from node, to node and the weight/path between these two nodes
            else:
                prev, nxt, weight = line.split()
                #build a graph with the nodes and weights
                g.add_edge(prev, nxt, float(weight))
            #add count_line to indicate the input is read in line by line
            count_line += 1

    #instantiate k_shortest algorithm with the graph built, origin, destination, and the number of shortest paths required
    k_shortest = KShortest(g, origin, destination, k)
    #initalise collections of the shortest distances
    k_shortest.initialise_population()
    #returns k number of shorest paths and print out
    distances = k_shortest.select_k_shortest_path()
    print("%d shortest distances include:" %k)
    print(*distances, sep=", ")
    #print out the actual time taken by subtracting the base processing time
    actual_time = time.process_time()
    print("K-Shortest Time taken (secs) = ", actual_time-base_time)