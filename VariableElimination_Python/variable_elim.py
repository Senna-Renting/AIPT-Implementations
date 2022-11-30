"""
@Author: Joris van Vugt, Moira Berens, Leonieke van den Bulk

Class for the implementation of the variable elimination algorithm.

"""
import pandas as pd
import numpy as np

class VariableElimination():

    def __init__(self, network):
        """
        Initialize the variable elimination algorithm with the specified network.
        Add more initializations if necessary.

        """
        self.network = network

    def run(self, query, observed, elim_order):
        """
        Use the variable elimination algorithm to find out the probability
        distribution of the query variable given the observed variables

        Input:
            query:      The query variable
            observed:   A dictionary of the observed variables {variable: value}
            elim_order: Either a list specifying the elimination ordering
                        or a function that will determine an elimination ordering
                        given the network during the run

        Output: A variable holding the probability distribution
                for the query variable

        """
        # store probs as factors
        factors = [prob.copy(deep=True) for key,prob in self.network.probabilities.items()]

        # ..................................
        # The variable elimination algorithm
        # ..................................

        # marginalizing and reducing the factors using the elimination order (elim_order)
        for elim_node in elim_order:
            if elim_node in observed.keys():
                # reduce to the values that were observed
                f_have_node, indices = self.have_node(factors, elim_node)
                for i,factor in enumerate(f_have_node):
                    f_have_node[i] = self.reduce_factor(observed[elim_node], elim_node, factor)
                # remove updated factors in factors list
                for i in reversed(indices):
                    factors.pop(i)
                # add new factors to factors list
                factors.extend(f_have_node.copy())
            else:
                # marginalize the respective factors
                f_have_node, indices = self.have_node(factors, elim_node)
                for i,factor in enumerate(f_have_node):
                    f_have_node[i] = self.margin_factor(elim_node, factor)
                # remove updated factors in factors list
                for i in reversed(indices):
                    factors.pop(i)
                # add new factors to factors list
                factors.extend(f_have_node.copy())
        # computing the product of the factors
        product = 1
        for factor in factors:
            product *= factor["prob"][0]

        print(f"Final result: {product}")
        print(type(product))

    # returns the factors and their respective indices which have the elimination node in their factor
    def have_node(self, factors, elim_node):
        f_have_node = list()
        indices = list()

        for i,factor in enumerate(factors):
            if elim_node in factor.columns:
                indices.append(i)
                f_have_node.append(factor)
        return f_have_node, indices

    # reduce the factor by only selecting the given evidence (fixed_state)
    def reduce_factor(self, fixed_state, node, factor):
        return factor[factor[node] == fixed_state]
    # marginalize out the values of a random variable (elimination node) and return the resulting factor
    def margin_factor(self, node, factor):
        #initialize columns of marginalized factor
        columns = list()
        for column in factor.columns:
            if column != node:
                columns.append(column)
        #create empty marginalized factor and make manipulable copy of the factor
        factor_copy = factor.copy()
        marg_factor = pd.DataFrame(list(), columns=columns)
        marg_factors = list()
        #function to recurse over the possible marginal combinations
        def recurse_combs(factor, marg_factor, index, combination):
            columns = list(marg_factor.columns)
            columns.pop()
            if(index == len(columns)):
                # create a single row dataframe with the result of the marginalized combination
                selection = list()
                for i, column in enumerate(columns):
                    factor = factor[(factor[column] == combination[i])]
                marg_row = combination.copy()
                marg_row.append(factor["prob"].sum())
                columns.append("prob")
                marg_row = {columns[i]:[marg_el] for i,marg_el in enumerate(marg_row)}
                columns.pop()
                marg_row = pd.DataFrame(marg_row)
                factor.drop(node, axis=1, inplace=True)
                marg_factor = pd.concat([marg_factor,marg_row])
                marg_factors.append(marg_row)
            else:
                # check for all possible combinations of the marginalized attributes
                for value in factor[columns[index]].unique():
                    combination.append(value)
                    recurse_combs(factor.copy(), marg_factor, index+1, combination.copy())
                    combination.pop()
        #add the data to the marginalized factor
        recurse_combs(factor.copy(), marg_factor, 0, list())
        return pd.concat(marg_factors)

    def mult_factor(self, factor1, factor2):
        pass
