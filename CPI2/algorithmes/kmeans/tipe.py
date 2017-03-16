''' Function K-Means
INPUT : kmeans_rand(min,max,n,k), kmeans_file(file_n,k)
min,max : Intervalle des coordoonées
n : Nombres d'éléments
k : Nombre souhaité de Centroïdes
file_n : nom du fichier avec l'extension.

OUPUT : array [x,y]
Sort un Array qui donne les coordonnées des k centroïdes et affiches sur un graphique touts les points entrées avec
k centroïdes initialisé aléatoirement, et un autre graphique après avoir fais les calculs des centroïdes.
'''

import matplotlib.pyplot as plt
import numpy as np #Import numpy locally in variable np
import sys
import math as m
import seaborn as sns; sns.set()
import matplotlib.cm as cmx
import matplotlib.colors as colors
from numpy import linalg as LA

#Fonction read_data permet de lire les données d'un fichier formaté et de resortir un array des éléments du fichier
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
	return np.asarray(dataread)

#Fonction init_centroids ressort k centroids aléatoire
def init_centroids (datas, k):
	centroids_create = datas.copy()
	np.random.shuffle(centroids_create)
	return centroids_create[:k]



'''Fonction close_centroid nous permet de calculer pour chaque élément le centroides qui lui est le plus proche et le ressort sous forme
d'array'''
def close_centroid(datas, centds):
	pproche = []
	for ind in datas:
		normes = []
		for cen in centds:
			normes.append(m.sqrt((cen[0]-ind[0])**2 + (cen[1]-ind[1])**2))
		pproche.append(normes.index(min(normes)))
	return np.asarray(pproche)



'''Fonction movmnt_centroids calcul la moyenne des vecteurs de chaque points par rapport à son centroide le plus proche
qui le déplace ensuite par rapport à ce vecteur moyen'''
def movmnt_centroids(dat, pclose, cent):
	for i in range(len(cent)):
		indices = np.where(pclose == i)[0]
		sumx = 0
		sumy = 0
		card = len(indices)
		for j in indices:
			sumx += dat[j][0]
			sumy += dat[j][1]
		cent[i][0] = sumx//card
		cent[i][1] = sumy//card
	return cent

#Fonction qui affecte les nouvelles positions des centroids
itera = 0
def ite_movmt_centro(data,centr):
	global itera
	done = False
	epsi = 0
	def ecart (copie,origin,index):
		ex = abs(ccentre[index][0] - centr[index][0])
		ey = abs(ccentre[index][1] - centr[index][1])
		return True if (ex <= epsi and ey <= epsi) else False

	while (not done):
		itera += 1
		print(itera)
		ccentre = centr.copy()
		pp = close_centroid(data,centr)
		centr = movmnt_centroids(data, pp, centr)
		lon = len(ccentre)
		for i in range(lon):
			if ecart(ccentre,centr,i):
				if (i == (len(ccentre)-1)):
					done = True
				else:
					pass
			else:
				break
	return centr

#get_cmap permet de créer un array avec N couleurs différente
def get_cmap(N):
	color_norm = colors.Normalize(vmin=0, vmax=N-1)
	scalar_map = cmx.ScalarMappable(norm=color_norm,cmap='hsv')
	def map_index_to_rgb_color(index):
		return scalar_map.to_rgba(index)
	return map_index_to_rgb_color


#Ajouter les calculs d'intérations

'''Fonction kmeans, est la fonction principale qui appelle toute les fonctions ci-dessus. Elle sort un array avec les
coordonnées de chaque centroide après que les centroides convergent et affiche dans une figure le grpahique de chaque
chaque points avant et après l'application de kmeans'''
def kmeans(data, k):
	plt.subplot(121)
	plt.suptitle('K-Means', fontsize=14, fontweight='bold')
	centroids = init_centroids(data, k)
	cmap = get_cmap(k+1)
	ccentroids = close_centroid(data, centroids)

	for i in range(len(ccentroids)):
		plt.scatter(data[i, 0], data[i, 1], c=cmap(ccentroids[i]))
	plt.scatter(centroids[:, 0], centroids[:, 1], s=20, c='black')
	plt.title('Avant')
	plt.grid(False)
	plt.axis('off')

	plt.subplot(122)
	centroids = ite_movmt_centro(data,centroids)
	ccentroids = close_centroid(data, centroids)
	for i in range(len(ccentroids)):
		plt.scatter(data[i, 0], data[i, 1], c=cmap(ccentroids[i]))
	plt.scatter(centroids[:, 0], centroids[:, 1], s=55, c='black')
	plt.title('Après %d itérations' % itera)
	plt.grid(False)
	plt.axis('off')

	fig = plt.gcf()

	fig.canvas.set_window_title('Algorirthme K-Means')
	print("Coordonnée des centroides :")

	plt.show()
	return centroids



#Fonction kmeans_rand appelle kmean avec des données aléatoire
def kmeans_rand(mini,maxi,n,k):
	return kmeans(np.random.randint(mini, maxi, size=(n, 2)), k)



#Fonction kmeans_file appelle kmean avec des données pris d'un fichier
def kmeans_file(file_n,k):
	return kmeans(np.array(read_data(file_n)), k)
