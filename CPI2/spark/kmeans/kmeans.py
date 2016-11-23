import numpy as np #Import numpy locally in variable np
from apgl.graph import *


#Random Data Sets : np.random.randint(low,high, size=(num,dim))

def read_data():
	data_file = open('dataset.in','r')
	dat = (data_file.read()).split("\n")
	data_file.close()
	dat.pop()
	data =[]
	for d in dat:
		esp = d.find(' ')
		x = d[:esp]
		y = d[esp+1:]
		data.append((int(x),int(y)))
	del dat
	return data


data = np.array(read_data())
print(data)
