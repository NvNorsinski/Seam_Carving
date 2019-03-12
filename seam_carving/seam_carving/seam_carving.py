import matplotlib.pyplot as plt
import imageio
import numpy as np
import tkinter as tk
from tkinter import *


class seamCarving:
    def __init__(self, image_path):
        self.__image = imageio.imread(image_path)
        self.original = self.__image
        #self.__image_shape = self.__image.shape
       # self.__energy_pic = np.zeros(shape=((self.__image_shape[0], self.__image_shape[1])), dtype=np.int)
        self.__energy_pic = self.__calcDiff(self.__image)
        self.cutImage = self.__searchSeam(self.__image, self.__energy_pic)


    def plot(self, image):
        # plt.figure('Bilder')
        # plt.imshow(image, cmap='gray')
        # plt.title('Normal')
        # plt.show()

        plt.figure('Bilder')
        plt.subplot(221)
        plt.imshow(image)
        plt.title('beschnitten')

        plt.subplot(222)
        plt.imshow(self.original)
        plt.title('Normal')

        plt.show()


    def deleteNSeams(self, n):
        for i in range(0, n):
            self.cutImage = self.__searchSeam(self.cutImage, self.__energy_pic)


    def __calcDiff(self, image):
        image_shape = image.shape

        # calculate difference along x axis
        diffx = np.diff(image, axis=1)
        # convert to larger datatype because of coming addition and squaring of entrys
        diffx = diffx.astype(np.uint32)
        diffx = diffx ** 2
        # sum for rgb
        diffx = np.sum(diffx, axis=2)

        # padding -> add colum for border handling
        difxr = image[:, image_shape[1] - 1] - image[:, 0]
        difxr = difxr.astype(np.uint32)
        difxr = np.sum(difxr, axis=1)
        difxr = difxr ** 2

        # reshape to change vector to matrix -> array([...]) to array([[...]])
        difxr = np.reshape(difxr, (1, image_shape[0]))
        energyX = np.concatenate((diffx, difxr.T), axis=1)

        # same thing for y-direction
        diffy = np.diff(image, axis=0)
        diffy = diffy.astype(np.uint32)
        diffy = diffy ** 2

        diffy = np.sum(diffy, axis=2)

        difyr = image[image_shape[0] - 1, :] - image[0, :]
        difyr = difyr.astype(np.uint32)
        difyr = np.sum(difyr, axis=1)
        difyr = difyr ** 2

        difyr = np.reshape(difyr, (1, image_shape[1]))
        energyY = np.concatenate((diffy, difyr), axis=0)

        energy = np.add(energyX, energyY)
        # normalize with maximum differenz 3 - channels, 2 - directions, **2 - eliminate sign  256^2 * 3 * 2 = 393216
        energy = (energy / 393216) * 255

        # convert to picture type
        energy = energy.astype(np.uint8)
        return energy


    def __searchSeam(self, image, energy_pic):
        image_shape = image.shape
        seamImage = np.zeros((image_shape[0], image_shape[1]), dtype=np.int)

        rows, cols = (image_shape[0], image_shape[1])

        # copy first row
        seamImage[:][0] = energy_pic[:][0]
        lowEnergyPath = []


        # claculate energy for each row
        for i in range(1, rows - 1):
            for j in range(1, cols - 2):
                seamImage[i][j] = energy_pic[i][j] + min(seamImage[i - 1][j - 1], seamImage[i - 1][j],
                                                            seamImage[i - 1][j + 1])

        # coordinate of point of lowest energy
        cordX = np.argmin(seamImage[:][rows-1])
        cordY = rows
        cordMin = cordX, cordY

        lowEnergyPath.append(cordMin)

        # coordinates of pixels to delete
        lowPixelCoord = []

        # add first lowest coordinates

        # backtrace
        for i in range(rows-1, -1, -1):
            # works like top statement in stack
            j, k = lowEnergyPath[-1]

            if j >=1 and j <= cols-2 and seamImage[i][j-1] <= seamImage[i][j] and \
                    seamImage[i][j-1] <= seamImage[i][j+1]:
                newX = j-1
            elif j >=1 and j <= cols-2 and seamImage[i][j] <= seamImage[i][j-1] and \
                    seamImage[i][j] <= seamImage[i][j+1]:
                newX = j
            elif j >=1 and j <= cols-2 and seamImage[i][j+1] <= seamImage[i][j] and\
                    seamImage[i][j+1] <= seamImage[i][j-1]:
                newX = j+1
            # in case of bordering pixels
            elif j < 1:
                if seamImage[i][j] <= seamImage[i][j+1]:
                    newX = j
                else:
                    newX = j+1
            elif j > cols-2:
                if seamImage[i][j] <= seamImage[i][j-1]:
                    newX = j
                else:
                    newX = j-1

            # turn coordinates into index of pixels to delete.
            # image will chanched to an 1 d array
            cordMin = newX, i

            # determine position of pixel to delete in flattened array
            posFlat = (i * cols) + newX
            lowPixelCoord.append(posFlat)

            lowEnergyPath.append(cordMin)

        # cut image
        splitImage = np.dsplit(image, 3)

        # cut energy matrix
        self.__energy_pic = np.delete(self.__energy_pic, lowPixelCoord)
        self.__energy_pic = np.reshape(self.__energy_pic, (rows, cols - 1))

        # delete pixels in every rgb channel and recombine these
        splitImage[0] = np.delete(splitImage[0], lowPixelCoord)
        splitImage[1] = np.delete(splitImage[1], lowPixelCoord)
        splitImage[2] = np.delete(splitImage[2], lowPixelCoord)

        for i in range(0, len(splitImage)):
            splitImage[i] = np.reshape(splitImage[i], (rows, cols - 1))

        cutImage = np.dstack((splitImage[0], splitImage[1]))
        cutImage = np.dstack((cutImage, splitImage[2]))
        return cutImage


# properties

picture_path = '20160728_144930.jpg'
picture_path = '20150521_115436.jpg'

P = seamCarving(picture_path)

P.deleteNSeams(50)
P.plot(P.cutImage)

#
# from PIL import Image, ImageTk
# plt.show()
# root = Tk()
# #root = tk.tk()
#
# img = ImageTk.PhotoImage(image=Image.fromarray(P.cutImage))
#
# panel = tk.Label(root, image = img)
# print(panel.winfo_height())
# panel.pack(side = "bottom", fill = "both", expand = "yes")
#
# print(panel.winfo_height())
# root.mainloop()

