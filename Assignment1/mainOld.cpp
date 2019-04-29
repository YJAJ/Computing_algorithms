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
    private:
        std::vector<int> coinDenominations;
        int value;
        int minNumCoins;
        int maxNumCoins;
        int numCoins;
        std::map<int, int> collections;

    public:
        static int numCombinations;
        //static int numCoins;
        Combinations()
        {
            value = 100;
            coinDenominations = findPrime(value);
            minNumCoins = 8;
            maxNumCoins = 25;
            numCoins = 0;
            collections = {};
        }
        //getters
        std::vector<int> getCoinDen()
        {
            return coinDenominations;
        }
        int getValue()
        {
            return value;
        }
        int getMinNumCoins()
        {
            return minNumCoins;
        }
        int getMaxNumCoins()
        {
            return maxNumCoins;
        }
        int getNumCoins()
        {
            return numCoins;
        }
        int getNumCombinations()
        {
            return numCombinations;
        }
        std::map<int, int> getCollections()
        {
            return collections;
        }
        //setters
        int setNumCoins()
        {
            return ++numCoins;
        }
        void setNumCombinations()
        {
            ++numCombinations;
        }
        void setCollections(int numCoins)
        {
            collections[numCoins] = 0;
        }
        void addCollections(int numCoins)
        {
            collections[numCoins] += 1;
        }
        //calculate remaining value
        int calRemainingValue(int amount, int subValue)
        {
            return amount - subValue;
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
            coinDenom.push_back(amount);
            return coinDenom;
        }
};

//int Combinations::numCombinations = 0;
//int Combinations::numCoins = 0;

// int calCombination(Combinations solution, int val, int currentCoin)
// {
//     std::vector<int> coins = solution.getCoinDen();
//     auto coinDenSz = coins.size();

//     cout << "amount " << val << '\n';
//     if (val==0)
//     {
//         //cout << "nCombo " << nCombo << '\n';
//         return 1;
//     }
//     if (val<0)
//     {
//         return 0;
//     }
//     int nCombinations = 0;
//     for (int index = currentCoin; index < coinDenSz; ++index)
//     {
//         nCombinations += calCombination(solution, val-coins[index], index);
//     }
//     return nCombinations;
// }

// int calCombination(Combinations &solution, int val, int currentCoin, int coinRestriction, int numCoins)
// {
//     std::vector<int> coins = solution.getCoinDen();
//     auto coinDenSz = coins.size();

//     if (val>0 && numCoins==coinRestriction)
//     {
//         return 0;
//     }
//     if (val==0 && numCoins==coinRestriction)
//     { 
//         if (solution.getCollections().find(numCoins)==solution.getCollections().end())
//         {
//             solution.setCollections(numCoins);
//         }
//         solution.addCollections(numCoins);
//         return 1;
//     }
//     if (val==0 && numCoins!=coinRestriction)
//     { 
//         if (solution.getCollections().find(numCoins)==solution.getCollections().end())
//         {
//             solution.setCollections(numCoins);
//         }
//         solution.addCollections(numCoins);
//     }

//     int nCombinations = 0;
//     for (int index = currentCoin; index < coinDenSz; ++index)
//     {
//         int diff = val-coins[index];
//         if (diff>=0)
//         {
//             if (numCoins<coinRestriction)
//             {
//                 ++numCoins;
//                 nCombinations += calCombination(solution, diff, index, coinRestriction, numCoins);
//             }
//             --numCoins;
//         }
//     }
//     return nCombinations;
// }

