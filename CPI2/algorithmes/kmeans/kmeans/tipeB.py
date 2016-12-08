''' Function K-Means
INPUT : kmeans_rand(min,max,n,k), kmeans_file(file_n,k)
min,max : Intervalle des coordonnées
n : Nombres d'éléments
k : Nombre souhaité de Centroides
file_n : nom du fichier avec l'extension.

OUPUT : array [x,y]
Sort un Array qui donne les coordonnées des k centroides et affiches sur un graphique touts les points entrées avec
k centroides initialisé aléatoirement, et un autre graphique après avoir fais les calculs des centroides.
'''

import matplotlib.pyplot as plt
import numpy as np #Import numpy locally in variable np
import seaborn as sns; sns.set()
import matplotlib.cm as cmx
import matplotlib.colors as colors
''' '''
def read_data(file_name):
	data_file = open(file_name, 'r')
	dat = (data_file.read()).split("\n")
	data_file.close()
	dat.pop()
	dataread =[]
	for d in dat:
		esp = d.find(' ')
		x = d[:esp]
		y = d[esp+1:]
		dataread.append((int(x), int(y)))
	del dat
	return dataread

def init_centroids (datas, k):
	centroids_create = datas.copy()
	np.random.shuffle(centroids_create)
	return centroids_create[:k]

def close_centroid(datas, centds):
	dists = np.sqrt(((datas - centds[:, np.newaxis])**2).sum(axis=2))
	return np.argmin(dists, axis=0)


def movmnt_centroids(dat, pclose, cent):
	return np.array([dat[pclose==k].mean(axis=0) for k in range(cent.shape[0])])

def get_cmap(N):
	color_norm = colors.Normalize(vmin=0, vmax=N-1)
	scalar_map = cmx.ScalarMappable(norm=color_norm,cmap='hsv')
	def map_index_to_rgb_color(index):
		return scalar_map.to_rgba(index)
	return map_index_to_rgb_color

def kmeans(data, k):
	plt.subplot(121)
	centroids = init_centroids(data, k)
	cmap = get_cmap(k+1)
	ccentroids = close_centroid(data, centroids)
	for i in range(len(ccentroids) - 1):
		plt.scatter(data[i, 0], data[i, 1], c=cmap(ccentroids[i]))
	plt.scatter(centroids[:, 0], centroids[:, 1], s=20, c='black')
	plt.title('Avant mouvement des centroïdes')
	#plt.grid(False)
	#plt.axis('off')

	plt.subplot(122)
	clo = close_centroid(data, centroids)
	centroids = movmnt_centroids(data, clo, centroids)
	ccentroids = close_centroid(data, centroids)
	for i in range(len(ccentroids) - 1):
		plt.scatter(data[i, 0], data[i, 1], c=cmap(ccentroids[i]))
	plt.scatter(centroids[:, 0], centroids[:, 1], s=20, c='black')
	plt.title('Après mouvement des centroïdes')
	#plt.grid(False)
	#plt.axis('off')

	fig = plt.gcf()
	fig.canvas.set_window_title('Algorirthme K-Means')
	print("Coordonnée des centroides :")

	plt.show()
	return centroids

def kmeans_rand(min,max,n,k):
	return kmeans(np.random.randint(min, max, size=(n, 2)), k)

def kmeans_file(file_n,k):
	return kmeans(np.array(read_data(file_n)), k)
