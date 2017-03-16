'''./bin/spark-submit /Users/davidrigaux/Documents/GIT/Big_Data/CPI2/algorithmes/spark/spark-2.1.0-bin-hadoop2.7/wordcount.py'''
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("My App")
sc = SparkContext(conf = conf) #Create SparkContext

'''Function that counts the number of repition of one word.'''
def wordcountF (n_top,path,context): #path correspond au chemin du fichier à lire
	inputFileData = sc.textFile(path).cache() #open file
	formattedText = inputFileData.map(lambda x: x.replace("'",' ').replace('.',' ').replace(',',' ').lower()) #every ponctuation transformed + lowercased
	textSplitSpaces = formattedText.flatMap(lambda x: x.split(" ")) #Splits all words in a flattern RDD instead of being in several RDDs
	tupleCreation = textSplitSpaces.map(lambda x: (x,1))#add the value of 1 in a (key,value) format with each word found
	keyValueAdd = tupleCreation.reduceByKey(lambda x,y: x+y)#add all values having the same key together
	filterKeyValue = keyValueAdd.filter(lambda (x,y) : x != '') #delete all keys being ''
	ordreKeyValue = filterKeyValue.map(lambda a: (a[1],a[0])).sortByKey(False)#exchaning key/value to sort from biggest to smallest
	return ordreKeyValue.top(n_top)#return only the n_top first elements of the RDD in list format

print (wordcountF(10,"/Users/davidrigaux/Documents/GIT/Big_Data/CPI2/algorithmes/spark/spark-2.1.0-bin-hadoop2.7/lipsum.txt",sc))
#calling the main function and printing the results
