import numpy as np
import numpy.linalg as npl
import matplotlib.pyplot as plt
import re

def posGNSS(nom):
    '''posGNSS renvoie une liste des donnee de hauteur.'''
    try:
        f = open(nom, "r")
    except IOError as e:
        print("Erreur ouverture fichier.\n", e)

    data = []
    dataNorthing = []
    dataEasting = []

    for c in f:
        if c[:6] == "$GPGGA":
            cc = c.split(",")
            if (cc[-4] != ',' or cc[-4] != '') and (cc[2] != ',' or cc[2] != '') and (cc[4] != ',' or cc[4] != ''):
                data.append(cc[-4])
                dataNorthing.append(cc[2])
                dataEasting.append(cc[4])

    f.close()

    return data, dataNorthing, dataEasting

def posAltitudeGNSS(nom):
    '''posGNSS renvoie une liste des donnee de hauteur.'''
    try:
        f = open(nom, "r")
    except IOError as e:
        print("Erreur ouverture fichier.\n", e)

    data = []
    dataNorthing = []
    dataEasting = []

    for c in f:
        if c[:6] == "$GPGGA":
            cc = c.split(",")
            if (cc[-6] != ',' or cc[-6] != '') and (cc[2] != ',' or cc[2] != '') and (cc[4] != ',' or cc[4] != ''):
                data.append(cc[-6])
                dataNorthing.append(cc[2])
                dataEasting.append(cc[4])

    f.close()

    return data, dataNorthing, dataEasting

def strtoflt(data):
    '''converti une liste de chaine de caractere en float.'''
    cc = [0]
    for i in range(len(data)):
        try:
            cc.append(float(data[i]))
        except:
            pass

    return cc[1:]

def strDegtofltDeg(data):
    '''converti une liste de chaine de caractere en float en degre.'''
    cc = [0]
    for i in range(len(data)):
        try:
            cc.append(float(data[i])/ 100)
            cc[-1] += (float(data[i]) % 100) / 6000
        except:
            pass

    return cc[1:]

