import time
import math
import os
import collections

class Combinations():
    """This class solves the number of combination with or without restricting the number of coins used."""
    def __init__(self):
        self.value = 0
        self.coin_denominations = []
        self.coin_den_sz = 0
        self.num_coins = 0
        self.min_coins = 1
        self.max_coins = 0
        self.collection = collections.OrderedDict()

    def find_prime(self, amount):
        #make a list of prime numbers smaller than value including 1
        self.coin_denominations.append(1)
        for num in range(2,amount):
            if self.is_prime(num):
                self.coin_denominations.append(num)
        self.coin_den_sz = len(self.coin_denominations)
        return self.coin_denominations

    def is_prime(self, num):
        #number is two, prime
        if num==2:
            return True
        #if number is divided by 2 and no remaining value,
        #it is not a prime
        if num%2==0:
            return False
        root = math.floor(math.sqrt(num))
        #as the multiplication of 2s are removed, we can check odd numbers only now
        for n in range(3, root+1, 2):
            if num%n==0:
                return False
        return True

    def cal_combination_all(self):
        #initialise matrix with two rows and value+1 columns and fill them with 1s
        matrix = [[1 for x in range(self.value+1)] for x in range(2)]
        coin_denom = 1
        row_index = 1
        while (coin_denom<self.coin_den_sz):
            coin_val = 0
            while (coin_val<self.value+1):
                #x represents previous number of solutions found for smaller values (column-wise solutions)
                x = matrix[row_index][coin_val - self.coin_denominations[coin_denom]] \
                    if coin_val - self.coin_denominations[coin_denom] >= 0 else 0
                #y represents previous number of solutions found for smaller denominations (row-wise solutions)
                if row_index==0:
                    y = matrix[row_index+1][coin_val] if coin_denom >= 1 else 0
                else:
                    y = matrix[row_index-1][coin_val] if coin_denom >= 1 else 0
                #add x and y to get the total solutions for the specific row and column intersection
                matrix[row_index][coin_val] = x + y
                coin_val += 1
            row_index += 1
            coin_denom += 1
            #because there are only two rows, alternating most recent solutions are done within two rows
            if row_index== 2:
                row_index -= 2
        #as row_index was added before this (due to row_index+=1), the result row should be the other row
        result_row = row_index+1 if row_index==0 else row_index-1
        print("Time taken (secs) = %.6f" % time.process_time())
        return matrix[result_row][self.value]

    def cal_combination(self, val, current_coin, coin_restriction, num_coins):
        coin_check = num_coins==coin_restriction-1
        #first pruning - if remaining value is not a prime number and the restricted number of coins-1 is reached, do not expand
        if (val not in self.coin_denominations and coin_check):
            return 0
        #return one solution if remaining value is a prime number or 1 and add one to the number of solutions
        if (val in self.coin_denominations and coin_check):
            num_coins += 1
            if num_coins not in self.collection:
                self.collection[num_coins] = 0
            self.collection[num_coins] += 1
            num_coins -= 1
            return 1
        #if remaining value is a prime number or 1 but does not meet the number of coin requirements,
        #just add one to the number of solutions for different number of coins used
        if (val in self.coin_denominations and not coin_check):
            num_coins += 1
            if num_coins not in self.collection:
                self.collection[num_coins] = 0
            self.collection[num_coins] += 1
            num_coins -= 1
        nCombinations = 0
        for index in range(current_coin, self.coin_den_sz):
            diff = val - self.coin_denominations[index]
            #second pruning - if the remaining difference is smaller than coin_denomination, do not expand
            #because we need combinations not permutations
            if diff >= self.coin_denominations[index]:
                num_coins += 1
                nCombinations += self.cal_combination(diff, index, coin_restriction, num_coins)
            else:
                return 0
            num_coins -= 1
        return nCombinations

    def cal_combinations(self):
        amount = self.value
        nCoins = self.num_coins
        current_coin = 0
        #run the maximum number of coins case
        #because the number of solutions for smaller number of coins will be discovered
        #and stored in the dictionary collection during run time
        self.cal_combination(amount, current_coin, self.max_coins, nCoins)
        #sum up the number of solutions between min_coins and max_coins
        nCombo = sum([self.collection[x] for x in range(self.min_coins, self.max_coins + 1)])
        print("Time taken (secs) = %.6f" % time.process_time())
        return nCombo

def read_file(input):
    with open(input) as f:
        file = f.readlines()
    file = [x.strip() for x in file]
    return file

def output_file(nCombo):
    with open('Output.txt', 'a') as output:
        output.write(str(nCombo)+'\n')

if __name__ == "__main__":
    input_file = input("Enter your file path: ")
    #check file path and give an error if the path does not exist
    assert os.path.exists(input_file), "I did not find the specified file at, " + str(input_file)
    lines = read_file(input_file)
    for input in lines:
        #combinatorial solution instance
        combSolution = Combinations()
        fields = input.strip().split()
        combSolution.value = int(fields[0])
        combSolution.find_prime(combSolution.value)
        #if only one field, min_coins = 1 and max_coins = value
        if len(fields)==1:
            combSolution.max_coins = combSolution.value
        #if two fields, min_coins and max_coins = second field
        if len(fields)==2:
            combSolution.min_coins = int(fields[1])
            combSolution.max_coins = int(fields[1])
        #if three fields, min_coins = second field and max_coins = third field
        if len(fields)==3:
            combSolution.min_coins = int(fields[1])
            combSolution.max_coins = int(fields[2])
        #if all solutions need to be found, use dynamic programming
        if combSolution.min_coins==1 and combSolution.max_coins==combSolution.value:
            nCombo = combSolution.cal_combination_all()
        #else backtracking and pruning
        else:
            nCombo = combSolution.cal_combinations()
        #acount for the gold coin solution if min_coins = 1
        if combSolution.min_coins==1:
            nCombo += 1
        output_file(nCombo)