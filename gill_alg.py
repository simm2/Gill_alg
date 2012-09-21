import numpy as np
import matplotlib.pyplot as plt
import random
from math import *
import operator as op

#this is a helper function to calclate the combinitorial function "N choose k"

def ncr(n,r):
    if r == 0:
        return n
    elif n == 0:
        return 0
    elif r > n:
        return 0
    else:
        return factorial(n)/(factorial(n-r)*factorial(r))
# This function creates a placeholder for the arbitrary dictionary of reactions 
# in our system that this program will simulate
def ReactionList():
    l = [[['x'],['c']    ,.05]]     

    return l

# This is a placeholder for our initial population vector
def PopulationVector():
    d = {'x':1000,
         'c':0,}

    return d
    
# This function retrieves the reaction rates from our dictionary and returns
# them in a list that will become our reaction rate vector. It takes our
# reaction rate dictionary as a parameter.
def Cmu(RList):
    c_mu = []
    for reactants,products,rate in RList:
        c_mu.append(rate)
    return c_mu


def calcM(RList):
    """This function returns the number of reactions in our dictionary"""
    M = len(RList)
    return M


def calcN(Rlist):
    species = sum([reactants + products 
                   for (reactants,products,rate) in Rlist],[])
    return len(set(species))

# this function is used to caclulate the discrete RV mu in step 2 of this
# algorithim. mu is the index of the reaction that occurs which leads to the
# next system state. The function takes as parameters: the dictionary a_0, a
# uniform RV r_2, and the sum of all values in a_0 (which is calculated in
# Step 1)
def calcMu(a_0,r_2,a_sum):
    s = 0
    v = int()
    while s < a_sum*r_2:
        s = s + a_0[v]
        v = v + 1
    return v

# This function calculates h_i for every species of reactants and stores them
# to a list which the function returns. The function takes our reaction list
# and our population dictionary as parameters 
def calc_h(RList,X_i):
    h_mu=[]
    for reactants,products,rate in RList:
        h_i = [ncr(X_i[species],reactants.count(species))
                                    for species in set(reactants)]
        h_mu.append(reduce(op.mul,h_i))
    return h_mu

     

def main():

    # Step 0: initilize values
    # call our dictionary
    RList = ReactionList()
    # c_mu: the reaction constans for each defined reaction
    #       value is the average probability reaction mu will occur in the next
    #       infitesimal time period dt
    c_mu = Cmu(RList)
    # X_i: population of each reactant species
    X_i = PopulationVector()
    # M: number of possible reactions in system
    M = calcM(RList)
    # N: number of molecule species in system
    N = calcN(RList) 
    # pop: the development of molecule X population over time
    pop = list()
    # time: the list of times when a defined reaction occurs
    time = list()
    # initial start time and reaction counter
    t = 0
    counter = 0



    # define conditions for when algorithim is run
    while counter <= 1000:
        # Step 1: parameter calculation
        # update value of h
        # h: the number of distinct reactant combinations availible in the state
        h_mu = calc_h(RList,X_i)
        # calculate each a_mu and take thier sum
        # a_mu:average probability reaction mu will occur given the curent state
        #      of the system
        a_0 = [c_mu[i]*h_mu[i] for i in range(M)]
        a_sum = sum(a_0)
        # When a_sum is 0 there is no posible reaction that can occour in the
        # System. When this occours, end the algorithim here
        if a_sum == 0:
            break
        # Step 2: Monte-Carlo simulation
        # generate r_1 and r_2
        r_1 = random.uniform(0,1)
        r_2 = random.uniform(0,1)
        # calculate the continuous RV tau
        # tau: time till reaction mu that leads to the next system state
        tau = (1/a_sum)*log(1/r_1)
        # calculate the discrete RV mu
        # mu: the index number that identifies the reaction that occurs
        mu = calcMu(a_0,r_2,a_sum)
        # Step 3: System update and data record
        # update the system time and add to the list
        t = t + tau
        time.append(t)
        # update the population levels in the system and add them to the list
        reaction = RList[mu-1]
        for reactants in reaction[0]:
            X_i[reactants] -= 1
        for products in reaction[1]:
            X_i[products] += 1
            
        
    
        

        
        #reaction counter increases
        counter += 1

    #test code here
    
    print pop
    x = [X_i['x'] for X_i in pop]
    


    
print('loaded...')

main()
