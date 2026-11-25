# implement cross validation

import copy
import numpy as np
from knn import KNearestNeighbor

num_folds = 5
k_choices = [1, 3, 5, 8, 10, 12, 15, 20, 50, 100]

X_train_folds = []
y_train_folds = []
################################################################################
# TODO:                                                                        #
# Split up the training data into folds. After splitting, X_train_folds and    #
# y_train_folds should each be lists of length num_folds, where                #
# y_train_folds[i] is the label vector for the points in X_train_folds[i].     #
# Hint: Look up the numpy array_split function.                                #
################################################################################

X_train_folds = np.array_split(X_train, num_folds)

y_train_folds = np.array_split(y_train, num_folds)

# A dictionary holding the accuracies for different values of k that we find
# when running cross-validation. After running cross-validation,
# k_to_accuracies[k] should be a list of length num_folds giving the different
# accuracy values that we found when using that value of k.
k_to_accuracies = {}


################################################################################
# TODO:                                                                        #
# Perform k-fold cross validation to find the best value of k. For each        #
# possible value of k, run the k-nearest-neighbor algorithm num_folds times,   #
# where in each case you use all but one of the folds as training data and the #
# last fold as a validation set. Store the accuracies for all fold and all     #
# values of k in the k_to_accuracies dictionary.                               #
################################################################################
classifier = KNearestNeighbor()

for k in k_choices:
  k_to_accuracies[k] = []
  for i in range(num_folds):
    # use pop() or copy() to remove an item an index
    train_img = X_train_folds.copy()
    validate_img = np.array(train_img.pop(i))
    col = validate_img.shape[1]
    # join all images together
    train_img = np.reshape(np.array(train_img), (-1, col))

    train_label = y_train_folds.copy()
    validate_label = np.array(train_label.pop(i))
    # join all labels together
    train_label = np.reshape(np.array(train_label), (-1))

    # remember all the data
    classifier.train(train_img, train_label)

    # use any loop to calculate distance (i use no loop for its speed)
    # return y_pred
    label_predict = classifier.predict(validate_img, k=k)
    score = np.sum(label_predict == validate_label)

    k_to_accuracies[k].append(score)

# Print out the computed accuracies
for k in sorted(k_to_accuracies):
    for accuracy in k_to_accuracies[k]:
        print('k = %d, accuracy = %f' % (k, accuracy))