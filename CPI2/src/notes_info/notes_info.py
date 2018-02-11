#
#
# Created by Maxime Lundiquist, Mehdi Dalaa, Mandry Mbundu, David Rigaux
# EISTI, TIPE 2016 - 2017
#
# How to run : ./bin/spark-submit /Users/davidrigaux/Documents/GIT/Big_Data/CPI2/algorithmes/notes_info/notes_info.py
#
# What does it do : This program calculates the K-means of either random data sets, or from an input file
# Notes d'info : kmeans.kmeans_file("notes.in",2)

import csv
import numpy as np
import matplotlib.pyplot as plt
from pyspark import SparkContext
from pyspark.mllib.clustering import KMeans, KMeansModel
from pyspark.mllib.regression import LabeledPoint, LinearRegressionWithSGD, LinearRegressionModel
from numpy import array
from math import sqrt

############### PARAMETRES ######################
dir_path = "/Users/davidrigaux/Documents/GIT/Big_Data/CPI2/algorithmes/notes_info/"
file_name = "exemples_notes.csv"
k=4
#################################################

#Create SparkContext
sc = SparkContext()
file_in = np.genfromtxt(dir_path+file_name,dtype=float,delimiter=',')
#Delete the first row
file_in = np.delete(file_in,0,0)

#selects only the two last columns
data = file_in[:,[1,2]]


##########KMEANS#############
model = KMeans.train(sc.parallelize(data), k, maxIterations=100, initializationMode="random",seed=50, initializationSteps=5, epsilon=1e-4)

cluster_ind = model.predict(sc.parallelize(data))

cluster_centers = model.clusterCenters
cluster_indList = cluster_ind.collect()


cluster_sizes = cluster_ind.countByValue().items() #Nombre d'eleves dans chaque clusters

div = []
for i in range(0,k):
	div.append([])

for i in range(0,len(cluster_indList)) :
	div[cluster_indList[i]].append(i+1)

for i in range(0,k) :
	print('\nVoici les eleves faisant partie du cluster de centre {}'.format(cluster_centers[i]))
	print (div[i])

colors = ['r','b','y','g','c','m']

for i in range(0,len(div)) :
	for j in div[i]:
		plt.scatter(data[j-1][0],data[j-1][1],c=colors[i])
	plt.scatter(cluster_centers[i][0],cluster_centers[i][1],s=100,c='k')
plt.title('KMeans avec {} clusters'.format(len(div)))

######Regression Lineaire

# Calculate the mean value of a list of numbers
def mean(values):
	return sum(values) / float(len(values))

# Calculate covariance between x and y
def covariance(x, mean_x, y, mean_y):
	covar = 0.0
	for i in range(len(x)):
		covar += (x[i] - mean_x) * (y[i] - mean_y)
	return covar

# Calculate the variance of a list of numbers
def variance(values, mean):
	return sum([(x-mean)**2 for x in values])

# Calculate coefficients
def coefficients(dataset):
	x = [row[0] for row in dataset]
	y = [row[1] for row in dataset]
	x_mean, y_mean = mean(x), mean(y)
	b1 = covariance(x, x_mean, y, y_mean) / variance(x, x_mean)
	b0 = y_mean - b1 * x_mean
	return [b0, b1]


def graph(x_range):
	x = np.array(x_range)
	y = coefs[0]+  x*coefs[1]
	plt.plot(x, y)
# Test simple linear regression

fig = plt.figure()
for i in data :
	plt.scatter(i[0],i[1])
coefs = coefficients(data)
graph(range(0, 20))
plt.title('Regression Lineaire. Equation de la droite de regression : {0}*x + {1}'.format(coefs[1],coefs[0]))
plt.xlabel('Informatique Theorique')
plt.ylabel('Programmation')
plt.show()
