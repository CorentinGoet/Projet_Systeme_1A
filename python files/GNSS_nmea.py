#!/bin/python3
# -*- coding: utf-8 -*-

"""
Author : Corentin GOETGHEBEUR; Maël GODARD; Raphaël VALERI; Hugo FAUVEL
"""
import matplotlib.pyplot as plt
from pyproj import Transformer
import matplotlib.image as img
import numpy as np
from osgeo import gdal
import serial



class GPGGA:
    """
    Classe correspondant au traitement des données NMEA GPGGA transmisent par le GPS
    """

    def __init__(self, file_name, image):
        self.GGA = self.lecture(file_name)
        self.image = image
        self.liste_long, self.liste_lat, self.liste_alt = self.coords(self.GGA)
        self.liste_Xlamb = []
        self.liste_Ylamb = []
        self.liste_img_x = []
        self.liste_img_y = []



        for i in range(len(self.liste_lat)):
            x_lamb, y_lamb = self.deg_to_Lamb(self.liste_lat[i], self.liste_long[i])
            self.liste_Xlamb.append(x_lamb)
            self.liste_Ylamb.append(y_lamb)

        for i in range(len(self.liste_Xlamb)):
            X, Y = self.conv_img(self.liste_Xlamb[i], self.liste_Ylamb[i])
            print(X, Y)
            self.liste_img_x.append(X)
            self.liste_img_y.append(Y)

    def lecture(self, file_name):
        """
        Lecture du fichier file_name
        :return: liste des trames GPGGA
        """
        file = open(file_name, "r")
        lignes = file.readlines()
        GGA = []
        for ligne in lignes:
            if '$GPGGA' in ligne:
                GGA.append(ligne)
        return GGA

    def deg_to_Lamb(self, x1, y1):
        """
        Conversion des mesures en degrés vers un système de coordonnées de Lambert
        :param x1:
        :param y1:
        :return:
        """
        transformer = Transformer.from_crs(4326, 2154, always_xy=True)
        points = [(x1, y1)]
        for pt in transformer.itransform(points):
            return pt

    def coords(self, liste):
        """
        Récupère la longitude et la latitude à partir de la trame NMEA GPGGA
        :return: (Liste des longitudes, liste des latitudes)
        """
        long = []
        lat = []
        alt = []

        for mesure in liste:
            mes = mesure.split(",")[2:]
            print(mes)
            try:
                if mes[1] == 'N':
                    long.append(float(mes[0][0:2]) + (float(mes[0][2:])) / 60)
                else:
                    long.append(-float(mes[0][0:2]) - (float(mes[0][2:])) / 60)
                if mes[3] == 'E':
                    lat.append(float(mes[2][0:3]) + (float(mes[2][3:])) / 60)
                else:
                    lat.append(-float(mes[2][0:3]) - (float(mes[2][3:])) / 60)
                if mes[-5] == 'M':
                    alt.append(float(mes[-6]))
            except Exception as e:
                print('trame incomplète ou non compatible')
        return long, lat, alt

    def img_data(self, image):
        """
        Replace les coordonnées par rapport à l'image. (valeurs de positionnement de l'image obtenues sur moodle)
        :param image: image de background
        :return: (x, y) origine de la photo
        """

        # données de l'image
        im = gdal.Open('..\\images\\ensta_2015.jpg', gdal.GA_ReadOnly)
        geo = im.GetGeoTransform()
        origin_x, origin_y = geo[0], geo[3]
        scale_x, scale_y = geo[1], geo[5]
        return origin_x, origin_y, scale_x, scale_y

    def conv_img(self, E, N):
        """
        Replace les coordonnées par rapport à l'image. (valeurs de positionnement de l'image obtenues sur moodle)
        :param E: longitude (lambert93)
        :param N: latitude (lambert93)
        :return: (x, y) coordonnées corrigées
        """
        origin_x, origin_y, scale_x, scale_y = self.img_data(self.image)

        x = (E - origin_x) / scale_x
        y = (N - origin_y) / scale_y

        return x, y

    def aff_V2(self):
        """
        inutile
        :return:
        """
        im = gdal.Open(self.image)
        nx = im.RasterXSize
        ny = im.RasterYSize
        nb = im.RasterCount
        image = np.zeros((ny, nx, nb))
        image[:, :, 0] = im.GetRasterBand(1).ReadAsArray() / 255
        image[:, :, 1] = im.GetRasterBand(2).ReadAsArray() / 255
        image[:, :, 2] = im.GetRasterBand(3).ReadAsArray() / 255
        print(image[0, 0, :])
        print(image.shape)
        plt.figure()
        plt.imshow(image)
        plt.plot(self.liste_img_x, self.liste_img_y)
        plt.show()

    def aff_V3_init(self):
        """
        initialisation de l'affichage en direct
        :return:
        """
        fig = plt.figure(1)
        plt.title("Position GPS en direct")

        plt.ion()

        # affichage de l'image
        background = img.imread(self.image)
        plt.imshow(background)
        plt.xlim([500, 1000])
        plt.ylim([1200, 800])


        plt.pause(1)


        # les points à afficher sont ajoutés dans aff_V3_add

    def aff_V3_add(self, trame):
        """
        ajoute à la figure le point associé à la trame
        :param trame:
        :return:
        """
        if trame.split(',')[0] != '$GPGGA':
            print("Trame incorrecte")
        else:
            print(trame)
            long, lat = self.coords([trame])
            if len(long) == len(lat) == 1:
                xlamb, ylamb = self.deg_to_Lamb(lat[0], long[0])
                x, y = self.conv_img(xlamb, ylamb)
                print(x, y)
                plt.figure(1)
                plt.plot(x, y, '+b')
                plt.pause(0.5)


    def affichage(self):
        """
        Affiche sur l'image donnée en entrée les points de position GPS
        :param image: image de fond
        :return:
        """

        plt.figure()
        plt.title("Position GPS")

        # affichage de l'image
        background = img.imread(self.image)
        plt.imshow(background)
        plt.xlim([500, 1000])
        plt.ylim([1200, 800])
        # affichage des données GPS

        plt.plot(self.liste_img_x, self.liste_img_y, '+b')

        plt.show()

    def test_statistiques(self, ref):
        """
        Mesure la précision des données en calculant le biais, fidélité et précision
        :param ref: point de référence (8000, 9000 ...)
        :return:
        """

        # Coordonnées du point de référence
        if ref == 8000:
            x_ref, y_ref, z_ref = 147787.422, 6839274.663, 88.837  # 8000
        elif ref == 'EB05':
            x_ref, y_ref, z_ref = 147807.631, 6839347.831, 88.91
        elif ref == 'EB06':
            x_ref, y_ref, z_ref = 147799.5, 6839343.26, 88.84

        # Calculs des moyennes
        m_x = np.mean(self.liste_Xlamb)
        m_y = np.mean(self.liste_Ylamb)
        m_z = np.mean(self.liste_alt)

        # Calculs du biais, de la fidélité et de la précision
        biais = np.sqrt((m_x - x_ref) ** 2 + (m_y - y_ref) ** 2 + (m_z - z_ref) ** 2)
        fid = np.sqrt(np.std(self.liste_Xlamb)**2 + np.std(self.liste_Ylamb)**2 + np.std(self.liste_alt)**2)
        prec = np.sqrt(biais ** 2 + fid ** 2)

        # affichage
        print("- "*20)
        print("######### Mesures de la précision ########")
        print('biais : ', biais, ' m')  # Justesse
        print('Fidélité : ', fid, 'm')
        print('Précision : ', prec, 'm')
        print("- "*20)

        # Affichage
        plt.figure()
        plt.title("Mesures statistiques horizontales")

        plt.plot(x_ref, y_ref, "or", label='réference')
        plt.plot(m_x, m_y, 'og', label='moyenne')
        plt.plot(self.liste_Xlamb, self.liste_Ylamb, '+b', label='mesures')
        plt.legend()
        plt.show()

        n = len(self.liste_alt)
        absc = range(n)
        plt.figure()
        plt.title('Mesures statistiques verticales')
        plt.plot(absc, m_z*np.ones(n), 'r', label="moyenne")
        plt.plot(absc, z_ref*np.ones(n), 'g', label='référence')
        plt.plot(absc, (m_z - np.std(self.liste_alt))*np.ones(n), '--r', label="moy - std")
        plt.plot(absc, (m_z + np.std(self.liste_alt)) * np.ones(n), '--r', label="moy + std")
        plt.plot(absc, self.liste_alt, '+b', label="mesures")
        plt.legend()
        plt.show()


