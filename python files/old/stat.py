import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms

def posGNSS(nom):
    '''posGNSS renvoie une liste des donnee de hauteur.'''
    try:
        f = open(nom, "r")
    except IOError as e:
        print("Erreur ouverture fichier.\n", e)

    dataEasting = []
    dataNorthing = []


    for c in f:
        if c[:6] == "$GPGGA":
            cc = c.split(",")
            print(cc)
            if (cc[-4] != ',' or cc[-4] != '') and (cc[2] != ',' or cc[2] != '') and (cc[4] != ',' or cc[4] != ''):
                dataEasting.append(cc[4])
                dataNorthing.append(cc[2])


    f.close()

    return dataEasting, dataNorthing

def incertitudeEllipse(m, seuil):
    '''incertitudeEllipse trace l'ellipse d'incertitude des donnees.
    Un test khi2 est utlise.

    Parametres:
    m: liste de liste (donne)
    seuil: float (erreur du test Khi2)'''
    tabKhi2 = [[0.1, 4.61], [0.05, 5.99], [0.01, 9.21]]
    k = 0

    for i in range(len(tabKhi2)):
        if tabKhi2[i][0] == seuil:
            k = tabKhi2[i][1]

    if k == 0:
        k = tabKhi2[1][1]

    cov_xy = np.cov(m)
    x_mean = np.mean(m[0])
    y_mean = np.mean(m[1])

    r1 = ((cov_xy[0, 0] + cov_xy[1, 1]) / 2) + (((cov_xy[0, 0] - cov_xy[1, 1]) / 2) ** 2 + cov_xy[0, 1] ** 2) ** 0.5
    r2 = ((cov_xy[0, 0] + cov_xy[1, 1]) / 2) - (((cov_xy[0, 0] - cov_xy[1, 1]) / 2) ** 2 + cov_xy[0, 1] ** 2) ** 0.5


    if cov_xy[0, 1] == 0 and cov_xy[0, 0] > cov_xy[1, 1]:
        theta = 0
    elif cov_xy[0, 1] == 0 and cov_xy[0, 0] < cov_xy[1, 1]:
        theta = np.pi / 2
    elif cov_xy[0, 0] == 0:
        theta = np.pi / 2
    else:
        theta = np.arctan(cov_xy[1, 1] / cov_xy[0, 0])

    x = []
    y = []


    t = np.linspace(0, 2 * np.pi, 100)

    for i in range(len(t)):
        x.append((k * r1) ** 0.5 * np.cos(theta) * np.cos(t[i]) - (k * r2) ** 0.5 * np.sin(theta) * np.sin(t[i]) + x_mean)
        y.append((k * r1) ** 0.5 * np.sin(theta) * np.cos(t[i]) + (k * r2) ** 0.5 * np.cos(theta) * np.sin(t[i]) + y_mean)

    plt.scatter(m[0], m[1])
    plt.plot(x, y, label = str(1 - seuil)[2:] + '%', linestyle = '--')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    tabEasting, tabNorthing = posGNSS("..\\files\\tour_terrain.txt")
    j = 0

    for i in range(len(tabNorthing)):
        if float(tabNorthing[i]) > 4824.13904:
            j += 1

    print(j)
    print(len(tabNorthing))

    m = np.zeros((j, 2))

    for i in range(j):
        if float(tabNorthing[i]) > 4824.13904:
            m[i][0] = tabEasting[i]
            m[i][1] = tabNorthing[i]

    m = m.T

    incertitudeEllipse(m, 0.01)
