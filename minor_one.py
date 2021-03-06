import os, pandas as pd, numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, r2_score, mean_squared_error
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.svm import SVC
from sklearn.utils import shuffle
from math import sqrt
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC
from sklearn.impute import SimpleImputer
from sklearn.ensemble import VotingClassifier
from keras.models import Sequential
from keras.layers import Dense


class MultipleLinearRegression:
	def __init__(self, dataset):		
		self.dataset = pd.read_csv(dataset)

	def model(self):

		self.train, self.test = train_test_split(self.dataset, test_size = 0.2)
		self.X_train, self.X_test = self.train.loc[:, ['TV', 'RADIO', 'NEWSPAPER']], self.test.loc[:, ['TV', 'RADIO', 'NEWSPAPER']]
		self.Y_train, self.Y_test = self.train.loc[:, ['SALES']], self.test.loc[:, ['SALES']]

		self.regression = LinearRegression()
		self.regression.fit(self.X_train, self.Y_train)

		self.y_prediction = np.round(self.regression.predict(self.X_test))
		self.Y_tester = np.round(self.Y_test.values.reshape(-1, 1))
		
		self.confusion_matrix = confusion_matrix(self.Y_tester, self.y_prediction)
		self.score_r2 = r2_score(self.y_prediction, self.Y_tester)
		self.rmse = np.sqrt(mean_squared_error(self.Y_tester,self.y_prediction))

		print ('\n')
		print ('\t\tPOLYNOMIAL REGRESSION')
		print ('R Squared: ', round(self.score_r2, 3))
		print ('RMSE: ', self.rmse)

class KNearestNeightbours:
	def __init__(self, dataset):
		self.dataset = pd.read_csv(dataset, names = ['age', 'distance_year', 'positive_nodes', 'survival_status'])

	def model(self):
		self.dataset['survival_status'] = self.dataset['survival_status'].map({1: 'Survived', 2: 'Died'})
		self.dataset = shuffle(self.dataset)

		self.X = self.dataset.iloc[:, :-1].values
		self.Y = self.dataset.iloc[:, -1].values

		self.scaler = MinMaxScaler(feature_range = (0, 1))
		self.rescaled_X = self.scaler.fit_transform(self.X)

		self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(self.rescaled_X, self.Y, test_size = 0.20)
		
		self.classifier = KNeighborsClassifier(n_neighbors = round(sqrt(len(self.X_train))))
		self.classifier.fit(self.X_train, self.Y_train)
		self.y_prediction = self.classifier.predict(self.X_test)

		self.confusion_matrix = confusion_matrix(self.Y_test, self.y_prediction)
		self.classification_report = classification_report(self.Y_test, self.y_prediction)
		self.accuracy = accuracy_score(self.Y_test, self.y_prediction)

		print ('\n')
		print ('\t\tK-NEAREST NEIGHBOURS')
		print ('Confusion Matrix:')
		print (self.confusion_matrix)
		print ('\n')
		print ('Classification report:')
		print (self.classification_report)
		print ('Accuracy: ', round(self.accuracy, 3))

class SVMModel:
	def __init__(self, dataset):
		self.dataset = pd.read_csv(dataset, names = ['variance', 'skewness', 'curtosis', 'entropy', 'class'])

	def model(self):
		self.X = self.dataset.iloc[:, :-1].values
		self.Y = self.dataset.iloc[:, -1].values

		self.scaler = MinMaxScaler(feature_range = (0, 1))
		self.rescaled_X = self.scaler.fit_transform(self.X)
		self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(self.rescaled_X, self.Y, test_size = 0.20)
		
		self.classifier = SVC(kernel = 'linear')
		self.classifier.fit(self.X_train, self.Y_train)

		self.y_prediction = self.classifier.predict(self.X_test)
		self.confusion_matrix = confusion_matrix(self.Y_test, self.y_prediction)
		self.classification_report = classification_report(self.Y_test, self.y_prediction)
		self.accuracy = accuracy_score(self.Y_test, self.y_prediction)

		print ('\n')
		print ('\t\tSUPPORT VECTROR MACHINE CLASSIFICATION')
		print ('Confusion Matrix:')
		print (self.confusion_matrix)
		print ('\n')
		print ('Classification report:')
		print (self.classification_report)
		print ('Accuracy: ', round(self.accuracy, 3))

class EnsambleModel:

	def __init__(self, dataset):
		self.dataset = pd.read_csv(dataset, names = ['Sample code number', 'Clump Thickness', 'Uniformity of Cell Size', 'Uniformity of Cell Shape', 'Marginal Adhesion', 'Single Epithelial Cell Size', 'Bare Nuclei', 'Bland Chromatin', 'Normal Nucleoli', 'Mitoses', 'Class'])
		self.dataset.drop(['Sample code number'], axis = 1, inplace = True)
		self.dataset.replace('?', 0, inplace = True)
	
	def model(self):
		self.data = self.dataset.values

		self.imputer = SimpleImputer()
		self.imputer_data = self.imputer.fit_transform(self.data)
		self.scaler = MinMaxScaler(feature_range = (0, 1))
		self.regularized_data = self.scaler.fit_transform(self.imputer_data)

		self.X = self.dataset.iloc[:, :-1].values
		self.Y = self.dataset.iloc[:, -1].values

		self.kFold = KFold(n_splits = 10, random_state = 6)
		self.ensamble_model = VotingClassifier(estimators = [('logistic', LogisticRegression(solver = 'lbfgs')), ('svm', SVC(gamma = 'scale'))])
		self.prediction = cross_val_score(self.ensamble_model, self.X, self.Y, cv = self.kFold)

		print ('\n')
		print ('\t\tENSEMBLE')
		print ('Accuracy: ', round(self.prediction.mean(), 3))

class NeuralNetworkModel:
	def __init__(self, dataset):
		self.dataset = pd.read_csv(dataset, names = ['Number of times pregnant', 'Plasma glucose concentration', 'Diastolic blood pressure', 'Triceps skin fold thickness', '2-Hour serum insulin', 'Body mass index', 'Diabetes pedigree function', 'Age', 'Class variable'])

	def model(self):
		self.data = self.dataset.values
		self.X = self.dataset.iloc[:, :-1].values
		self.Y = self.dataset.iloc[:, -1].values

		self.keras_model = Sequential()
		self.keras_model.add(Dense(12, input_dim = 8, activation = 'relu'))
		self.keras_model.add(Dense(10, activation = 'relu'))
		self.keras_model.add(Dense(1, activation = 'sigmoid'))
		self.keras_model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
		self.keras_model.fit(self.X, self.Y, epochs = 100, batch_size = 5, verbose = 0)

		self.val, self.accuracy = self.keras_model.evaluate(self.X, self.Y)

		print ('\n')
		print ('\tNEURAL NETWORK')
		print ('Accuracy: ', round((self.accuracy * 100), 2))

MultipleLinearRegression(dataset = 'datasets/advertising.csv').model()
KNearestNeightbours(dataset = 'datasets/haberman.csv').model()
SVMModel(dataset = 'datasets/data_banknote_authentication.csv').model()
EnsambleModel(dataset = 'datasets/breast-cancer-wisconsin.csv').model()
NeuralNetworkModel(dataset = 'datasets/diabetes.csv').model()