class Satellite:
    """
    Classe satellite utilisée dans la classe GPGSV.
    """
    def __init__(self, id, const, azimut, elevation, signal):
        self.id = id
        self.const = self.constellation(const)
        self.azimut = azimut
        self.elevation = elevation
        self.coords = self.coords_polaires(self.azimut, self.elevation)
        self.signal = [signal]

    def __str__(self):
        return "id :{} \n const:{} \n azimut:{} \n élévation:{}".format(self.id, self.const, self.azimut, self.elevation)


    def coords_polaires(self, az, el):
        """
        :param az: azimut
        :param el: élévation
        :return: (r, theta) Coordonées polaires du satellite par rapport au capteur
        """
        r = np.cos(np.radians(el))
        theta = -np.radians(az)
        return r, theta

    def constellation(self, const):
        if "GPG" in const:
            return 'GPS'
        elif "GLG" in const:
            return 'GLONASS'
        elif "BDG" in const:
            return 'BEIDOU'
        elif "GAG" in const:
            return 'GALLILEO'
        else:
            print('Erreur sattellite constellation non reconnue', const)

    def add_signal(self, signal):
        """
        Méthode permettant d'ajouter une valeur à la liste de force du signal du satellite
        """
        self.signal.append(signal)



class GSV:
    """
    Classe correspondant au traitement des données NMEA GPGSV.
    """

    def __init__(self, file_name):
        self.GSV = self.lecture(file_name)
        self.nb_satellites = int(self.GSV[0][3])
        self.nb_tramesGSV = int(self.GSV[0][1])
        self.sat_GPS = []
        self.sat_GALLILEO = []
        self.sat_GLONASS = []
        self.sat_BEIDOU = []
        self.liste_satellites()



    def lecture(self, file_name):
        """
        Lecture du fichier pour extraire les données GSV
        :param file_name: Nom du fichier
        :return: Liste de trames GPGSV
        """

        file = open(file_name, "r")
        lignes = file.readlines()
        all_GSV = []
        GSV = []
        for ligne in lignes:
            if '$GPGSV' in ligne or '$GLGSV' in ligne or '$BDGSV' in ligne or '$GAGSV' in ligne:
                all_GSV.append(ligne)

        # Pour éviter la redondance dans les trames
        for trame in all_GSV:
            if trame not in GSV:
                GSV.append(trame.split(','))
        return GSV

    def liste_satellites(self):
        """
        :return: liste des satellites visibles
        """
        liste_sat = []
        for i in range(len(self.GSV)):
            try:
                trame = self.GSV[i]
                trame[-1] = trame[-1][0:-4]  # on retire les caractères de checksum
                nb_sat = len(trame) // 4 - 1
                const = trame[0]
                for j in range(nb_sat):
                    id = int(trame[4 + j*4])
                    el = float(trame[5 + j*4])
                    az = float(trame[6 + j*4])
                    si = float(trame[7 + j*4])

                    if (const, id) not in liste_sat:  # on évite de prendre plusieurs fois le même satellite
                        liste_sat.append((const, id))
                        sat = Satellite(id, const, az, el, si)

                        if sat.const == 'GPS':
                            self.sat_GPS.append(sat)

                        elif sat.const == 'GALLILEO':
                            self.sat_GALLILEO.append(sat)

                        elif sat.const == 'GLONASS':
                            self.sat_GLONASS.append(sat)

                        elif sat.const == 'BEIDOU':
                            self.sat_BEIDOU.append(sat)
                    elif si < 80:
                        for s in self.sat_GPS:
                            if s.id == id:
                                sat = s
                                break
                        sat.add_signal(si)
            except Exception:
                print("pb sat")




    def affichage(self):
        """
        Affiche en coordonnées polaires les positions des satellites visibles.
        :return:
        """

        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        listes_gnss = [self.sat_GPS, self.sat_GALLILEO, self.sat_GLONASS, self.sat_BEIDOU]
        couleurs = ['r', 'b', 'g', 'y']
        noms = ['GPS', 'GALLILEO', 'GLONASS', 'BEIDOU']

        for i in range(len(listes_gnss)):
            r = []
            theta = []
            for sat in listes_gnss[i]:
                coords = sat.coords
                r.append(coords[0])
                theta.append(coords[1])
            ax.plot(theta, r, 'o', color=couleurs[i], label=noms[i])



        ax.set_rticks([0, 0.5, 1, 1.5])
        ax.legend()
        ax.set_title("Vue du ciel des satellites visibles", va='bottom')

        #affichage de la force du signal
        plt.figure()
        plt.title("Evolution de la force du signal des satellite")
        plt.ylabel("Rapport Signal à Bruit")
        for sat in self.sat_GPS:
            plt.plot(range(len(sat.signal)), sat.signal)
        #plt.xlim([3000, 4000])
        plt.show()



