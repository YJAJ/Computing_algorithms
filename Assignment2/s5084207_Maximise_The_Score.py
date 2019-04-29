class Heap:
    def __init__(self):
        self.heap = []

    def build_max_heap(self):
        return

    def build_digit_heap(self):
        return

class Priority_queue:
    def __init__(self, n_balls):
        self.length = n_balls
        return

class Score_maximiser:
    def __init__(self, n_balls):
        self.scott_pq = Priority_queue(n_balls)
        self.rusty_pq = Priority_queue(n_balls)
        self.num_balls = n_balls
        self.results = {}
        assert n_balls == self.scott_pq.length

    def play_round(self, turns):
        return

    def play_game(self):
        return

    def cal_results(self):
        return self.results


if __name__=="__main__":
    game_score = Score_maximiser(3)
    print(game_score)