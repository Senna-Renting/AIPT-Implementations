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
        # ............................................................................
        # Everything in this function is the contribution of: Senna Renting (s1067489)
        # ............................................................................
        factors = [prob.copy(deep=True) for key,prob in self.network.probabilities.items()]

        # ..................................
        # The variable elimination algorithm
        # ..................................

        # marginalizing and reducing the factors using the elimination order (elim_order)
        print(f"elim_order: {elim_order}")
        for elim_node in elim_order:
            if elim_node in observed.keys():
                # multiply factors containing elim_node to form a single factor
                f_have_node, indices = self.have_node(factors, elim_node)
                if len(f_have_node) >= 2:
                    f_have_node = [self.mult_factors(f_have_node, elim_node=elim_node)]
                # reduce the factor to the values that were observed
                f_have_node[0] = self.reduce_factor(observed[elim_node], elim_node, f_have_node[0])
                # remove updated factors in factors list
                for i in reversed(indices):
                    factors.pop(i)
                # add new factor to factors list
                factors.append(f_have_node[0].copy())
            elif elim_node != query:
                # multiply factors containing elim_node to form a single factor
                f_have_node, indices = self.have_node(factors, elim_node)
                if len(f_have_node) >= 2:
                    f_have_node = [self.mult_factors(f_have_node, elim_node=elim_node)]
                # marginalize the respective factor
                f_have_node[0] = self.margin_factor(elim_node, f_have_node[0])
                # remove updated factors in factors list
                for i in reversed(indices):
                    factors.pop(i)
                # add new factor to factors list
                factors.append(f_have_node[0].copy())
        # Compute the product of the resulting factors
        states = factors[0][query].unique()
        results = [1]*len(states)
        for factor in factors:
            for i,state in enumerate(states):
                results[i] *= factor[factor[query] == state]["prob"].values[0]
        dict_data = dict()
        dict_data[query] = states
        dict_data["prob"] = results
        result = pd.DataFrame(data=dict_data)
        print(f"Final result: {result}")
        return result

    # returns the factors and their respective indices which have the elimination node (elim_node) in their factor
    """
    @Author: Senna Renting (s1067489)

    Select the factors that contain a specific random variable

    Input:
        elim_node (str): node name on which we want to match factors
        factors (list): factors (pandas DataFrame's) to search through

    Output:
        (list, list): Two lists, first one contains the resulting factors,
                      the second their respective indices from the input (factors parameter).
    """
    def have_node(self, factors, elim_node):
        f_have_node = list()
        indices = list()

        for i,factor in enumerate(factors):
            if elim_node in factor.columns:
                indices.append(i)
                f_have_node.append(factor)
        return f_have_node, indices

    # function that multiplies multiple factors together on a selected variable
    """
    @Author: Senna Renting (s1067489)

    Function for multiplying two or more factors together

    Input:
        elim_node (str): random variable on which we want to multiply the factors
        factors (list): List of factors (pandas DataFrames)

    Output:
        (pd.Dataframe): Result of multiplying multiple factors
    """
    def mult_factors(self, factors, elim_node=None):
        if elim_node != None:
            output = factors[0]
            for i in range(1,len(factors)):
                output = pd.merge(output, factors[i], on=elim_node)
                prob_cols = [column for column in output.columns if "prob" in column]
                prob = output[prob_cols[0]]*output[prob_cols[1]]
                output.drop(prob_cols, axis=1, inplace=True)
                output["prob"] = prob
            return output

    # reduce the factor by only selecting the given evidence (fixed_state)
    """
    @Author: Senna Renting (s1067489)

    Function to reduce a factor by the given evidence

    Input:
        fixed_state (str): evidence state to reduce on
        node (str): random variable of which we have evidence
        factor (pd.DataFrame): any factor that allows for reduction

    Output:
        (pd.Dataframe): A reduced factor
    """
    def reduce_factor(self, fixed_state, node, factor):
        return factor[factor[node] == fixed_state]

    # marginalize out the values of a random variable (elimination node) and return the resulting factor
    """
    @Author: Senna Renting (s1067489)

    Marginalize out the values/states of a random variable

    Input:
        node (str): random variable we want to marginalize
        factor (pd.DataFrame): any factor that allows for marginalization

    Output:
        (pd.Dataframe): A marginalized factor
    """
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
        """
        Function that recursively applies the marginalize operation on each combination of the random variables

        Input:
            factor (pd.DataFrame): given factor to marginalize
            marg_factor (pd.DataFrame): output factor after marginalization is applied
            index (int): current considered column of the factor to marginalize on
            combination (list): list for remembering the considered combination so far
        Output:
            I do not have an output for this function
            (actually the 'marg_factor' input parameter serves as an output as well)

        """
        def recurse_combs(factor, marg_factor, index, combination):
            columns = list(marg_factor.columns)
            # remove the 'prob' column from the columns variable
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
