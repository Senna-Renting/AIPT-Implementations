"""
Institute: Radboud University
Course: SEM1V (AI: Principles & Techniques)
Student: Senna Renting (s1067489)
Task: 3
Date: 20 December 2022

@Author: Joris van Vugt, Moira Berens, Leonieke van den Bulk

Entry point for the creation of the variable elimination algorithm in Python 3.
Code to read in Bayesian Networks has been provided. We assume you have installed the pandas package.

"""
from read_bayesnet import BayesNet
from variable_elim import VariableElimination

if __name__ == '__main__':
    # The class BayesNet represents a Bayesian network from a .bif file in several variables

    # Example 1 (uncomment code below if you want to check the result for this example)
    #net = BayesNet('survey.bif') # Format and other networks can be found on http://www.bnlearn.com/bnrepository/
    #query = 'T'
    #evidence = {'O':'self'}

    # Example 2 (uncomment code below if you want to check the result for this example)
    net = BayesNet('earthquake.bif')
    query = 'Alarm'
    evidence = {'Burglary': 'True'}

    # These are the variables read from the network that should be used for variable elimination
    #print("Nodes:")
    #print(net.nodes)
    #print("Values:")
    #print(net.values)
    #print("Parents:")
    #print(net.parents)
    #print("Probabilities:")
    #print(net.probabilities)
    #print("\n\n\n\n")

    # Make your variable elimination code in the seperate file: 'variable_elim'.
    ve = VariableElimination(net)


    # Determine your elimination ordering before you call the run function. The elimination ordering
    # is either specified by a list or a heuristic function that determines the elimination ordering
    # given the network. Experimentation with different heuristics will earn bonus points. The elimination
    # ordering can for example be set as follows:
    elim_order = net.nodes

    # Call the variable elimination function for the queried node given the evidence and the elimination ordering as follows:
    ve.run(query, evidence, elim_order)
