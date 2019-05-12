import math
import time
import os.path
import sys

class GameBall:
    '''Holding the value written on a ball, calculating the sum of digits and storing this value,
        and setting and storing the state of the ball as to whether it is taken or not'''
    def __init__(self, input_val):
        self.value = input_val
        self.digit_value = self.cal_digit_sum(self.value)
        self.state = 0

    #getter - get the value of a ball
    def get_value(self):
        return self.value

    #getter - get the sum of digits on a ball
    def get_digit(self):
        return self.digit_value

    #getter - get the state of a ball whether it is taken
    def get_state(self):
        return self.state

    #set the state of the ball to deleted (1) when it is extracted
    def set_state_deleted(self):
        if not self.state:
            self.state = 1

    #calculate the sum of all digits
    def cal_digit_sum(self, input_val):
        if input_val==0:
            return 0
        if input_val!=0:
            return input_val%10 + self.cal_digit_sum(input_val//10)

class PriorityQueue:
    '''Performs functions of a priority queue based on a heap and providing the max value based on
        a different priority criterion set for each player'''
    def __init__(self, ball_list):
        self.ball = GameBall(0)
        self.ball_heap = [self.ball]
        self.ball_list = ball_list
        self.size = 0
    #checks whether a queue is empty, first element in the queue is reserved not to be used
    def is_empty(self):
        return len(self.ball_heap)==1

    #return length of the current  queue
    def length(self):
        return len(self.ball_heap)

    #return the front value i.e. value of the max ball which is in the queue’s second index
    def front(self):
        return self.ball_heap[1].get_value()

    #return the ball object in the queue’s second index i.e. max ball
    def front_index(self):
        return self.ball_heap[1]

    #util function swap – swapping two balls x and y
    def swap(self, x, y):
        temp = self.ball_heap[y]
        self.ball_heap[y] = self.ball_heap[x]
        self.ball_heap[x] = temp

    #heapify  up makes the ball goes up to meet the max heap property
    #where a parent node must be larger than child nodes.
    def heapify_up(self, size, priority):
        while size//2 > 0:
            if priority=="HEADS": #Scott’s priority
                #parent node < child node then swap based on the value
                if self.ball_heap[size//2].get_value()<self.ball_heap[size].get_value():
                    self.swap(size//2, size)
            if priority=="TAILS": #Rusty’s priority
                #parent node < child node then swap based on the sum of digits
                if self.ball_heap[size//2].get_digit()<self.ball_heap[size].get_digit():
                    self.swap(size//2, size)
                #parent node = child node then look at the value and swap based on the value
                if self.ball_heap[size//2].get_digit()==self.ball_heap[size].get_digit():
                    if self.ball_heap[size//2].get_value()<self.ball_heap[size].get_value():
                        self.swap(size//2, size)
            #reduce index size to half to do the same process until the max heap property is met
            size = size//2

    def get_max_child(self, index, priority):
        #if the right child does not exist, return the left child index (heap fills left before right)
        if index * 2 + 1 > self.size:
            return index * 2
        else:
            if priority=="HEADS":
                #left node > right node then return left node
                if self.ball_heap[index * 2].get_value() > self.ball_heap[index * 2 + 1].get_value():
                    return index * 2
                else:
                    return index * 2 + 1
            if priority=="TAILS":
                #left node > right node then return left node
                if self.ball_heap[index * 2].get_digit() > self.ball_heap[index * 2 + 1].get_digit():
                    return index * 2
                #left node = right node then check the value of left and right rather than the sum of digit
                elif self.ball_heap[index * 2].get_digit() == self.ball_heap[index * 2 + 1].get_digit():
                    if self.ball_heap[index * 2].get_value() > self.ball_heap[index * 2 + 1].get_value():
                        return index * 2
                    else:
                        return index * 2 + 1
                #otherwise return right node
                else:
                    return index * 2 + 1

    #heapify down method makes a parent node that is smaller than child nodes
    #to be placed at the right position in the queue
    def heapify_down(self, c_index, priority):
        #while current index is smaller than the size of the queue
        while (c_index * 2) <= self.size:
            #get the child node with a larger value based on the priority
            max_child_index = self.get_max_child(c_index, priority)
            if priority=="HEADS":
                #if the value of the current index < the value of the max_child_index then swap
                if self.ball_heap[c_index].get_value() < self.ball_heap[max_child_index].get_value():
                    self.swap(c_index, max_child_index)
            if priority=="TAILS":
                #if the sum of digits of the current index < the sum_of digits of the max_child_index then swap
                if self.ball_heap[c_index].get_digit() < self.ball_heap[max_child_index].get_digit():
                    self.swap(c_index, max_child_index)
                #if the sum of digits of the current index = the value of the max_child_index
                if self.ball_heap[c_index].get_digit() == self.ball_heap[max_child_index].get_digit():
                    #then consider the value of the current index compared to the value of the max_child_index
                    if self.ball_heap[c_index].get_value() < self.ball_heap[max_child_index].get_value():
                        self.swap(c_index, max_child_index)
            #current index goes down to the max_child_index to meet max heap property
            c_index = max_child_index

    #insert the ball and build the heap, followed by heapify
    def insert(self, ball_picked, priority):
        self.ball_heap.append(ball_picked)
        self.size += 1
        self.heapify_up(self.size, priority)
    #extract and return max_addition and heapify down to ensure the heap property
    def delete(self, priority, turns):
        if self.is_empty():
            print("Priority queue is empty.")
            return -1
        #initialise the sum of the max balls for each player in this round
        max_addition = 0
        #track the number of turns taken by each player
        player_turn = 0
        while player_turn != turns:
            #find the max and change deleted state to 1
            if not self.front_index().get_state():
                max_deleted = self.front()
                self.ball_heap[1].set_state_deleted()
                #remove the element by assigning the least value and reduce the size of the heap
                self.ball_heap[1] = self.ball_heap[self.size]
                self.size -= 1
                #heapify down to ensure the heap property is still met
                self.heapify_down(1, priority)
                #add the extracted ball to the result of this round
                max_addition += max_deleted
                #the player used one turn
                player_turn += 1
            else:
                #remove the element by swapping and reduce the size of the heap
                self.ball_heap[1] = self.ball_heap[self.size]
                self.size -= 1
                #heapify down to ensure the heap property is met
                self.heapify_down(1, priority)
                #but do not add any value to the result or player’s turn as nothing happened
        return max_addition

    #util function – print the value, the sum of digits, and the state of each ball in the queue
    def print_queue(self):
        for i in range(1, self.size+1):
            print("value: ", self.ball_heap[i].get_value(),
                  " digit sum: ", self.ball_heap[i].get_digit(), " state: ", self.ball_heap[i].get_state())

class ScoreMaximiser:
    '''Responsible for building two different priority queues and dealing with turns for each player.
        This class also calculates the final score and returns the sum to a main function.'''
    def __init__(self, n_balls, ball_list):
        self.num_balls = n_balls
        self.ball_list = ball_list
        self.results = {"scott":0, "rusty":0}
        self.scott_pq = PriorityQueue(ball_list)
        self.rusty_pq = PriorityQueue(ball_list)
    #build two priority queues based on each player's priority
    def build_pq(self):
        for i in range(len(self.ball_list)):
            self.scott_pq.insert(self.ball_list[i], "HEADS")
            self.rusty_pq.insert(self.ball_list[i], "TAILS")
    #start to play rounds
    def play_round(self, turns, player_turn):
        #calculate how many rounds are available in the game
        rounds = math.ceil(self.num_balls/turns)
        #initialise which player would play first
        toggled = player_turn
        #track balls so that when all balls are taken, there is no more game
        track_balls = 0
        #if there are still balls not taken
        if track_balls!=self.num_balls:
            #for each round
            for game_round in range(rounds):
                if toggled=="HEADS": #Scott's turn
                    #get the sum of all max balls taken for this round
                    max_taken = self.scott_pq.delete(toggled, turns)
                    if max_taken is not None:
                        #add the sum of max balls taken to the previous result
                        self.cal_results(max_taken, "scott")
                if toggled=="TAILS": #Rusty's turn
                    # get the sum of all max balls taken for this round
                    max_taken = self.rusty_pq.delete(toggled, turns)
                    if max_taken is not None:
                        # add the sum of max balls taken to the previous result
                        self.cal_results(max_taken, "rusty")
                #change the turn
                toggled = self.toggle(toggled)
                #track the number of balls taken
                track_balls += turns
        return self.return_results()

    #change the turn
    def toggle(self, turn):
        toggled = turn
        if turn == "HEADS":
            toggled = "TAILS"
        if turn == "TAILS":
            toggled = "HEADS"
        return toggled

    #add extracted value to the existing sum for each player
    def cal_results(self, max_taken, key):
        self.results[key] += max_taken

    #return player name and total score to print out
    def return_results(self):
        return self.results


class FileLoader:
    def __init__(self, infile):
        self.filename = infile
        self.output = "out.txt"

    #load file content to list without new line character
    def load_file(self):
        self.content = [line.rstrip('\n') for line in open(self.filename)]

    #get all the information on input and place it to a dictionary
    def format_content(self):
        #first line has the total number of games
        num_game = int(self.content[0])
        num_games = num_game*3
        track_set = 0
        games = []
        game_setting = {"n_balls": 0, "n_turns": 0, "ball_list": [], "turn": ""}
        for index in range(1, num_games+1):
            #every second line has number of balls and maximum number of turns
            if index%3==1:
                game_setting["n_balls"], game_setting["n_turns"] = map(int, self.content[index].split())
                track_set += 1
            #every third line has list of balls
            if index%3==2:
                game_setting["ball_list"] = list(map(int, self.content[index].split()))
                track_set += 1
            #every four line has which player start first
            if index%3==0:
                game_setting["turn"] = self.content[index]
                track_set += 1
            if track_set==3:
                games.append(game_setting)
                game_setting = {"n_balls": 0, "n_turns": 0, "ball_list": [], "turn": ""}
                track_set = 0
        return num_game, games

if __name__=="__main__":
    file_name = input("Please provide the input file name.")
    c_path = os.path.join(os.getcwd(), file_name)
    #if file name does not exist, error
    if not os.path.exists(c_path):
        print("File does not exist. Please check your file name and try again.")
        sys.exit()

    #load the data into the dictionary form to start games
    input_file = FileLoader(c_path)
    input_file.load_file()
    n_game = 0
    no_game, games = input_file.format_content()

    #start game by iterating each game
    for each_game in range(no_game):
        #number of balls
        n_ball = games[each_game]['n_balls']
        #maximum number of turns allowed
        n_turns = games[each_game]['n_turns']
        #which player starts the game first
        turn = games[each_game]['turn']
        #initialise list of balls
        balls = []
        #store/calculate the value of a ball and initialise the state of taken in list of balls
        for each_ball in range(games[each_game]['n_balls']):
            ball = GameBall(games[each_game]['ball_list'][each_ball])
            balls.append(ball)
        #instantiate game to start
        game = ScoreMaximiser(n_ball, balls)
        #build two queues - one for Scott, one for Rusty
        game.build_pq()
        #play a game
        result = game.play_round(n_turns, turn)
        print(result["scott"], result["rusty"])
        print("Time taken (secs) = ", time.process_time())
        #generate output file in a folder
        with open("output.txt", 'a') as output_file:
            results = str(result["scott"]) + ' ' + str(result["rusty"]) + '\n'
            output_file.write(results)