int calCombination(Combinations &solution, int val, int currentCoin, int coinRestriction, int numCoins)
{
    std::vector<int> coins = solution.getCoinDen();
    auto coinDenSz = coins.size();

    if ((std::find(coins.begin(), coins.end(), val) == coins.end()) && numCoins==coinRestriction-1)
    {
        return 0;
    }
    if ((std::find(coins.begin(), coins.end(), val) != coins.end()) && numCoins==coinRestriction-1)
    { 
        ++numCoins;
        if (solution.getCollections().find(numCoins)==solution.getCollections().end())
        {
            solution.setCollections(numCoins);
        }
        solution.addCollections(numCoins);
        --numCoins;
        return 1;
    }
    if ((std::find(coins.begin(), coins.end(), val) != coins.end())  && numCoins!=coinRestriction-1)
    { 
        ++numCoins;
        if (solution.getCollections().find(numCoins)==solution.getCollections().end())
        {
            solution.setCollections(numCoins);
        }
        solution.addCollections(numCoins);
        --numCoins;
    }

    int nCombinations = 0;
    for (int index = currentCoin; index < coinDenSz; ++index)
    {
        int diff = val-coins[index];
        if (diff>=coins[index])
        {
            ++numCoins;
            nCombinations += calCombination(solution, diff, index, coinRestriction, numCoins);
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
    Combinations combSolution = Combinations();
    int amount = combSolution.getValue();
    int nCombo = 0;
    int nCoins = combSolution.getNumCoins();

    calCombination(combSolution, amount, 0, combSolution.getMaxNumCoins(), nCoins);

    // std::map<int, int> copy = combSolution.getCollections();
    // for (std::map<int, int>::iterator i = copy.begin(); i != copy.end(); ++i)
    // {
    //     std::cout << i->first << ' ' << i->second << ' ';
    // }
    for (int coin = combSolution.getMinNumCoins(); coin < combSolution.getMaxNumCoins()+1; ++coin)
    {
        nCombo += combSolution.getCollections()[coin];
    }
    return nCombo;
}

int main()
{
    clock_t start_t, end_t;
    start_t = clock();

    // std::vector<std::vector<int> > data;
    // std::string line_;
    // //open file
    // ifstream file_("input.txt");
    // //if file is open
    // if (file_.is_open())
    // {
    //     //while reading in line by line
    //     while(getline(file_, line_))
    //     {
    //         std::vector<int> lineData;
    //         std::vector<int> numData;
    //         stringstream beforeSplit(line_);
    //         string value;

    //         while(getline(beforeSplit, value, ' '))
    //         {
    //             lineData.push_back(std::stoi(value));
    //         }
    //         // for (std::vector<int>::const_iterator i = lineData.begin(); i != lineData.end(); ++i)
    //         // {
    //         //     std::cout << *i << ' ';
    //         // }
            
    //         data.push_back( lineData );
    //         // if (!l || iCount < 0)
    //         // {
    //         //     std::cout << "Error in the input file - not an integer." << endl;
    //         // }
    //         // else
    //         // {
    //         //     std::vector<int> lineData;
    //         //     int value;
    //         //     while ( lineData.size() != iCount && l >> value ) 
    //         //     {
    //         //         lineData.push_back( value ) ;
    //         //     }
    //         //     if ( lineData.size() == iCount ) 
    //         //     {
    //         //         data.push_back( lineData );
    //         //     }
    //         //     // for (std::vector<int>::const_iterator i = lineData.begin(); i != lineData.end(); ++i)
    //         //     // {
    //         //     //     std::cout << *i << ' ';
    //         //     // }
    //         // }
    //     }
    //     int k = 0;
    //     for (std::vector<std::vector<int>>::const_iterator i = data.begin(); i != data.end(); ++i, ++k)
    //     {
    //         for (std::vector<int>::const_iterator j = i->begin(); j != i->end(); ++j)
    //         std::cout << k << *j << '\n';
    //     }

    //     file_.close();
    // }
    // else
    // {
    //     std::cout << "Failed to open the input file." << endl;
    // }
    

    int nC;
    nC = calCombinations();
    cout << nC << '\n';
    
    end_t = clock();
    double cpu_time_used = ((double) (end_t - start_t))/CLOCKS_PER_SEC;
    cout.precision(6);
    std::cout << "I have slept for " << std::fixed << cpu_time_used << " seconds." <<endl;

    return 0;
}