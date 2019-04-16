import time
import math
import os
import collections

class Combinations():
    def __init__(self):
        self.value = 0
        self.coinDenominations = []
        self.coinDenSz = 0
        self.numCoins = 0
        self.minCoins = 1
        self.maxCoins = 0
        self.collection = collections.OrderedDict()

    def find_prime(self, amount):
        self.coinDenominations.append(1)
        for num in range(2,amount):
            if self.is_prime(num):
                self.coinDenominations.append(num)
        self.coinDenSz = len(self.coinDenominations)
        return self.coinDenominations
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

    def calCombinationAll(self):
        matrix = [[1 for x in range(self.value+1)] for x in range(2)]
        coin_denom = 1
        row_index = 1
        while (coin_denom<self.coinDenSz):
            coin_val = 0
            while (coin_val<self.value+1):
                x = matrix[row_index][coin_val - self.coinDenominations[coin_denom]] \
                    if coin_val - self.coinDenominations[coin_denom] >= 0 else 0
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

    def calCombination(self, val, currentCoin, coinRestriction, numCoins):
        #first pruning - value is larger than 0 and the restricted number of coins is reached
        if val>0 and numCoins==coinRestriction:
            return 0
        #return one solution if value becomes zero
        if (val==0 and numCoins==coinRestriction):
            if numCoins not in self.collection:
                self.collection[numCoins] = 0
            self.collection[numCoins] += 1
            return 1
        if (val==0 and numCoins!=coinRestriction):
            if numCoins not in self.collection:
                self.collection[numCoins] = 0
            self.collection[numCoins] += 1
        nCombinations = 0
        for index in range(currentCoin,self.coinDenSz):
            diff = val - self.coinDenominations[index]
            if diff>=0:
                if numCoins<coinRestriction:
                    numCoins += 1
                    nCombinations += self.calCombination(diff, index, coinRestriction, numCoins)
            numCoins -= 1
        return nCombinations

    def calCombinations(self):
        amount = self.value
        nCoins = self.numCoins
        currentCoin = 0
        self.calCombination(amount, currentCoin, self.maxCoins, nCoins)
        nCombo = sum([self.collection[x] for x in range(self.minCoins,self.maxCoins+1)])
        print("Time taken (secs) = %.6f" % time.process_time())
        return nCombo

def readFile(input):
    with open(input) as f:
        file = f.readlines()
    file = [x.strip() for x in file]
    return file

def outputFile(nCombo):
    with open('Outputresult.txt', 'a') as output:
        output.write(str(nCombo)+'\n')

if __name__ == "__main__":
    input_file = input("Enter your file path: ")
    #check file path and give an error if the path does not exist
    assert os.path.exists(input_file), "I did not find the file at, " + str(input_file)
    lines = readFile(input_file)
    for input in lines:
        # combination instance
        combSolution = Combinations()
        fields = input.strip().split()
        combSolution.value = int(fields[0])
        combSolution.find_prime(combSolution.value)
        if len(fields)==1:
            combSolution.maxCoins = combSolution.value
        if len(fields)==2:
            combSolution.minCoins = int(fields[1])
            combSolution.maxCoins = int(fields[1])
        if len(fields)==3:
            combSolution.minCoins = int(fields[1])
            combSolution.maxCoins = int(fields[2])
        if combSolution.minCoins==1 and combSolution.maxCoins==combSolution.value:
            nCombo = combSolution.calCombinationAll()
        else:
            nCombo = combSolution.calCombinations()
        if combSolution.maxCoins==combSolution.value:
            nCombo += 1
        outputFile(nCombo)