import time
import math
import os
import collections

class Combinations():
    def __init__(self):
        self.value = 0
        self.coin_denominations = []
        self.coin_den_sz = 0
        self.num_coins = 0
        self.min_coins = 1
        self.max_coins = 0
        self.collection = collections.OrderedDict()
        self.temp_collection = []

    def find_prime(self, amount):
        self.coin_denominations.append(1)
        for num in range(2,amount):
            if self.is_prime(num):
                self.coin_denominations.append(num)
        self.coin_den_sz = len(self.coin_denominations)
        return self.coin_denominations

    def is_prime(self, num):
        if num==2:
            return True
        if num%2==0:
            return False
        root = math.floor(math.sqrt(num))
        for n in range(3, root+1, 2):
            if num%n==0:
                return False
        return True

    def find_largest_prime(self, value):
        if value == 0:
            return value
        if value in self.coin_denominations:
            return self.coin_denominations.index(value)
        for r in range(value - 1, 1, -1):
            if r in self.coin_denominations:
                return self.coin_denominations.index(r)

    def cal_combination_all(self):
        matrix = [[1 for x in range(self.value+1)] for x in range(2)]
        coin_denom = 1
        row_index = 1
        while (coin_denom<self.coin_den_sz):
            coin_val = 0
            while (coin_val<self.value+1):
                x = matrix[row_index][coin_val - self.coin_denominations[coin_denom]] \
                    if coin_val - self.coin_denominations[coin_denom] >= 0 else 0
                if row_index==0:
                    y = matrix[row_index+1][coin_val] if coin_denom >= 1 else 0
                else:
                    y = matrix[row_index-1][coin_val] if coin_denom >= 1 else 0
                matrix[row_index][coin_val] = x + y
                coin_val += 1
            row_index += 1
            coin_denom += 1
            if row_index== 2:
                row_index -= 2
        result_row = row_index+1 if row_index==0 else row_index-1
        return matrix[result_row][self.value]

    def cal_combination(self, val, current_coin, right_most_coin, coin_restriction, num_coins):
        #first pruning - if value is larger than 0 and the restricted number of coins is reached
        if (val not in self.coin_denominations and num_coins==coin_restriction-1):
            return 0
        #return one solution if value becomes zero and add one to the number of solutions
        #if (val==0 and num_coins==coin_restriction):
        if (val in self.coin_denominations and num_coins==coin_restriction-1):
            num_coins += 1
            if num_coins not in self.collection:
                self.collection[num_coins] = 0
            self.collection[num_coins] += 1
            num_coins -= 1
            return 1
        #if value is zero but does not meet the number of coin requirements, just add one to the number of solutions
        #if (val==0 and num_coins!=coin_restriction):
        if (val in self.coin_denominations and num_coins==coin_restriction-1):
            num_coins += 1
            if num_coins not in self.collection:
                self.collection[num_coins] = 0
            self.collection[num_coins] += 1
            num_coins -= 1
        nCombinations = 0
        explored = []
        for index in range(current_coin, self.coin_den_sz):
            diff = val - self.coin_denominations[index]
            #second pruning - if a coin denomination is larger than value
            # if diff>=0:
            #     if num_coins<coin_restriction:
            if {self.coin_denominations[index], diff} not in self.temp_collection:
                num_coins += 1
                nCombinations += self.cal_combination(diff, index, right_most_coin, coin_restriction, num_coins)
                explored.append({self.coin_denominations[index], diff})
            num_coins -= 1
        return nCombinations

    def cal_combinations(self):
        amount = self.value
        nCoins = self.num_coins
        current_coin = 0
        right_most_coin = self.coin_den_sz - 1
        self.cal_combination(amount, current_coin, right_most_coin, self.max_coins, nCoins)
        nCombo = sum([self.collection[x] for x in range(self.min_coins, self.max_coins + 1)])
        print("Time taken (secs) = %.6f" % time.process_time())
        return nCombo

def read_file(input):
    with open(input) as f:
        file = f.readlines()
    file = [x.strip() for x in file]
    return file

def output_file(nCombo):
    with open('Outputresult.txt', 'a') as output:
        output.write(str(nCombo)+'\n')

if __name__ == "__main__":
    input_file = input("Enter your file path: ")
    #check file path and give an error if the path does not exist
    assert os.path.exists(input_file), "I did not find the file at, " + str(input_file)
    lines = read_file(input_file)
    for input in lines:
        # combination instance
        combSolution = Combinations()
        fields = input.strip().split()
        combSolution.value = int(fields[0])
        combSolution.find_prime(combSolution.value)
        if len(fields)==1:
            combSolution.max_coins = combSolution.value
        if len(fields)==2:
            combSolution.min_coins = int(fields[1])
            combSolution.max_coins = int(fields[1])
        if len(fields)==3:
            combSolution.min_coins = int(fields[1])
            combSolution.max_coins = int(fields[2])
        if combSolution.min_coins==1 and combSolution.max_coins==combSolution.value:
            nCombo = combSolution.cal_combination_all()
        else:
            nCombo = combSolution.cal_combinations()
        if combSolution.max_coins==combSolution.value:
            nCombo += 1
        output_file(nCombo)