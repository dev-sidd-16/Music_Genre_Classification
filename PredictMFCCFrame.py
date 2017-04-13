import math
import numpy as np
import sklearn
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="numpy")
from numpy.random import permutation, randint
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.multiclass import OneVsRestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn import svm
from sklearn import tree
from sklearn.neural_network import MLPClassifier
from statistics import mode
from sklearn.naive_bayes import GaussianNB
from scipy import stats

#data = np.loadtxt('mfcc_1000_500.npy',delimiter = ',',dtype = float)
data = np.loadtxt('mfcc.npy',delimiter=',',dtype=float)
labels = np.loadtxt('mfcc_labels.npy',delimiter=',',dtype=float)
labels.astype(int)
print np.shape(data)

# Randomly shuffle the index of nba.
randomize = np.arange(len(data))
np.random.shuffle(randomize)
data = data[randomize]
labels = labels[randomize]

# Set a cutoff for how many items we want in the test set (in this case 1/3 of the items)
test_cutoff = int(math.floor(len(data)/3))
# Generate the test set by taking the first 1/3 of the randomly shuffled indices.
test_data = data[0:test_cutoff]

test_label = labels[0:test_cutoff]
# Generate the train set with the rest of the data.
train_data = data[test_cutoff:]
train_label = labels[test_cutoff:]

#for sample in train_data:
train_data = np.reshape(train_data, (np.shape(train_data)[0]*1206,np.shape(train_data)[1]/1206))
test_data = np.reshape(test_data, (np.shape(test_data)[0]*1206,np.shape(test_data)[1]/1206))

train_label_updated = []
for label in train_label:
    for x in range(0,1206):
        train_label_updated.append(label)
train_label = train_label_updated

print np.shape(train_data)
print np.shape(train_label)

#KNN Classifier
neigh = KNeighborsClassifier(n_neighbors=5, algorithm='auto', metric='minkowski', p=1)
neigh.fit(train_data,train_label)
predictions_knn = neigh.predict(test_data)

#SVM Classifier
svc = svm.LinearSVC(random_state=0)
svc = OneVsRestClassifier(svc)
clf = CalibratedClassifierCV(svc, cv=10)
clf.fit(train_data,train_label)
predictions_svm = clf.predict(test_data)

#Decision Tree Classifier
clf = tree.DecisionTreeClassifier()
clf = clf.fit(train_data, train_label)
predictions_decision = clf.predict(test_data)

#Neural Network Classifier
clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(100,), random_state=1,activation='tanh')
clf.fit(train_data, train_label)
predictions_neural = clf.predict(test_data)

#Naive Bayes
clf = GaussianNB()
clf.fit(train_data,train_label)
predictions_naive = clf.predict(test_data)


predictions_ensemble = []
for x in range(0,test_cutoff):
    try:
        predictions_ensemble.append(mode([int(predictions_knn[x]),int(predictions_svm[x]),int(predictions_decision[x]),int(predictions_neural[x],int(predictions_naive[x]))]))
    except:
        val = randint(0,5)
        if val == 0:
            predictions_ensemble.append(int(predictions_knn[x]))
        if val == 1:
            predictions_ensemble.append(int(predictions_svm[x]))
        if val == 2:
            predictions_ensemble.append(int(predictions_decision[x]))
        if val == 3:
            predictions_ensemble.append(int(predictions_neural[x]))
        if val == 4:
            predictions_ensemble.append(int(predictions_naive[x]))
        pass



predictions_svm = np.reshape(predictions_svm,np.shape(predictions_svm)[0]/1206,np.shape(predictions_svm)[1]*1206)
predictions_decision = np.reshape(predictions_decision,np.shape(predictions_decision)[0]/1206,np.shape(predictions_decision)[1]*1206)
predictions_ensemble = np.reshape(predictions_ensemble,np.shape(predictions_ensemble)[0]/1206,np.shape(predictions_ensemble)[1]*1206)
predictions_knn = np.reshape(predictions_knn,np.shape(predictions_knn)[0]/1206,np.shape(predictions_knn)[1]*1206)
predictions_naive = np.reshape(predictions_naive,np.shape(predictions_naive)[0]/1206,np.shape(predictions_naive)[1]*1206)
predictions_neural = np.reshape(predictions_neural,np.shape(predictions_neural)[0]/1206,np.shape(predictions_neural)[1]*1206)

predictions_svm_new = []
predictions_decision_new = []
predictions_ensemble_new = []
predictions_knn_new = []
predictions_naive_new = []
predictions_neural_new = []
for x in range(0,1000):
    predictions_svm_new[x] = stats.mode(predictions_svm[x])[0][0]
    predictions_decision_new[x] = stats.mode(predictions_decision[x])[0][0]
    predictions_ensemble_new[x] = stats.mode(predictions_ensemble[x])[0][0]
    predictions_knn_new[x] = stats.mode(predictions_knn[x])[0][0]
    predictions_naive_new[x] = stats.mode(predictions_naive[x])[0][0]
    predictions_neural_new[x] = stats.mode(predictions_neural[x])[0][0]

predictions_svm = predictions_svm_new
predictions_decision = predictions_decision_new
predictions_ensemble = predictions_ensemble_new
predictions_knn = predictions_knn_new
predictions_naive = predictions_naive_new
predictions_neural = predictions_neural_new

# Create the knn model.
# Look at the five closest neighbors.
# knn = KNeighborsRegressor(n_neighbors=5)
# # Fit the model on the training data.
# knn.fit(train_data, train_label)
# # Make point predictions on the test set using the fit model.
# predictions = knn.predict(test_data)
# print type(predictions)
knn_count = 0
svm_count = 0
decision_count = 0
neural_count = 0
ensemble_count = 0
naive_count = 0

for x in range(0,test_cutoff):
    # print int(test_label[x]),int(predictions_knn[x])
    if int(test_label[x]) == int(predictions_knn[x]):
        knn_count += 1
    if int(test_label[x]) == int(predictions_svm[x]):
        svm_count += 1
    if int(test_label[x]) == int(predictions_decision[x]):
        decision_count += 1
    if int(test_label[x]) == int(predictions_neural[x]):
        neural_count += 1
    if int(test_label[x]) == int(predictions_ensemble[x]):
        ensemble_count += 1
    if int(test_label[x]) == int(predictions_naive[x]):
        naive_count += 1

mse = (((predictions_knn - test_label) ** 2).sum()) / len(predictions_knn)
print "MSE: "
print mse

acc_knn = knn_count/float(test_cutoff) * 100
acc_svm = svm_count/float(test_cutoff) * 100
acc_decision = decision_count/float(test_cutoff) * 100
acc_neural = neural_count/float(test_cutoff) * 100
acc_ensemble = ensemble_count/float(test_cutoff) * 100
acc_naive = naive_count/float(test_cutoff) * 100

print "KNN Accuracy: "
print acc_knn
print "SVM Accuracy: "
print acc_svm
print "Decision Accuracy: "
print acc_decision
print "Neural Accuracy: "
print acc_neural
print "NaiveBayes Accuracy: "
print acc_naive
print "Ensemble Accuracy: "
print acc_ensemble