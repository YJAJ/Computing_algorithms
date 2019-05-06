import math
import time
import os

class Game_Ball:
    def __init__(self, input):
        self.value = input
        self.digit_value = self.cal_digit_sum(self.value)
        self.state = 0
    #getters
    def get_value(self):
        return self.value
    def get_digit(self):
        return self.digit_value
    def get_state(self):
        return self.state
    #setter
    def set_state_deleted(self):
        if not self.state:
            self.state = 1
    #calculate the sum of all digits
    def cal_digit_sum(self, input):
        if input==0:
            return 0
        if input!=0:
            return input%10 + self.cal_digit_sum(input//10)

class Binary_Heap:
    def __init__(self, ball_list):
        self.ball = Game_Ball(0)
        self.ball_heap = [self.ball]
        self.ball_list = ball_list
        self.size = 0

    def is_empty(self):
        return len(self.ball_heap)==1

    def length(self):
        return len(self.ball_heap)-1

    def maximum(self, priority):
        return self.ball_heap[1].get_value()

    def maximum_index(self, priority):
        return self.ball_heap[1]

    def swap(self, x, y):
        temp = self.ball_heap[y]
        self.ball_heap[y] = self.ball_heap[x]
        self.ball_heap[x] = temp

    def heapify_up(self, size, priority):
        while size//2 > 0:
            #parent node < child node then swap
            if priority=="HEADS":
                if self.ball_heap[size//2].get_value()<self.ball_heap[size].get_value():
                    self.swap(size//2, size)
            if priority=="TAILS":
                if self.ball_heap[size//2].get_digit()<self.ball_heap[size].get_digit():
                    self.swap(size//2, size)
                if self.ball_heap[size//2].get_digit()==self.ball_heap[size].get_digit():
                    if self.ball_heap[size//2].get_value()<self.ball_heap[size].get_value():
                        self.swap(size//2, size)
            size = size//2

    def get_max_child(self, index, priority):
        #if the right child does not exist, return the left child index
        if index * 2 + 1 > self.size:
            return index * 2
        else:
            if priority=="HEADS":
                if self.ball_heap[index * 2].get_value() > self.ball_heap[index * 2 + 1].get_value():
                    return index * 2
                else:
                    return index * 2 + 1
            if priority=="TAILS":
                if self.ball_heap[index * 2].get_digit() > self.ball_heap[index * 2 + 1].get_digit():
                    return index * 2
                elif self.ball_heap[index * 2].get_digit() == self.ball_heap[index * 2 + 1].get_digit():
                    if self.ball_heap[index * 2].get_value() > self.ball_heap[index * 2 + 1].get_value():
                        return index * 2
                    else:
                        return index * 2 + 1
                else:
                    return index * 2 + 1

    def heapify_down(self, c_index, priority):
        while (c_index * 2) <= self.size:
            max_child_index = self.get_max_child(c_index, priority)
            if priority=="HEADS":
                if self.ball_heap[c_index].get_value() < self.ball_heap[max_child_index].get_value():
                    self.swap(c_index, max_child_index)
            if priority=="TAILS":
                if self.ball_heap[c_index].get_digit() < self.ball_heap[max_child_index].get_digit():
                    self.swap(c_index, max_child_index)
                if self.ball_heap[c_index].get_digit() == self.ball_heap[max_child_index].get_digit():
                    if self.ball_heap[c_index].get_value() < self.ball_heap[max_child_index].get_value():
                        self.swap(c_index, max_child_index)
            c_index = max_child_index
    #insert the ball and build the heap, followed by heapify
    def insert(self, ball, priority):
        self.ball_heap.append(ball)
        self.size += 1
        self.heapify_up(self.size, priority)

    def extract_max(self, priority, turns):
        if self.is_empty():
            print("Priority queue is empty.")
            return -1
        max_addition = 0
        turn = 0
        while turn != turns:
            #find the max and change deleted state to 1
            if not self.maximum_index(priority).get_state():
                max_deleted = self.maximum(priority)
                self.ball_heap[1].set_state_deleted()
                #remove the element by assigning the least value and reduce the size of the heap
                self.ball_heap[1] = self.ball_heap[self.size]
                self.size -= 1
                self.heapify_down(1, priority)
                max_addition += max_deleted
                turn += 1
            else:
                #remove the element by assigning the least value and reduce the size of the heap
                self.ball_heap[1] = self.ball_heap[self.size]
                self.size -= 1
                self.heapify_down(1, priority)
        return max_addition
    #print out the heap with the data in each ball
    def print_heap(self):
        for i in range(1, self.size+1):
            print("value: ", self.ball_heap[i].get_value(),
                  " digit sum: ", self.ball_heap[i].get_digit(), " state: ", self.ball_heap[i].get_state())

class Score_Maximiser:
    def __init__(self, n_balls, ball_list):
        self.num_balls = n_balls
        self.ball_list = ball_list
        self.results = {"scott":0, "rusty":0}
        self.scott_pq = Binary_Heap(ball_list)
        self.rusty_pq = Binary_Heap(ball_list)
        # assert n_balls == self.scott_pq.size()
        # assert n_balls == self.rusty_pq.size()

    def build_pq(self):
        for i in range(len(self.ball_list)):
            self.scott_pq.insert(self.ball_list[i], "HEADS")
            self.rusty_pq.insert(self.ball_list[i], "TAILS")
        # print(self.scott_pq.print_heap())
        # print(self.rusty_pq.print_heap())

    def play_round(self, turns, turn):
        rounds = math.ceil(self.num_balls/turns)
        toggle = turn
        track_balls = 0
        if track_balls!=self.num_balls:
            for game_round in range(rounds):
                if toggle=="HEADS":
                    max = self.scott_pq.extract_max(toggle, turns)
                    # print(max)
                    if max!=None:
                        self.cal_results(max, "scott")
                if toggle=="TAILS":
                    max = self.rusty_pq.extract_max(toggle, turns)
                    # print(max)
                    if max!=None:
                        self.cal_results(max, "rusty")
                # print(toggle)
                toggle = self.toggle(toggle)
                track_balls += turns
        return self.return_results()

    def toggle(self, turn):
        if turn == "HEADS":
            toggle = "TAILS"
        if turn == "TAILS":
            toggle = "HEADS"
        return toggle

    def cal_results(self, max, key):
        self.results[key] += max

    def return_results(self):
        return self.results

class File_Loader():
    def __init__(self, infile):
        self.filename = infile
        self.output = "out.txt"

    def load_file(self):
        self.content = [line.rstrip('\n') for line in open(self.filename)]

    def format_content(self, n_game):
        no_game = int(self.content[0])
        no_games = no_game*3
        track_set = 0
        games = []
        game_setting = {"n_balls": 0, "n_turns": 0, "ball_list": [], "turn": ""}
        for index in range(1, no_games+1):
            if index%3==1:
                game_setting["n_balls"], game_setting["n_turns"] = map(int, self.content[index].split())
                track_set += 1
            if index%3==2:
                game_setting["ball_list"] = list(map(int, self.content[index].split()))
                track_set += 1
            if index%3==0:
                game_setting["turn"] = self.content[index]
                track_set += 1
            if track_set==3:
                games.append(game_setting)
                game_setting = {"n_balls": 0, "n_turns": 0, "ball_list": [], "turn": ""}
                track_set = 0
        return no_game, games

    def write_file(self):
        return

if __name__=="__main__":
    c_path = os.path.join(os.getcwd(), "inputLeScore.txt")
    input_file = File_Loader(c_path)
    input_file.load_file()
    n_game = 0
    no_game, games = input_file.format_content(n_game)
    for each_game in range(no_game):
        n_ball = games[each_game]['n_balls']
        n_turns = games[each_game]['n_turns']
        turn = games[each_game]['turn']
        balls = []
        for each_ball in range(games[each_game]['n_balls']):
            ball = Game_Ball(games[each_game]['ball_list'][each_ball])
            balls.append(ball)
        game = Score_Maximiser(n_ball, balls)
        game.build_pq()
        results = game.play_round(n_turns, turn)
        print(results)
        print("Time taken (secs) = ", time.process_time())