import matplotlib.pyplot as plt
plt.figure()
plt.title('test figures interactive')
plt.ion()
img = plt.imread('..\\images\\ensta_2015.jpg')
plt.imshow(img)

for i in range(100):
    plt.plot(i, 3*i, 'ob')
    plt.pause(0.5)
