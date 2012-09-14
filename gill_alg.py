import numpy as np
import matplotlib.pyplot as plt
import random
import math

#this is a helper function to test a value to see if its a list
def RepresentsList(s):
    try: 
        list(s)
        return True
    except ValueError:
        return False

# This function creates a placeholder for the arbitrary dictionary of reactions 
# in our system that this program will simulate
def ReactionList():
    d = [[['Y_1']      ,['Y_2']            ,.01],
         [['Y_1','Y_2'],['Z_1']            ,.05],
         [['Y_1']      ,['Y_1','Y_1','Y_3'],.02],
         [['Y_1','Y_1'],['Z_2']            ,.03],
         [['Y_3','Y_2'],['Y_2']            ,.01]]

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

# This function returns the number of molecule species in our dictionary
# def calcN(RList):-
#     N = 0
#     for reactants,products,rate in RList:
#         Nlist = reactants+products
#             p = set(l)
#             for v in p:
#                 N += 1
#     return N

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
    v = 1
    while s < a_sum*r_2:
        s = s + a_0['a_'+str(v)]
        v = v + 1
    return v-1

def main():

    # Step 0: initilize values
    # call our dictionary
    RList = ReactionList()
    # c_mu: the reaction constans for each defined reaction
    #       value is the average probability reaction mu will occur in the next
    #       infitesimal time period dt
    c = Cmu(RList)
    # X_i: population of each reactant species
    X_i = [1000,2000,3000,4000,5000,6000] #Method of input from outside module?
    # M: number of possible reactions in system
    M = calcM(RList)
    # N: number of molecule species in system
    N = calcN(RList) 
    # pop: the development of molecule X population over time
    pop = list()
    # time: the list of times when a defined reaction occurs
    time = list()
    # dictionary used to store values in Step 2
    a_0 = {'a_1':0}
    # initial start time
    t = 0


    # define conditions for when algorithim is run
    while X > 0:
        # Step 1: parameter calculation
        # update value of h
        # h: the number of distinct reactant combinations availible in the state
        h = X
        # calculate each a_mu and take thier sum
        # a_mu:average probability reaction mu will occur given the curent state
        #      of the system
        a_0['a_1'] = h * c
        a_sum = sum(a_0.values())
        # Step 2: Monte-Carlo simulation
        # generate r_1 and r_2
        r_1 = random.uniform(0,1)
        r_2 = random.uniform(0,1)
        # calculate the continuous RV tau
        # tau: time till reaction mu that leads to the next system state
        tau = (1/a_sum)*math.log(1/r_1)
        # calculate the discrete RV mu
        # mu: the index number that identifies the reaction that occurs
        mu = calcMu(a_0,r_2,a_sum)
        # Step 3: System update and data record
        # update the system time and add to the list
        t = t + tau
        time.append(t)
        # update the population levels in the system
        X = X - 1
        pop.append(X)

    #test code here
    print('c_mu =',c_mu)
    print('M =',M)


    
print('loaded...')
