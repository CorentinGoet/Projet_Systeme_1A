import matplotlib.pyplot as plt
from pyproj import Proj, transform
from pyproj import Transformer
import matplotlib.image as img
import numpy as np


#### Grandeurs utilies

# x=alpha*E +beta*N + ct1
alpha = 0.622672164
beta = -0.093309478
ct1 = 546305.0875

# y=gamma*E +delta*N + ct2
gamma = -0.046338701
delta = -0.620534551
cte2 = 4251139.032

def deg_to_Lamb(x1, y1):
    transformer = Transformer.from_crs(4326, 2154, always_xy=True)
    points = [(x1, y1)]
    for pt in transformer.itransform(points):
        return pt


def conversion_pour_image(E, N):
    x = alpha * E + beta * N + ct1
    y = gamma * E + delta * N + cte2
    return x, y

def stats_horizontal(nb_mesures, fichiers, ref, titre):
    GPA = []
    for i in range(nb_mesures):
        fich = open(fichiers[i], "r")
        lignes = fich.readlines()
        for ligne in lignes:
            if '$GPGGA' in ligne:
                GPA.append(ligne)

    liste_lat = []
    liste_long = []
    liste_Xlamb = []
    liste_Ylamb = []

    for mesure in GPA:
        mes = mesure.split(",")[2:6]
        if mes[1] == 'N':
            liste_long.append(float(mes[0][0:2]) + (float(mes[0][2:])) / 60)
        else:
            liste_long.append(-float(mes[0][0:2]) - (float(mes[0][2:])) / 60)
        if mes[3] == 'E':
            liste_lat.append(float(mes[2][0:3]) + (float(mes[2][3:])) / 60)
        else:
            liste_lat.append(-float(mes[2][0:3]) - (float(mes[2][3:])) / 60)

    for i in range(len(liste_lat)):
        X, Y = deg_to_Lamb(liste_lat[i], liste_long[i])
        liste_Xlamb.append(X)
        liste_Ylamb.append(Y)

    #moyenne des mesures
    m_x = np.mean(liste_Xlamb)
    m_y = np.mean(liste_Ylamb)
    plt.plot(m_x, m_y, 'og', label='moyenne')
    if ref == 8000:
        x_ref, y_ref = 147787.422, 6839274.663  # 8000
    else:
        x_ref, y_ref = 147788.609, 6839279.724  # 9000


    plt.plot(x_ref, y_ref, "or", label='réference')

    for i in range(len(liste_Ylamb)):
        plt.plot(liste_Xlamb[i], liste_Ylamb[i], "+b")
    plt.title(titre)
    plt.legend()

    biais = np.sqrt((m_x-x_ref)**2+(m_y-y_ref)**2)
    fid = np.sqrt(np.std(liste_Xlamb)**2 + np.std(liste_Ylamb)**2)
    prec = np.sqrt(biais**2 + fid**2)
    print('biais : ',biais, ' m') #Justesse
    print('Fidélité : ', fid, 'm')
    print('Précision : ', prec, 'm')
    plt.show()

def stats_vertical(fichier1,fichier2, titre):
    GGA1 = []
    GGA2 = []
    altitude1 = []
    altitude2 = []
    fich1 = open(fichier1, "r")
    fich2 = open(fichier2, "r")
    lignes1 = fich1.readlines()
    lignes2 = fich2.readlines()
    for ligne in lignes1:
        if '$GPGGA' in ligne:
            GGA1.append(ligne.split(','))
    for ligne in lignes2:
        if '$GPGGA' in ligne:
            GGA2.append(ligne.split(','))

    for i in range(len(GGA1)):
        try:
            altitude1.append(float(GGA1[i][-6]) - float(GGA1[i][-4]))
        except:
            pass
    for i in range(len(GGA2)):
        try:
            altitude2.append(float(GGA2[i][-6]) - float(GGA2[i][-4]))
        except:
            pass

    nb_mesures1 = len(altitude1)
    nb_mesures2 = len(altitude2)
    altitude1 = np.array(altitude1)
    altitude2 = np.array(altitude2)

    # stats des mesures
    m_1 = np.mean(altitude1)
    m_2 = np.mean(altitude2)
    fid1 = np.std(altitude1)
    fid2 = np.std(altitude2)

    nb_mesures = max(nb_mesures1, nb_mesures2)
    x = np.linspace(1, nb_mesures, nb_mesures)
    plt.plot(x, m_1*np.linspace(1, 1, nb_mesures), 'r', label=fichier1)
    plt.plot(x, m_2 * np.linspace(1, 1, nb_mesures), 'g', label= fichier2)
    plt.plot(x, (m_1 - fid1)*np.linspace(1, 1, nb_mesures), '--r')
    plt.plot(x, (m_1 + fid1)*np.linspace(1, 1, nb_mesures), '--r')
    plt.plot(x, (m_2 - fid2) * np.linspace(1, 1, nb_mesures), '--g')
    plt.plot(x, (m_2 + fid2) * np.linspace(1, 1, nb_mesures), '--g')

    for i in range(nb_mesures1):
        plt.plot(i, altitude1[i], "+k")

    for i in range(nb_mesures2):
        plt.plot(i, altitude2[i], "+b")
    plt.title(titre)
    plt.xlabel = 'mesure'
    plt.ylabel = 'altitude [m]'
    plt.legend()

    print('Fidélité '+fichier1+' : ', fid1, 'm')
    print('Fidélité '+fichier2+' : ', fid2, 'm')

    plt.show()



if __name__ == "__main__":
    #stats_horizontal(2, ("UV24_L_Proflex_8000.txt", "UV24_V_Proflex_8000.txt"), 8000, 'Acquisition Proflex 8000')
    stats_vertical('..\\files\\mesures_stat\\UE24_SP80_20210602_EB06.txt', '..\\files\\mesures_stat\\EB06_GSTAR_11h40.txt', 'Altitude Proflex')
    #stats_vertical('UV24_V_GStarIV_8000.txt', 'UV24_L_Proflex_8000.txt', 'Altitude 8000')