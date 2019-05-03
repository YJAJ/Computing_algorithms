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
    def __init__(self):
        self.ball = Game_Ball(0)
        self.ball_heap = [self.ball]
        self.size = 0

    def is_empty(self):
        return len(self.ball_heap)==1

    def size(self):
        return len(self.ball_heap)-1

    def find_max(self):
        return self.ball_heap[1].get_value()

    def swap(self, x, y):
        temp = self.ball_heap[y]
        self.ball_heap[y] = self.ball_heap[x]
        self.ball_heap[x] = temp

    def heapify_up(self, size):
        while size//2 > 0:
            #parent node < child node then swap
            if self.ball_heap[size//2].get_value()<self.ball_heap[size].get_value():
                self.swap(size//2, size)
            size = size//2

    def get_max_child(self, index):
        if index * 2 + 1 > self.size:
            return index * 2
        else:
            if self.ball_heap[index * 2].get_value() > self.ball_heap[index * 2 + 1].get_value():
                return index * 2
            else:
                return index * 2 + 1

    def heapify_down(self, c_index):
        while (c_index * 2) <= self.size:
            max_child_index = self.get_max_child(c_index)
            if self.ball_heap[c_index].get_value() < self.ball_heap[max_child_index].get_value():
                self.swap(c_index, max_child_index)
            c_index = max_child_index

    def insert(self, ball):
        self.ball_heap.append(ball)
        self.size += 1
        self.heapify_up(self.size)

    def delete_max(self):
        #find the max and change deleted state to 1
        max_deleted = self.find_max()
        self.ball_heap[1].set_state_deleted()
        #move the last element to the top
        self.swap(1, self.size)
        #self.ball_heap[1] = self.ball_heap[self.size]
        self.size -= 1
        self.heapify_down(1)
        return max_deleted

    def print_heap(self):
        for i in range(1, len(self.ball_heap)):
            print("value: ", self.ball_heap[i].get_value(),
                  " digit sum: ", self.ball_heap[i].get_digit(), " state: ", self.ball_heap[i].get_state())

# class Priority_queue:
#     def __init__(self, n_balls):
#         self.length = n_balls
#         return

# class Score_maximiser:
#     def __init__(self, n_balls):
#         self.scott_pq = Priority_queue(n_balls)
#         self.rusty_pq = Priority_queue(n_balls)
#         self.num_balls = n_balls
#         self.results = {}
#         assert n_balls == self.scott_pq.length
#
#     def play_round(self, turns):
#         return
#
#     def play_game(self):
#         return
#
#     def cal_results(self):
#         return self.results

if __name__=="__main__":
    balls = [1000, 99, 98]
    heap = Binary_Heap()
    for i in range(len(balls)):
        ball = Game_Ball(balls[i])
        #print(ball.get_value(), ball.get_digit(), ball.get_state())
        heap.insert(ball)

    heap.print_heap()
    heap.delete_max()
    heap.print_heap()
    # game_score = Score_maximiser(3)
    # balls = [1000, 99, 98]
    # print(game_score)