#
#
# Created by Maxime Lundiquist, Mehdi Dalaa, Mandry Mbundu, David Rigaux
# EISTI, TIPE 2016 - 2017
#
# How to run : ./bin/spark-submit /Users/davidrigaux/Documents/GIT/Big_Data/CPI2/algorithmes/wordcount/wordcount.py
#
#
# What does it do : This program performs a wordcout, which counts the number of occurences of words, and returning the top n words


from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("My App")
sc = SparkContext(conf = conf) #Create SparkContext

'''Function that counts the number of repition of one word.'''
def wordcountF (n_top,path): #path correspond au chemin du fichier a lire

	inputFileData = sc.textFile(path).cache() #open file
	###### Nettoyage du text
	formattedText = inputFileData.map(lambda x: x.replace("'",' ').replace('.',' ').replace(',',' ').lower()) #every ponctuation transformed + lowercased
	textSplitSpaces = formattedText.flatMap(lambda x: x.split(" ")) #Splits all words in a flattern RDD instead of being in several RDDs

	###### Commencement du comptage
	tupleCreation = textSplitSpaces.map(lambda x: (x,1)) #add the value of 1 in a (key,value) format with each word found
	keyValueAdd = tupleCreation.reduceByKey(lambda x,y: x+y) #add all values having the same key together
	filterKeyValue = keyValueAdd.filter(lambda (x,y) : x != '') #delete all keys being ''
	ordreKeyValue = filterKeyValue.map(lambda a: (a[1],a[0])).sortByKey(False)#exchaning key/value to sort from biggest to smallest
	return ordreKeyValue.top(n_top)#return only the n_top first elements of the RDD in list format

print (wordcountF(10,"/Users/davidrigaux/Documents/GIT/Big_Data/CPI2/algorithmes/wordcount/lipsum.txt"))
#calling the main function and printing the results
