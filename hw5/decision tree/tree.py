#!/usr/bin/env python

import numpy as np
from constants import CONTINUOUS

def compute_entropy(x):
    frequencies = np.bincount(x.astype('i4')).astype('f8')
    probabilities = frequencies / np.sum(frequencies) 
    probabilities = [p for p in probabilities if p > 0] # remove 0's
    log_probabilities = np.log2(probabilities)
    return -1 * np.sum(probabilities * log_probabilities)

class Node:
    def __init__(self, data=None, labels=None, features=None, parent=None,
                 value=None, depthleft=10000):
        # initialise instance variables
        self._data = data
        self._labels = labels
        self._features = features
        self._parent = parent
        self._children = []
        self._split = (None, None) # dimension, location (if continuous)
        self._leaf = False
        self._pred = -1
        self._value = value

        # check if this is a leaf
        unique_labels = np.unique(self._labels)
        if len(unique_labels) == 1 or depthleft == 0:
            self._leaf = True,
            frequencies = np.bincount(self._labels.astype('i4'), minlength=2).astype('f8')
            assert sum(frequencies) > 0
            probabilities = frequencies / np.sum(frequencies) 
            self._pred = probabilities 
            return

        dimension, location = self._compute_split()
        if dimension in CONTINUOUS:
            self._split = (dimension, location)
        else:
            self._split = (dimension, None)

        #print 'In node'
        #print '\tfeatures:', self._features
        #print '\tsplit:', self._split
        #print '\tnsamples:', self._data.shape
        idxs, values = self._split_data()
        new_features = self._features
        if dimension not in CONTINUOUS:
            new_features = [f for f in self._features if f != dimension]
        for idx, v in zip(idxs, values):
            self._children.append(Node(data=self._data[idx],
                                       labels=self._labels[idx],
                                       features=new_features,
                                       parent=self, value=v,
                                       depthleft=depthleft-1))

    def _compute_split(self):
        dimension = None
        location = None
        min_entropy = 1.0

        for f in self._features:
            values = self._data[:,f] # has missing values = -1
            idx = values != -1 # indices of non-missing values
            values = values[idx] # no missing values
            labels = self._labels[idx]
            unique_values = np.unique(values)

            if f in CONTINUOUS: # continuous feature
                for v in unique_values:
                    # compute conditional entropy of splitting on <= v, > v
                    idx = values <= v
                    conditional_entropy = len(values[idx])/float(len(values)) * \
                                          compute_entropy(labels[idx]) + \
                                          len(values[~idx])/float(len(values)) * \
                                          compute_entropy(labels[~idx])
                    if conditional_entropy < min_entropy:
                        min_entropy = conditional_entropy
                        dimension = f
                        location = v

            else: # categorical feature
                # compute the proportion of each feature value (weights)
                frequencies = np.bincount(values.astype('i4')).astype('f8')
                weights = [freq for freq in frequencies / np.sum(frequencies) if freq > 0]
                
                # then compute the label-entropy for each feature value
                entropies = np.array([compute_entropy(labels[values==v])
                                      for v in unique_values])

                # conditional entropy of categorical feature f
                conditional_entropy = np.sum(weights * entropies)

                if conditional_entropy < min_entropy:
                    min_entropy = conditional_entropy
                    dimension = f
 
        return (dimension, location)

    def _split_data(self):
        dimension, location = self._split
        values = self._data[:,dimension]
        if dimension in CONTINUOUS:
            return [values <= location, values > location],\
                   ['<='+str(location), '>'+str(location)]
        else:
            unique_values = [int(i) for i in np.unique(values)
                             if i != -1]
            return [values == v for v in unique_values],\
                    unique_values

    def predict(self, X):
        if self._leaf:
            #print 'Leaf, prediction:', self._pred
            return np.argmax(self._pred) 

        dimension, location = self._split
        #print 'Checking split:', dimension, location, X[dimension]
        
        if int(X[dimension]) == -1: # missing value
           most_likely_child = np.argmax([c._data.shape[0]
                                          for c in self._children])
           #print 'Moving to most likely node:'
           #print [c._data.shape[0] for c in self._children]
           #print self._children[most_likely_child]._value
           return self._children[most_likely_child].predict(X)
        
        if dimension in CONTINUOUS:
            if X[dimension] <= location:
                #print 'Moving to node:', self._children[0]._value
                return self._children[0].predict(X)
            else:
                #print 'Moving to node:', self._children[1]._value
                return self._children[1].predict(X)
        else:
            for child in self._children:
                if child._value == int(X[dimension]):
                    #print 'Moving to node:', child._value
                    return child.predict(X)
            
            most_likely_child = np.argmax([c._data.shape[0]
                                           for c in self._children])
            return self._children[most_likely_child].predict(X)

class DecisionTree:
    def __init__(self, maxdepth=10000):
        self._root = None
        self._maxdepth = maxdepth

    def fit(self, X, y):
        self._root = Node(data=X, labels=y,
                          features=range(X.shape[1]), parent=None,
                          depthleft=self._maxdepth) 

    def predict(self, X):
        preds = []
        for x in X:
            #print 'Predicting:'
            #print x
            preds.append(self._root.predict(x))
        return [int(p) for p in preds]

    def print_tree(self):
        self._print_tree(self._root)

    def _print_tree(self, node, tabs=''):
        if node is None:
            return

        #print tabs + 'DATA:'
        #print tabs + str(node._data).replace('\n', '\n' + tabs)
        #print tabs + 'LABELS:'
        #print tabs + str(node._labels).replace('\n', '\n' + tabs)
        print tabs + str(len(node._labels)) + ' samples'
        print tabs + 'VALUE:', node._value

        if node._leaf:
            print tabs + 'LEAF: PRED =', node._pred
        else:
            dimension, location = node._split
            print tabs, 'SPLIT', node._split

            for child in node._children:
                print tabs + 'CHILD:'
                self._print_tree(child, tabs + '\t')
