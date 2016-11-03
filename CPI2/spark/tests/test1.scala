val conf = new SparkConf().setAppName("WordCount")
val sc = new SparkContext(conf)

val input = sc.textFile(inputFile)
val words = input.flatMap
