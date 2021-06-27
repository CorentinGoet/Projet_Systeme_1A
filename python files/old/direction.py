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
    dataMagnetic = []
    dataVelocity = []

    for c in f:
        if c[:6] == "$GPVTG":
            cc = c.split(",")
            data.append(float(cc[1]))
            dataMagnetic.append(cc[3])
            dataVelocity.append(cc[7])

    f.close()

    return data, dataMagnetic, dataVelocity

def mesure(data):
    dataCap = []
    m = np.mean(data)
    ecart = np.std(data)

    for i in range(len(data)):
        if abs(data[i] - m) < 3 * ecart:
            dataCap.append(data[i])

    return dataCap, m, ecart

if __name__ == '__main__':
    #mesure1
    fichier = "..\\files\\mesures_stat\\8000_PHONE.nmea"
    data1, dataMagnetic1, dataVelocity1 = posGNSS(fichier)


    print(data1)
    print(dataMagnetic1)
    print(dataVelocity1)

    fig = plt.figure()
    plt.scatter(np.linspace(0, len(data1), len(data1)), data1)
    plt.title("cap reel.")
    plt.xlabel("Mesure")
    plt.ylabel("cap reel (en deg)")
    plt.show()

    dataCap1, m1, ecart1 = mesure(data1)
    print(dataCap1)
    print("Moyenne: ", m1)
    print("Ecart type: ", ecart1)

    fig = plt.figure()
    plt.scatter(np.linspace(0, len(dataCap1), len(dataCap1)), dataCap1)
    plt.plot(np.linspace(0, len(dataCap1), len(dataCap1)), np.linspace(m1, m1, len(dataCap1)))
    plt.plot(np.linspace(0, len(dataCap1), len(dataCap1)), np.linspace(m1 - ecart1, m1 - ecart1, len(dataCap1)))
    plt.plot(np.linspace(0, len(dataCap1), len(dataCap1)), np.linspace(m1 + ecart1, m1 + ecart1, len(dataCap1)))
    plt.title("cap reel.")
    plt.xlabel("Mesure")
    plt.ylabel("cap reel (en deg)")
    plt.show()

    #mesure3, degage

    data3, dataMagnetic3, dataVelocity3 = posGNSS(fichier)

    print(data3)
    print(dataMagnetic3)
    print(dataVelocity3)

    fig = plt.figure()
    plt.scatter(np.linspace(0, len(data3), len(data3)), data3)
    plt.title("cap reel.")
    plt.xlabel("Mesure")
    plt.ylabel("cap reel (en deg)")
    plt.show()

    dataCap3, m3, ecart3 = mesure(data3)
    print(dataCap3)
    print("Moyenne: ", m3)
    print("Ecart type: ", ecart3)

    #mesure2, non degage

    data2, dataMagnetic2, dataVelocity2 = posGNSS("test49.txt")

    print(data2)
    print(dataMagnetic2)
    print(dataVelocity2)

    fig = plt.figure()
    plt.scatter(np.linspace(0, len(data2), len(data2)), data2)
    plt.title("cap reel.")
    plt.xlabel("Mesure")
    plt.ylabel("cap reel (en deg)")
    plt.show()

    dataCap2, m2, ecart2 = mesure(data2)
    print(dataCap2)
    print("Moyenne: ", m2)
    print("Ecart type: ", ecart2)

    fig = plt.figure()
    plt.scatter(np.linspace(0, len(dataCap2), len(dataCap2)), dataCap2)
    plt.plot(np.linspace(0, len(dataCap2), len(dataCap2)), np.linspace(m2, m2, len(dataCap2)))
    plt.plot(np.linspace(0, len(dataCap2), len(dataCap2)), np.linspace(m2 - ecart2, m2 - ecart2, len(dataCap2)))
    plt.plot(np.linspace(0, len(dataCap2), len(dataCap2)), np.linspace(m2 + ecart2, m2 + ecart2, len(dataCap2)))
    plt.scatter(np.linspace(0, len(dataCap1), len(dataCap1)), dataCap1)
    plt.plot(np.linspace(0, len(dataCap1), len(dataCap1)), np.linspace(m1, m1, len(dataCap1)))
    plt.plot(np.linspace(0, len(dataCap1), len(dataCap1)), np.linspace(m1 - ecart1, m1 - ecart1, len(dataCap1)))
    plt.plot(np.linspace(0, len(dataCap1), len(dataCap1)), np.linspace(m1 + ecart1, m1 + ecart1, len(dataCap1)))
    plt.scatter(np.linspace(0, len(dataCap3), len(dataCap3)), dataCap3)
    plt.plot(np.linspace(0, len(dataCap3), len(dataCap3)), np.linspace(m3, m3, len(dataCap3)))
    plt.plot(np.linspace(0, len(dataCap3), len(dataCap3)), np.linspace(m3 - ecart3, m3 - ecart3, len(dataCap3)))
    plt.plot(np.linspace(0, len(dataCap3), len(dataCap3)), np.linspace(m3 + ecart3, m3 + ecart3, len(dataCap3)))
    plt.title("cap reel.")
    plt.xlabel("Mesure")
    plt.ylabel("cap reel (en deg)")
    plt.show()