def med(data):
    '''height renvoie la mediane de la hauteur, de la latitude, de la longitude.'''
    hmed = data[len(data) // 2]
    return hmed

def height():
    dataHeight = []
    dataHeightEcart = []
    dataNorthing = []
    dataEasting = []

    data, dataN, dataE = posGNSS("text22.txt")
    dataH = strtoflt(data)
    dataN = strDegtofltDeg(dataN)
    dataE = strDegtofltDeg(dataE)


    dataHeight.append(med(dataH))
    dataHeightEcart.append(np.std(dataH))
    dataNorthing.append(med(dataN))
    dataEasting.append(med(dataE))

    data, dataN, dataE = posGNSS("text23.txt")
    dataH = strtoflt(data)
    dataN = strDegtofltDeg(dataN)
    dataE = strDegtofltDeg(dataE)

    dataHeight.append(med(dataH))
    dataHeightEcart.append(np.std(dataH))
    dataNorthing.append(med(dataN))
    dataEasting.append(med(dataE))

    data, dataN, dataE = posGNSS("texte25.txt")
    dataH = strtoflt(data)
    dataN = strDegtofltDeg(dataN)
    dataE = strDegtofltDeg(dataE)

    dataHeight.append(med(dataH))
    dataHeightEcart.append(np.std(dataH))
    dataNorthing.append(med(dataN))
    dataEasting.append(med(dataE))

    data, dataN, dataE = posGNSS("texte26.txt")
    dataH = strtoflt(data)
    dataN = strDegtofltDeg(dataN)
    dataE = strDegtofltDeg(dataE)

    dataHeight.append(med(dataH))
    dataHeightEcart.append(np.std(dataH))
    dataNorthing.append(med(dataN))
    dataEasting.append(med(dataE))

    data, dataN, dataE = posGNSS("texte27.txt")
    dataH = strtoflt(data)
    dataN = strDegtofltDeg(dataN)
    dataE = strDegtofltDeg(dataE)

    dataHeight.append(med(dataH))
    dataHeightEcart.append(np.std(dataH))
    dataNorthing.append(med(dataN))
    dataEasting.append(med(dataE))

    data, dataN, dataE = posGNSS("texte28.txt")
    dataH = strtoflt(data)
    dataN = strDegtofltDeg(dataN)
    dataE = strDegtofltDeg(dataE)

    dataHeight.append(med(dataH))
    dataHeightEcart.append(np.std(dataH))
    dataNorthing.append(med(dataN))
    dataEasting.append(med(dataE))

    data, dataN, dataE = posGNSS("texte29.txt")
    dataH = strtoflt(data)
    dataN = strDegtofltDeg(dataN)
    dataE = strDegtofltDeg(dataE)

    dataHeight.append(med(dataH))
    dataHeightEcart.append(np.std(dataH))
    dataNorthing.append(med(dataN))
    dataEasting.append(med(dataE))

    data, dataN, dataE = posGNSS("texte291.txt")
    dataH = strtoflt(data)
    dataN = strDegtofltDeg(dataN)
    dataE = strDegtofltDeg(dataE)

    dataHeight.append(med(dataH))
    dataHeightEcart.append(np.std(dataH))
    dataNorthing.append(med(dataN))
    dataEasting.append(med(dataE))

    data, dataN, dataE = posGNSS("texte292.txt")
    dataH = strtoflt(data)
    dataN = strDegtofltDeg(dataN)
    dataE = strDegtofltDeg(dataE)

    dataHeight.append(med(dataH))
    dataHeightEcart.append(np.std(dataH))
    dataNorthing.append(med(dataN))
    dataEasting.append(med(dataE))

    data, dataN, dataE = posGNSS("texte293.txt")
    dataH = strtoflt(data)
    dataN = strDegtofltDeg(dataN)
    dataE = strDegtofltDeg(dataE)

    dataHeight.append(med(dataH))
    dataHeightEcart.append(np.std(dataH))
    dataNorthing.append(med(dataN))
    dataEasting.append(med(dataE))

    data, dataN, dataE = posGNSS("texte294.txt")
    dataH = strtoflt(data)
    dataN = strDegtofltDeg(dataN)
    dataE = strDegtofltDeg(dataE)

    dataHeight.append(med(dataH))
    dataHeightEcart.append(np.std(dataH))
    dataNorthing.append(med(dataN))
    dataEasting.append(med(dataE))

    return dataHeight, dataHeightEcart, dataNorthing, dataEasting

def altitude():
    dataHeight = []
    dataHeightEcart = []
    dataNorthing = []
    dataEasting = []

    data, dataN, dataE = posAltitudeGNSS("text22.txt")
    dataH = strtoflt(data)
    dataN = strDegtofltDeg(dataN)
    dataE = strDegtofltDeg(dataE)

    dataHeight.append(med(dataH))
    dataHeightEcart.append(np.std(dataH))
    dataNorthing.append(med(dataN))
    dataEasting.append(med(dataE))

    data, dataN, dataE = posAltitudeGNSS("text23.txt")
    dataH = strtoflt(data)
    dataN = strDegtofltDeg(dataN)
    dataE = strDegtofltDeg(dataE)

    dataHeight.append(med(dataH))
    dataHeightEcart.append(np.std(dataH))
    dataNorthing.append(med(dataN))
    dataEasting.append(med(dataE))

    data, dataN, dataE = posAltitudeGNSS("texte25.txt")
    dataH = strtoflt(data)
    dataN = strDegtofltDeg(dataN)
    dataE = strDegtofltDeg(dataE)

    dataHeight.append(med(dataH))
    dataHeightEcart.append(np.std(dataH))
    dataNorthing.append(med(dataN))
    dataEasting.append(med(dataE))

    data, dataN, dataE = posAltitudeGNSS("texte26.txt")
    dataH = strtoflt(data)
    dataN = strDegtofltDeg(dataN)
    dataE = strDegtofltDeg(dataE)

    dataHeight.append(med(dataH))
    dataHeightEcart.append(np.std(dataH))
    dataNorthing.append(med(dataN))
    dataEasting.append(med(dataE))

    data, dataN, dataE = posAltitudeGNSS("texte27.txt")
    dataH = strtoflt(data)
    dataN = strDegtofltDeg(dataN)
    dataE = strDegtofltDeg(dataE)

    dataHeight.append(med(dataH))
    dataHeightEcart.append(np.std(dataH))
    dataNorthing.append(med(dataN))
    dataEasting.append(med(dataE))

    data, dataN, dataE = posAltitudeGNSS("texte28.txt")
    dataH = strtoflt(data)
    dataN = strDegtofltDeg(dataN)
    dataE = strDegtofltDeg(dataE)

    dataHeight.append(med(dataH))
    dataHeightEcart.append(np.std(dataH))
    dataNorthing.append(med(dataN))
    dataEasting.append(med(dataE))

    data, dataN, dataE = posAltitudeGNSS("texte29.txt")
    dataH = strtoflt(data)
    dataN = strDegtofltDeg(dataN)
    dataE = strDegtofltDeg(dataE)

    dataHeight.append(med(dataH))
    dataHeightEcart.append(np.std(dataH))
    dataNorthing.append(med(dataN))
    dataEasting.append(med(dataE))

    data, dataN, dataE = posAltitudeGNSS("texte291.txt")
    dataH = strtoflt(data)
    dataN = strDegtofltDeg(dataN)
    dataE = strDegtofltDeg(dataE)

    dataHeight.append(med(dataH))
    dataHeightEcart.append(np.std(dataH))
    dataNorthing.append(med(dataN))
    dataEasting.append(med(dataE))

    data, dataN, dataE = posAltitudeGNSS("texte292.txt")
    dataH = strtoflt(data)
    dataN = strDegtofltDeg(dataN)
    dataE = strDegtofltDeg(dataE)

    dataHeight.append(med(dataH))
    dataHeightEcart.append(np.std(dataH))
    dataNorthing.append(med(dataN))
    dataEasting.append(med(dataE))

    data, dataN, dataE = posAltitudeGNSS("texte293.txt")
    dataH = strtoflt(data)
    dataN = strDegtofltDeg(dataN)
    dataE = strDegtofltDeg(dataE)

    dataHeight.append(med(dataH))
    dataHeightEcart.append(np.std(dataH))
    dataNorthing.append(med(dataN))
    dataEasting.append(med(dataE))

    data, dataN, dataE = posAltitudeGNSS("texte294.txt")
    dataH = strtoflt(data)
    dataN = strDegtofltDeg(dataN)
    dataE = strDegtofltDeg(dataE)

    dataHeight.append(med(dataH))
    dataHeightEcart.append(np.std(dataH))
    dataNorthing.append(med(dataN))
    dataEasting.append(med(dataE))

    return dataHeight, dataHeightEcart, dataNorthing, dataEasting

def reg(tab, tabEasting):
    '''Regression lineaire par moindre carre.'''
    a = np.ones((len(tab), 2))
    a[:, 1] = tabEasting

    x = moindreCarre(tab, a)

    return x

def f(xx, xp):
    tab = [0] * len(xx)
    for i in range(len(xx)):
        tab[i] = xp[1] * xx[i] + xp[0]

    return tab


def moindreCarre(y, a):
    return npl.inv(a.T @ a) @ (a.T @ y)

if __name__ == '__main__':
    dataHeight, dataHeightEcart, dataNorthing, dataEasting = height()

    print(dataHeightEcart)
    xp = reg(dataHeight, dataEasting)
    x_min = min(dataEasting)
    x_max = max(dataEasting)

    xx = np.arange(x_min, x_max, 0.1)
    xh = f(xx, xp)

    fig = plt.figure()
    plt.scatter(dataEasting, dataHeight, label="donnée brute.")
    #plt.errorbar(dataEasting, dataHeight, yerr = dataHeightEcart)
    plt.plot(xx, xh, color="r", label="regréssion linéaire.")
    plt.title("Hauteur entre le geoide et l'ellipsiode WGS84.")
    plt.xlabel("Longitude (en deg, minute).")
    plt.ylabel("Hauteur (en metre).")
    plt.xlim(max(dataEasting), min(dataEasting))
    plt.figtext(0.15, 0.05, "Brest", fontsize=6)
    plt.figtext(0.55, 0.05, "Saint-Brieuc", fontsize=6)
    plt.figtext(0.85, 0.05, "Avranches", fontsize=6)
    plt.legend()
    plt.show()

    dataHeight, dataHeightEcart, dataNorthing, dataEasting = altitude()

    print(dataHeightEcart)



    fig = plt.figure()
    plt.scatter(dataEasting, dataHeight)
    plt.errorbar(dataEasting, dataHeight, yerr = dataHeightEcart)
    plt.title("Altitude (en metre).")
    plt.xlabel("Longitude (en deg).")
    plt.ylabel("Hauteur (en metre).")
    plt.xlim(max(dataEasting), min(dataEasting))
    plt.show()



