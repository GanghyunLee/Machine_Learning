#!/usr/bin/python

""" 
    This is the code to accompany the Lesson 2 (SVM) mini-project.

    Use a SVM to identify emails from the Enron corpus by their authors:    
    Sara has label 0
    Chris has label 1
"""
    
import sys
from time import time
sys.path.append("../tools/")
from email_preprocess import preprocess

### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
features_train, features_test, labels_train, labels_test = preprocess()

#########################################################
### your code goes here ###

from sklearn.svm import SVC

#============================================================
# Slow solution
#============================================================
# clf = SVC(kernel='linear')
# clf.fit(features_train, labels_train) # fit the model(Train)
# accuracy = clf.score(features_test, labels_test)

# print(accuracy)

#===================================================================
# To speed up an algorithm, train it on a smaller training data set
#===================================================================
# features_train = features_train[:int(len(features_train)/100)]
# labels_train = labels_train[:int(len(labels_train)/100)]

# clf = SVC(kernel='linear')
# clf.fit(features_train, labels_train) # fit the model(Train)
# accuracy = clf.score(features_test, labels_test)

# print(accuracy)
#########################################################
features_train = features_train[:int(len(features_train)/100)]
labels_train = labels_train[:int(len(labels_train)/100)]

clf = SVC(kernel = "rbf")
clf.fit(features_train, labels_train)

accuracy = clf.score(features_test, labels_test)

print(accuracy)

