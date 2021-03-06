'''
Created on Jul 18, 2016

@author: rbhat
'''
from sklearn.datasets import load_boston
from sklearn.cross_validation import train_test_split
from sklearn.metrics.classification import accuracy_score
from sklearn.metrics.regression import r2_score, mean_squared_error
from sklearn.preprocessing import MinMaxScaler

from models import SupervisedDBNRegression


# Loading dataset
boston = load_boston()
X, Y = boston.data, boston.target

# Splitting data
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

# Data scaling
min_max_scaler = MinMaxScaler()
X_train = min_max_scaler.fit_transform(X_train)

# Training
regressor = SupervisedDBNRegression(hidden_layers_structure=[200],
                                    learning_rate_rbm=0.01,
                                    learning_rate=0.001,
                                    n_epochs_rbm=100,
                                    n_iter_backprop=500,
                                    l2_regularization=0.0,
                                    activation_function='relu')
regressor.fit(X_train, Y_train)

# Test
X_test = min_max_scaler.transform(X_test)
Y_pred = regressor.predict(X_test)
print 'Done.\nR-squared: %f\nMSE: %f' % (r2_score(Y_test, Y_pred), mean_squared_error(Y_test, Y_pred))
#print 'Done.\nAccuracy: %f' % accuracy_score(Y_test, Y_pred)

