import time
import math
import collections

class Combinations():
    def __init__(self):
        self.value = 100
        self.coinDenominations = []
        self.coinDenSz = 0
        self.numCoins = 0
        self.minCoins = 5
        self.maxCoins = 10
        self.collection = collections.OrderedDict()

    def find_prime(self, amount):
        self.coinDenominations.append(1)
        for num in range(2,amount):
            if is_prime(num):
                self.coinDenominations.append(num)
        #self.coinDenominations.append(amount)
        self.coinDenSz = len(self.coinDenominations)
        return self.coinDenominations

def integer_squareroot(num):
    x = num
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + num // x) // 2
    return x

def is_prime(num):
    if num==2:
        return True
    if num%2==0:
        return False
    root = integer_squareroot(num)
    #root = math.floor(math.sqrt(num))
    for n in range(3, root+1, 2):
        if num%n==0:
            return False
    return True

def find_largest_prime(remainder, coins):
    if remainder==0:
        return remainder
    if remainder in coins:
        return coins.index(remainder)
    for r in range(remainder-1,1,-1):
        if r in coins:
            return coins.index(r)

# def calCombination(solution, val, currentCoin, coinRestriction, numCoins):
#     #first pruning - value is still larger than 0 and the restricted number of coins is reached
#     if val>0 and numCoins==coinRestriction:
#         return 0
#     #return one solution if value becomes zero
#     if (val==0 and numCoins==coinRestriction) or (is_prime(val) and numCoins==coinRestriction-1):
#         return 1
#     nCombinations = 0
#     for index in range(currentCoin,solution.coinDenSz):
#         if val//solution.coinDenominations[(solution.coinDenSz-1)-index]<=coinRestriction: #solution.coinDenominations[index]>solution.coinDenominations[int(solution.coinDenSz/2)-1]:
#             #k = (solution.coinDenSz-1)-index
#             diff = val - solution.coinDenominations[index]
#             if diff>=0:
#                 if numCoins<coinRestriction:
#                     numCoins += 1
#                     nCombinations += calCombination(solution, diff, index, coinRestriction, numCoins)
#                 numCoins -= 1
#     return nCombinations

def calCombination(solution, val, currentCoin, coinRestriction, numCoins):
    #first pruning - value is larger than 0 and the restricted number of coins is reached
    if val>0 and numCoins==coinRestriction:
        return 0
    #return one solution if value becomes zero
    if (val==0 and numCoins==coinRestriction): #or (is_prime(val) and numCoins==coinRestriction-1):
        if numCoins not in solution.collection:
            solution.collection[numCoins] = 0
        solution.collection[numCoins] += 1
        return 1
    if (val==0 and numCoins!=coinRestriction):
        if numCoins not in solution.collection:
            solution.collection[numCoins] = 0
        solution.collection[numCoins] += 1
    nCombinations = 0
    for index in range(currentCoin,solution.coinDenSz):
        #if val//solution.coinDenominations[(solution.coinDenSz-1)-index]<=coinRestriction: #solution.coinDenominations[index]>solution.coinDenominations[int(solution.coinDenSz/2)-1]:
            #k = (solution.coinDenSz-1)-index
        diff = val - solution.coinDenominations[index]
        if diff>=0:
            if numCoins<coinRestriction:
                numCoins += 1
                nCombinations += calCombination(solution, diff, index, coinRestriction, numCoins)
        numCoins -= 1

    return nCombinations

# def calCombination(solution, val):
#     coins = solution.coinDenominations
#     coinDenSz = len(coins)
#     table = [[0 for x in range(coinDenSz)] for x in range(val + 1)]
#
#     # Fill the entries for 0 value case (n = 0)
#     for i in range(coinDenSz):
#         table[0][i] = 1
#
#     # Fill rest of the table entries in bottom up manner
#             x = table[i - coins[j]][j] if i - coins[j] >= 0 else 0
#
#             # Count of solutions excluding S[j]
#             y = table[i][j - 1] if j >= 1 else 0
#
#             # total count
#             table[i][j] = x + y
#
#     return table[val][coinDenSz - 1]