if __name__ == '__main__':




    data = "..\\files\\tour_terrain.txt"
    image = "..\\images\\ensta_2015_3_.tif"
    #  ###  Données GPGGA   ###

    gpgga = GPGGA(data, image)

    # affichage

    gpgga.affichage()
    #gpgga.aff_V2()



    # Données GPGSV

    gpgsv = GSV(data)
    gpgsv.affichage()

    # Calculs de précision
    #stats = GPGGA(data, image)  # mesures avec le GSTAR

    #stats.test_statistiques(ref='EB06')

    stats = GPGGA("..\\files\\mesures_stat\\UE24_SP80_20210602_EB06.txt", image)
    stats.test_statistiques(ref='EB06')

    #affichage en direct

    with open("../files/mesure_continue.txt", "w") as f:
        indi = 0
        gps = serial.Serial('COM3', 4800, timeout=1)
        gpgga_direct = GPGGA('..\\files\\test.txt', image)
        gpgga_direct.aff_V3_init()
        while True:
            try:
                s = gps.readline().decode('ascii')[:-2]
                gpgga_direct.aff_V3_add(s)
                #print(s)
                #print(indi)
                f.write(s + "\n")
                indi += 1
                if "GSV" in s:
                    f.write(s + "\n")
            except Exception:
                print("pb réception")
