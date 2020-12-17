# encoding: utf-8

from fptree import FPNode, FPTree
from utility_methods import UtilityMethods
import time


class DDPMine:
    """
    Main class implementing the DDPMine algorithm.
    """
    # TODO: Insert sll the best patterns into a dta set or a file with their Max Gain
    def __init__(self, debug=False):
        self.fp_tree = FPTree.FPTree()
        self._maxGain_ = 0.0
        self._bestPattern = None
        self._bestPatterns = []
        self.debug = debug



    def mine(self, transactionDatabase, support):
        self._globalTransactionDatabase = transactionDatabase
        self.fp_tree = self.buildTree(transactionDatabase)
        self._globalFPTree = self.fp_tree

        return self._mine(self.fp_tree, support)


    def _mine(self, P, s):
        """
        Does the heavy lifting of mining for the nodes – returns the list of most
        discriminative patterns.
        """
        # while the tree is not empty

        while not P.empty:
            size = self._globalTransactionDatabase.size()

            start = time.perf_counter()

            # branch and bound to find best pattern
            self.branchAndBound(P, s, [])

            elapsed = time.perf_counter() - start

            print(("Transactions: %d – found best pattern '%s' in %f seconds" % (
                size, "".join([] if not self._bestPattern else self._bestPattern), elapsed)))



            if self.debug:
                print("best pattern:")
                print((self._bestPattern))
                print("Max Gain:")
                print((self._maxGain_))

            # if no best pattern then break
            if self._bestPattern == None:
                break

            # get transaction list and update tree
            transactionList = self._globalTransactionDatabase.transactionListFromPattern(self._bestPattern)

            self._globalTransactionDatabase.removeTransactions(transactionList)

            P = self.buildTree(self._globalTransactionDatabase)

            # append the new best found pattern
            self._bestPatterns.append([self._bestPattern, self._maxGain_])

            # reset the best pattern
            self._bestPattern = None
            self._maxGain_ = 0

        # return the list of best patterns
        return self._bestPatterns

    def buildTree(self, transactionDatabase):

        master = FPTree.FPTree()
        for transaction in transactionDatabase:
            # print transaction
            master.add(transaction)

        return master

    def branchAndBound(self, tree, minimum_support, suffix):

        for item, nodes in list(tree.items()):

            support = 0

            for n in nodes:
                count = n.count
                # print count
                support += count

            # make sure the support is sufficient
            # support = sum(n.count for n in nodes)

            if support >= minimum_support and item not in suffix:
                # we found a new possible canidate
                found_set = [item] + suffix

                # print("support")
                # print(support)
                # print("---")

                # since we are looking for the best pattern globally we need to compute the pattern's global information
                infoGain = UtilityMethods.InformationGain(support / self._globalTransactionDatabase.size(),
                                                          self._globalTransactionDatabase.labelSupport(),
                                                          self._globalTransactionDatabase.labelAndPatternSupport(
                                                              found_set))

                # if it is the best pattern then save it
                if infoGain > self._maxGain_:
                    self._maxGain_ = infoGain
                    self._bestPattern = found_set

                # construct the conditional database of new canidate from the global database
                conditionalDatabase = self._globalTransactionDatabase.buildConditionalDatabase(found_set)

                # compute the information gain upperbound of this new conditional database based on the size of the
                # conditional database and the global label support
                infoGainBound = UtilityMethods.InformationGainUpperBound(
                    conditionalDatabase.size() / self._globalTransactionDatabase.size(),
                    self._globalTransactionDatabase.labelSupport())
                # print("my max gain is:", self._maxGain_)
                # print("my info gain is:", infoGainBound)

                # if potential for high information gain patterns then recursivly mine them
                if self._maxGain_ >= infoGainBound:
                    pass
                else:
                    # Build a conditional tree and recursively mine
                    tpp = tree.prefix_paths(item)
                    conditionalTree = tree.conditional_tree_from_paths(tpp, minimum_support)
                    # print("my new cond FP tree is:", conditionalTree._root.children)
                    self.branchAndBound(conditionalTree, minimum_support, found_set)
