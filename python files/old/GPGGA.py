import matplotlib.pyplot as plt
from pyproj import Proj, transform
import matplotlib.image as img

#######Lecture des données

fich=open("../../files/test_acquisition_gps.txt", "r")
lignes=fich.readlines()
GPA=[]
GSV=[]
for ligne in lignes:
    if '$GPGGA' in ligne:
        GPA.append(ligne)
    if '$GPGSV' in ligne :
        GSV.append(ligne)

print(GSV)


#######traitement de coordonnées

liste_lat=[]
liste_long=[]

liste_Xlamb=[]
liste_Ylamb=[]


def deg_to_Lamb (x1,y1):
    outProj = Proj(init='epsg:2154')
    inProj = Proj(init='epsg:4326')
    x2,y2 = transform(inProj,outProj,x1,y1)
    return x2,y2

for mesure in GPA:
    mes = mesure.split(",")[2:6]
    if mes[1]=='N':
        liste_long.append(float(mes[0][0:2]) + (float(mes[0][2:]))/60)
    else:
        liste_long.append(-float(mes[0][0:2])- (float(mes[0][2:]))/60)
    if mes[3]=='E':
        liste_lat.append(float(mes[2][0:3])+ (float(mes[2][3:]))/60)
    else:
        liste_lat.append(-float(mes[2][0:3])- (float(mes[2][3:]))/60)

for i in range (len(liste_lat)):
    X,Y=deg_to_Lamb(liste_lat[i],liste_long[i])
    liste_Xlamb.append(X)
    liste_Ylamb.append(Y)

#######Conversion

E1, N1 = 147788.609, 6839279.724
E2, N2 = 147787.422, 6839274.663


#x=alpha*E +beta*N + ct1
alpha = 0.622672164
beta = -0.093309478
ct1=546305.0875

#y=gamma*E +delta*N + ct2
gamma =-0.046338701
delta =-0.620534551
cte2 =4251139.032

def conversion_pour_image(E,N):
    x = alpha * E + beta * N +ct1
    y = gamma * E + delta * N + cte2
    return x, y

# print(conversion_pour_image(147788.609,6839279.724))

liste_X_image=[]
liste_Y_image=[]

for i in range(len(liste_Xlamb)):
    X, Y = conversion_pour_image(liste_Xlamb[i],liste_Ylamb[i])
    liste_X_image.append(X)
    liste_Y_image.append(Y)

print(liste_lat[2],liste_long[2])
print(liste_Xlamb[-1],liste_Ylamb[-1])
print(deg_to_Lamb(-4.473138,48.41815833))
print(conversion_pour_image((147787.422+147788.609)/2, (6839279.724+6839274.663)/2))

image = img.imread('..\\images\\background.png')
plt.imshow(image)
x1, y1 = conversion_pour_image(147788.609, 6839279.724)
x2, y2 = conversion_pour_image(147787.422, 6839274.663)
plt.plot(x1,y1,"+r")
plt.plot(x2,y2,"+r")
x3,y3=conversion_pour_image((147787.422+147788.609)/2, (6839279.724+6839274.663)/2)
plt.plot(x3,y3,"+g")
for i in range (len(liste_Y_image)):
    plt.plot(liste_X_image[i],liste_Y_image[i],"+b")
plt.show()
