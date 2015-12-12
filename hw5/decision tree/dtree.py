#!/usr/bin/env python

import numpy as np
from tree import DecisionTree

fmap = {
        'a': 0, 'b': 1, # A1
        'u': 0, 'y': 1, 'l': 2, 't': 3, # A4
        'g': 0, 'p': 1, 'gg': 2, # A5
        'c': 0, 'd': 1, 'cc': 2, # A6
        'i': 3, 'j': 4, 'k': 5, # A6
        'm': 6, 'r': 7, 'q': 8, # A6
        'w': 9, 'x': 10, 'e': 11, # A6
        'aa': 12, 'ff': 13, # A6
        'v': 0, 'h': 1, 'bb': 2, # A7
        'j': 3, 'n': 4, 'z': 5, # A7
        'dd': 6, 'ff': 7, 'o': 8, # A7
        't': 0, 'f': 1, # A9, A10, A12
        'g': 0, 'p': 1, 's': 2, # A13
        '-': 0, '+': 1 # class
       }

def map_feature(fvalue):
    if fvalue in fmap:
        return fmap[fvalue] # categorical
    if fvalue == '?':
        return -1 # missing value
    return float(fvalue) # continuous

"""
    A1: 0, 1 categorical
    A2: continuous
    A3: continuous
    A4: 0, 1, 2, 3 categorical
    A5: 0, 1, 2 categorical
    A6: 0 - 13 categorical
    A7: 0 - 8 categorical
    A8: continuous
    A9: 0, 1 categorical
    A10: 0, 1 categorical
    A11: continuous
    A12: 0, 1 categorical
    A13: 0, 1, 2 categorical
    A14: continuous
    A15: continuous
    C: 0, 1 class
"""
def read_data(filename):
    D = []
    # dtype='S4, f8, f8, S4, S4, S4, S4, f8, S4, S4, f8, S4, S4, f8, f8, S4')
    i = 0
    with open(filename, 'r') as f:
        for line in f:
            data = [map_feature(x) for x in line.strip().split(',')]
            D.append(data)
            i += 1
    #dt = np.dtype('i4, f8, f8, i4, i4, i4, i4, f8, i4, i4, f8, i4, i4, f8, f8, i4')
    #D = np.array([tuple(d) for d in D], dtype=dt) 
    D = np.array(D)
    return D[:,:-1], D[:,-1]

def kfold(n_samples, n_folds):
    fsize = n_samples / n_folds
    frem = n_samples % n_folds # elements not in any fold
    
    # distribute the remaining elements across folds
    fsizes = [fsize] * n_folds
    for i in xrange(frem):
        fsizes[i] += 1
    assert sum(fsizes) == n_samples

    # generate fold indices
    indexes = range(n_samples)
    current_idx = 0
    for size in fsizes:
        test_idx = range(current_idx, current_idx + size)
        train_idx = [i for i in indexes if i not in test_idx]
        yield train_idx, test_idx
        current_idx = current_idx + size

def main():
    X, y = read_data('crx.data.txt')
    n_samples = X.shape[0]
    n_folds = 3
    n_samples_per_fold = n_samples / n_folds

    cum_accuracy =  0.0
    cum_p = 0.0
    cum_r = 0.0
    fold = 0

    """
    clf = DecisionTree(maxdepth=3)
    clf.fit(X, y)
    clf.print_tree()
    y_pred = clf.predict(X)
    print y.astype(np.int32)
    return
    """

    for train_idx, test_idx in kfold(n_samples, n_folds):
        print "Fold", fold
        fold += 1

        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]
  
        clf = DecisionTree(maxdepth=3)
        clf.fit(X_train, y_train)
        #clf.print_tree()

        y_pred = clf.predict(X_test)

        # TP, FP, TN and FN
        tp = sum([1 for i in xrange(len(y_pred))
                  if y_pred[i] == 1 and y_test[i] == 1])
        tn = sum([1 for i in xrange(len(y_pred))
                  if y_pred[i] == 0 and y_test[i] == 0])
        fp = sum([1 for i in xrange(len(y_pred))
                  if y_pred[i] == 1 and y_test[i] == 0])
        fn = sum([1 for i in xrange(len(y_pred))
                  if y_pred[i] == 0 and y_test[i] == 1])

        # accuracy for this fold
        acc = float(tp + tn)/(tp + tn + fp + fn)
        cum_accuracy += acc
        print "\tAccuracy:", acc

        # precision, recall
        try:
            p = float(tp) / (tp + fp)
            r = float(tp) / (tp + fn)
            cum_p += p
            cum_r += r
            f1 = 2 * p * r / (p + r) 
            print "\tPrecision:", p 
            print "\tRecall:", r
            print "\tF1:", f1
        except:
            # divide by zero
            pass

    print
    print "Average accuracy:", cum_accuracy/n_folds
    print "Average precision:", cum_p/n_folds
    print "Average recall:", cum_r/n_folds

    """
    clf = DecisionTreeClassifier().fit(X, y)
    dot_data = StringIO() 
    tree.export_graphviz(clf, out_file=dot_data) 
    graph = pydot.graph_from_dot_data(dot_data.getvalue())
    graph.write_pdf("dtree.pdf") 
    """

if __name__ == "__main__":
    main()
