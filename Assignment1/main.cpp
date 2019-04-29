#include <iostream>
#include <iterator>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <vector>
#include <string>
#include <ctime>
#include <cstdio>
#include <map>

using namespace std;

class Combinations
{
    public:
        int value;
        int minNumCoins;
        int maxNumCoins;
        std::vector<int> coinDenominations;
        std::map<int, int> collections;
        Combinations()
        {
            value = 100;
            coinDenominations = findPrime(value);
            minNumCoins = 8;
            maxNumCoins = 25;
            collections = {};
        }
        //is this number a prime number
        bool isPrime(int num)
        {
            if (num==2)
            {
                return true;
            }
            if (num%2==0)
            {
                return false;
            }
            for (int i=3; i * i <= num; i+=2)
            {
                if (num%i==0)
                {
                    return false;
                }
            }
            return true;
        }
        //build an array of prime numbers
        std::vector<int> findPrime(int amount)
        {
            std::vector<int> coinDenom;
            coinDenom.push_back(1);
            for (int num=2; num<amount; ++num)
            {
                if (isPrime(num))
                {
                    coinDenom.push_back(num);
                }
            }
            return coinDenom;
        }
        int calCombination(int &val, int &currentCoin, int &coinRestriction, int &numCoins)
        {
            auto coinDenSz = coinDenominations.size();
            bool coinCheck = numCoins==coinRestriction-1;

            if ((std::find(coinDenominations.begin(), coinDenominations.end(), val) == coinDenominations.end()) && coinCheck)
            {
                return 0;
            }
            if ((std::find(coinDenominations.begin(), coinDenominations.end(), val) != coinDenominations.end()) && coinCheck)
            { 
                ++numCoins;
                if (collections.find(numCoins)==collections.end())
                {
                    collections[numCoins] = 0;
                }
                collections[numCoins] += 0;;
                --numCoins;
                return 1;
            }
            if ((std::find(coinDenominations.begin(), coinDenominations.end(), val) != coinDenominations.end())  && !coinCheck)
            { 
                ++numCoins;
                if (collections.find(numCoins)==collections.end())
                {
                    collections[numCoins] = 0;
                }
                collections[numCoins] += 0;;
                --numCoins;
            }

            int nCombinations = 0;
            for (int index = currentCoin; index < coinDenSz; ++index)
            {
                int diff = val-coinDenominations[index];
                if (diff>=coinDenominations[index])
                {
                    ++numCoins;
                    nCombinations += calCombination(diff, index, coinRestriction, numCoins);
                }
                else
                {
                    return 0;
                }
                --numCoins;
            }
            return nCombinations;
        }

        int calCombinations()
        {
            int amount = value;
            int nCombo = 0;
            int numCoins = 0;
            int currentCoins = 0;
            calCombination(amount, currentCoins, maxNumCoins, numCoins);

            for (int coin = minNumCoins; coin < maxNumCoins+1; ++coin)
            {
                nCombo += collections[coin];
            }
            ++nCombo;
            return nCombo;
        }
};

int main()
{
    clock_t start_t, end_t;
    start_t = clock();
    Combinations combSolution = Combinations();
    int nC = combSolution.calCombinations();
    cout << nC << '\n';
    
    end_t = clock();
    double cpu_time_used = ((double) (end_t - start_t))/CLOCKS_PER_SEC;
    cout.precision(6);
    std::cout << "I have slept for " << std::fixed << cpu_time_used << " seconds." <<endl;

    return 0;
}