# def calCombination(solution, val):
#     coins = solution.coinDenominations
#     coin_denom_sz = len(coins)
#     values = [x for x in range(val+1)]
#     matrix = [[1 for x in range(val+1)] for x in range(coin_denom_sz)]
#
#     # for col in range(val+1):
#     #     matrix[0][col] = 1
#
#     coin_denom = 1
#     row_index = 1
#     while (coin_denom<coin_denom_sz):
#         coin_val = 0
#         while (coin_val<val+1):
#             x = matrix[row_index][coin_val - coins[coin_denom]] if coin_val - coins[coin_denom] >= 0 else 0
#             if row_index==0:
#                 y = matrix[row_index+1][coin_val] if coin_denom >= 1 else 0
#             else:
#                 y = matrix[row_index-1][coin_val] if coin_denom >= 1 else 0
#             matrix[row_index][coin_val] = x + y
#             coin_val += 1
#         row_index += 1
#         coin_denom += 1
#         if row_index== 2:
#             row_index -= 2
#     return matrix[1][val]

# def calCombination(solution, val):
#     coins = solution.coinDenominations
#     coin_denom_sz = len(coins)
#     values = [x for x in range(val+1)]
#     matrix = [[ [1,{}] for x in range(val+1)] for x in range(coin_denom_sz)]
#
#     for col in range(val+1):
#         if col==0:
#             matrix[0][col][1][0] = 1
#         else:
#             matrix[0][col][1][col] = 1
#             matrix[0][col][1][col-1] = 0
#
#     coin_denom = 1
#     row_index = 1
#     while (coin_denom<coin_denom_sz):
#         coin_val = 0
#         while (coin_val<val+1):
#             x = matrix[row_index][coin_val - coins[coin_denom]][0]if coin_val - coins[coin_denom] >= 0 else 0
#             y = matrix[row_index-1][coin_val][0] if coin_denom >= 1 else 0
#             matrix[row_index][coin_val][0] = x + y
#             add_one_coin(matrix[row_index][coin_val][1])
#             cur_diff = matrix[row_index][coin_val][0] - matrix[row_index-1][coin_val][0]
#             prev_diff = matrix[row_index][coin_val-1][0] - matrix[row_index-1][coin_val-1][0]
#             diff = cur_diff-prev_diff
#             if diff>=1:
#                 num_coins = coin_val//coins[coin_denom]+cal_remainder(matrix[row_index][coin_val%coins[coin_denom]][1])
#                 for k,v in matrix[row_index][coin_val][1].items():
#                     for sub_k,sub_v in matrix[(coin_val%coins[coin_denom])][coin_val][1].items():
#
#                 matrix[row_index][coin_val][1][num_coins] += 1
#             coin_val += 1
#         row_index += 1
#         coin_denom += 1
#     return matrix[coin_denom-1][val]

