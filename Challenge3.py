# ---------------------------------------------------------------------------
# Author: Doruk Aksoy
# Date: 04/02/2020
# Data Incubator Application Challenge 3
# ---------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
plt.close("all")
"""
Coins with values 1 through N (inclusive) are placed into a bag. 
All the coins from the bag are iteratively drawn (without replacement) at 
random. For the first coin, you are paid the value of the coin. For subsequent 
coins, you are paid the absolute difference between the drawn coin and the 
previously drawn coin. For example, if you drew 5,3,2,4,1, your payments 
would be 5,2,1,2,3 for a total payment of 13.

Please provide 5 digits of precision for all answers.
"""
# Function to calculate random draw total payment  
def randomDrawTotPay(N):
    # Coins in the bag
    coins = np.random.choice(N, N, replace=False)+1
    # Array to keep track of the payments
    pay = np.zeros(np.size(coins,axis=0),dtype=int)
    # For each coin in the bag
    for ind,val in enumerate(coins):
        # First coin pays the value of the coin
        if (ind==0): pay[ind] = val
        # Rest of them pay the absolute difference
        else: pay[ind] = np.abs(val-coins[ind-1])
    # Return total payment
    return pay.sum()

# Number of iterations
n_iterations = 1000000
# Initialize arrays to keep track of total payments
q10 = np.zeros(n_iterations,dtype=float)
q20 = np.zeros(n_iterations,dtype=float)
# For each iteration
for s in range(n_iterations):
    # Define a seed for random calculations
    np.random.seed(s)
    # Calculate total payments for N = 10
    q10[s] = randomDrawTotPay(10)
    # Calculate total payments for N = 20
    q20[s] = randomDrawTotPay(20)   

plt.hist(q10)
plt.hist(q20)

# Question 1
"""
What is the mean of your total payment for N=10?
"""
print("Q1:",np.round(q10.mean(),5))

# Question 2
"""
What is the mean of your total payment for N=20?
"""
print("Q2:",np.round(q20.mean(),5))

# Question 3
"""
What is the probability that your total payment is greater than or equal to 45 for N=10?
"""   
print("Q3:",np.round(np.size(q10[q10>=45])/np.size(q10),5))

# Question 4
"""
What is the standard deviation of your total payment for N=10?
"""
print("Q4:",np.round(q10.std(),5))

# Question 5
"""
What is the standard deviation of your total payment for N=20?
"""
print("Q5:",np.round(q20.std(),5))
# Question 6
"""
What is the probability that your total payment is greater than or equal to 160 for N=20?
"""
print("Q6:",np.round(np.size(q20[q20>=160])/np.size(q20),5))
    