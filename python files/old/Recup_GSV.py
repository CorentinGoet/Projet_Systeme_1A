#Script récupération trame NMEA GSV
import matplotlib.pyplot as plt
import numpy as np

def GSV(fichier):
    f = open(fichier)
    L = f.readlines()
    trames = []
    for i in range(len(L)):
        trames.append(L[i].split(","))

    trames_GSV = []
    for t in trames:
        if t[0] == '$GPGSV':
            trames_GSV.append(t)
    print('trames GSV', trames_GSV)

    GSV = []
    for t in trames_GSV: # eviter les doublons
        if t not in GSV:
            GSV.append(t)

    nb_tramesGSV = int(GSV[0][1])
    nb_satellites = int(GSV[0][3])

    # GSV = GSV[0:nb_tramesGSV]
    sat = []
    trame = 1
    cnt = 0
    for i in range(nb_satellites):
        if i > 3 * trame:  # 3 satellites par trame
            cnt = 0
            trame += 1
        sat_i = [GSV[trame - 1][4 + cnt * 4], (GSV[trame - 1][5 + cnt * 4], GSV[trame - 1][6 + cnt * 4])]
        sat.append(sat_i)
        cnt += 1

    print('GSV', GSV)
    print('Nombre de satellites visibles : ', nb_satellites)
    print(sat)

    elevation = []
    azimut = []

    for s in sat:
        elevation.append(int(s[1][0]))
        azimut.append(int(s[1][1]))

    for i in range(len(azimut)):
        azimut[i] = azimut[i] * 180 / np.pi

    r = []
    for i in range(len(elevation)):
        elevation[i] = elevation[i] * 180 / np.pi
        rayon = np.cos(elevation[i])
        r.append(rayon)

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.plot(azimut, r, 'o', color='r')
    ax.set_rticks([])
    ax.set_title("Vue du ciel des satellites visibles", va='bottom')
    plt.show()

GSV('..\\files\\acquisition 1.txt')