# def calCombination(solution, val):
#     coins = solution.coinDenominations
#     coin_denom_sz = len(coins)
#     matrix = [[ [1,{}] for x in range(val+1)] for x in range(coin_denom_sz)]
#
#     for col in range(val+1):
#         if col==0:
#             matrix[0][col][1][0] = 1
#         else:
#             matrix[0][col][1][col] = 1
#             matrix[0][col][1][col-1] = 0
#
#     coin_denom = 1
#     row_index = 1
#     while (coin_denom<coin_denom_sz):
#         coin_val = 0
#         while (coin_val<val+1):
#             x = matrix[row_index][coin_val - coins[coin_denom]][0]if coin_val - coins[coin_denom] >= 0 else 0
#             real_index = row_index - 1
#             y = matrix[real_index][coin_val][0] if coin_denom >= 1 else 0
#             matrix[row_index][coin_val][0] = x + y
#             matrix[row_index][coin_val][1] = matrix[real_index][coin_val][1].copy()
#
#             cur_diff = matrix[row_index][coin_val][0] - matrix[real_index][coin_val][0]
#             prev_diff = matrix[row_index][coin_val - 1][0] - matrix[real_index][coin_val - 1][0]
#             if prev_diff<0:
#                 prev_diff = cur_diff
#             diff = cur_diff-prev_diff
#
#             if diff>=1:
#                 k = coin_val // coins[coin_denom]
#                 if k not in matrix[row_index][coin_val][1]:
#                     matrix[row_index][coin_val][1][k] = 0
#                 matrix[row_index][coin_val][1][k] += 1
#                 remainder = coin_val % coins[coin_denom]
#                 largest_prime = find_largest_prime(remainder, coins)
#                 if remainder!=0:
#                     for sub_k,sub_v in matrix[largest_prime][remainder][1].items():
#                         k_copy = k+sub_k
#                         if k_copy not in matrix[row_index][coin_val][1]:
#                             matrix[row_index][coin_val][1][k_copy] = 0
#                         matrix[row_index][coin_val][1][k_copy] += sub_v
#                     matrix[row_index][coin_val][1][k] -= 1
#
#             #add one coin to previous values if not counted
#             if coin_val>coins[coin_denom]:
#                 for key, value in matrix[row_index][coin_val - 1][1].items():
#                     if key != val:
#                         next_k = key + 1
#                         if next_k not in matrix[row_index][coin_val][1]:
#                             matrix[row_index][coin_val][1][next_k] = 0
#                         if matrix[row_index][coin_val][1][next_k] < value:
#                             matrix[row_index][coin_val][1][next_k] = value
#             #add checking
#             check = sum(matrix[row_index][coin_val][1].values())
#             index = 1
#             if matrix[row_index][coin_val][0]>check:
#                 ordered_matrix = collections.OrderedDict(sorted(matrix[row_index][coin_val-1][1].items()))
#                 smallest = val
#                 for k in ordered_matrix.keys():
#                     if k < smallest and ordered_matrix[k]!=0:
#                         smallest = k
#                 if smallest+index not in matrix[row_index][coin_val][1].keys():
#                     matrix[row_index][coin_val][1][smallest+index] = 1
#                 else:
#                     matrix[row_index][coin_val][1][smallest+index] += 1
#                 #check = sum(matrix[row_index][coin_val][1].values())
#                 #index += 1
#             check2 = sum(matrix[row_index][coin_val][1].values())
#             if matrix[row_index][coin_val][0]>check2:
#                 ordered_matrix = collections.OrderedDict(sorted(matrix[row_index-1][coin_val][1].items()))
#                 smallest = val
#                 for k in matrix[row_index-1][coin_val][1].keys():
#                     if k < smallest and ordered_matrix[k] != 0:
#                         smallest = k
#                 if smallest not in matrix[row_index][coin_val][1].keys():
#                     matrix[row_index][coin_val][1][smallest] = 1
#                 else:
#                     matrix[row_index][coin_val][1][smallest] += 1
#             check3 = sum(matrix[row_index][coin_val][1].values())
#             if matrix[row_index][coin_val][0]>check3:
#                 for
#                 k = coin_val
#             print("row index: ", row_index, "coin_val: ", coin_val, " diff: ", matrix[row_index][coin_val][0]-check3)
#                 # #print("k: ", k)
#                 # remainder = coin_val - coins[coin_denom]*(k-1)
#                 # #print("remainder: ", remainder)
#                 # largest_prime = find_largest_prime(remainder, coins)
#                 # #print("l_prime: ", largest_prime)
#                 # ordered_matrix = collections.OrderedDict(sorted(matrix[largest_prime][remainder][1].items()))
#                 # #print(matrix[largest_prime][remainder][1])
#                 # smallest = val
#                 # for k,v in ordered_matrix.items():
#                 #     if k < smallest and ordered_matrix[k]!=0:
#                 #         smallest = k
#                 # if smallest + (k-1) not in matrix[row_index][coin_val][1].keys():
#                 #     matrix[row_index][coin_val][1][smallest + (k-1)] = 1
#                 # else:
#                 #     matrix[row_index][coin_val][1][smallest + (k-1)] += 1
#
#                 # check2 = sum(matrix[row_index][coin_val][1].values())
#                     # if remainder+1 not in matrix[row_index][coin_val][1]:
#                     #     matrix[row_index][coin_val][1][remainder+1] = 1
#             #         else:
#             #             matrix[row_index][coin_val][1][remainder+1] += 1
#
#             coin_val += 1
#         row_index += 1
#         coin_denom += 1
#     result = 0
#     for n_coins, sols in matrix[coin_denom_sz-1][val][1].items():
#         if n_coins >= solution.minCoins and n_coins <= solution.maxCoins:
#             result += sols
#     print(result)
#     return matrix[coin_denom_sz-1][val][1]

def calCombinations():
    combSolution = Combinations()
    combSolution.find_prime(combSolution.value)
    amount = combSolution.value
    nCoins = combSolution.numCoins
    # coinDenMin = amount//combSolution.maxCoins
    # coinDenMax = val//solution.minCoins+1
    nCombo = 0
    for coin in range(combSolution.maxCoins, combSolution.maxCoins-1, -1):
        if coin==1 or coin==combSolution.value:
            nCombo += 1
        else:
            nCombo += calCombination(combSolution, amount, 0, coin, nCoins)
    print(combSolution.collection)
    nCombo = sum([combSolution.collection[x] for x in range(5,11)])
    print("Time taken (secs) = %.6f" % time.process_time())
    return nCombo

if __name__ == "__main__":
    nCombo = calCombinations()
    print(nCombo)
    # print("Hello world")