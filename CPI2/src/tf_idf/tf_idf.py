#
#
# Created by Maxime Lundiquist, Mehdi Dalaa, Mandry Mbundu, David Rigaux
# EISTI, TIPE 2016 - 2017
#
# How to run : ./bin/spark-submit /Users/davidrigaux/Documents/GIT/Big_Data/CPI2/algorithmes/tf_idf/tf_idf.py
#
# What does it do : This program calculates the TF.IDF of a whole document set, or only the TF.IDF of a certain word


from pyspark import SparkConf, SparkContext
from pyspark.mllib.feature import HashingTF, IDF


#HashingTF : Maps a sequence of terms to their term frequencies using the hashing trick
# https://en.wikipedia.org/wiki/Feature_hashing

#IDF : Inverse document frequency (formule : log((m+1)/(d(t)+1))
# m : total number of documents and d(t) is the number of documents that contain term t.

###############################PARAMETRES#######################################

# Leave blank if want to calculate the TF.IDF of all words in the document set
mot = "fonction"
dir_path = "/Users/davidrigaux/Documents/GIT/Big_Data/CPI2/algorithmes/tf_idf"

################################################################################

conf = SparkConf().setMaster("local").setAppName("My App")

#Create SparkContext
sc = SparkContext(conf = conf)

#Load all documents in a certain directory
documents = sc.textFile(dir_path + "/*.txt").map(lambda line: line.split(" "))

hashing = HashingTF()

# Condition to know if the user wants to get the tf.idf of the whole document
# set or only one word
if mot != "" :
	index = hashing.indexOf(mot)
	mot_precis = True
else:
	mot_precis = False



#Term Frequency
#transform() : Transforms the input document (list of terms) to term frequency vectors, or transform the RDD of document to RDD of term frequency vectors.
tf = hashing.transform(documents)



#RDD Persistence
#Caching a dataset in memory across operations. Each nodes stores any partitions of it that it computes in memory and reuses them in other actions on that database. Used to make operation go up to 10x faster
tf.cache()

#Inverse Document Frequency
#fit used to compute the inverse document frequency of tf (term frequency vector)
idf = IDF().fit(tf)

tfidf = idf.transform(tf)

#Liste de SparseVector, resultat sans mot precis, TF.IDF de tous les mots
tf_idf_list = tfidf.collect()

# Work depending if we want the whole document set's tf.idf or only one word
if mot_precis :
	nb_docs = len(tf_idf_list)

	for i, spar_vec in enumerate(tf_idf_list) :
		tfidf_tmp = spar_vec[index]
		if tfidf_tmp != 0 :
			tfidf_precis = tfidf_tmp
			break
		if i == (nb_docs - 1) :
			tfidf_precis = 0
	print ("\n\nmot : %s \ntf.idf : %f" % (mot,tfidf_precis))
else:
	print('\n\n')
	print(tf_idf_list)
