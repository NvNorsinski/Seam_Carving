# Author Nils von Norsinski

import matplotlib.pyplot as plt
import imageio
import numpy as np
import scipy.misc
import sys
from pathlib import Path


class Seam_carving:
    """
    This class implements seam carving, described by Shai Adivan et al. 2007.
    It calculates an energy matrix to find path of lowest importance and delete those pixels using dynamic programming.

    Parameters
    ----------
    image_path: str
        Path to image

    Attributes
    ----------
    __image : ndarray
        image read from given path
    energyPic : ndarray
        energy matrix
    cutImage : ndarray
        cuttet image
    seamImage : ndarray
        Image to plot the seam image

    Methods
    -------
    plot()
        plot given image and original.
    deleteNSeams()
        delete given number of seams. Works only colum wise.
    calcDiff()
        calculate energy matrix
    searchSeam()
        searches seam to delete

    """

    def __init__(self, image_path):
        """
        Parameters
        ----------
        image_path : str
            Path to image
        """
        self.__image = imageio.imread(image_path)
        # could be private but was set to public to use class own plot method to show the image
        self.energyPic = self.__calcDiff(self.__image)
        self.cutImage = self.__searchSeam(self.__image, self.energyPic)

        # This variable will hold the seam image to plot it
        self.seamImage = np.zeros(self.__image.shape)

    def plot(self, image):
        """
        Plot a given image in comparison to originall image.

        Parameters
        ----------
        image : numpy.ndarray
            image to plot

        Returns
        -------
        None
        """

        plt.figure('Bilder')
        plt.subplot(221)
        plt.imshow(image, cmap='gray')
        plt.title('beschnitten')

        plt.subplot(222)
        plt.imshow(self.__image)
        plt.title('Normal')

        plt.show()

    def deleteNSeams(self, n):
        """
        Delete n seams from original, write result to disk and call plot.

        Parameters
        ----------
        n : int
            How many seams should be removed?

        Returns
        -------
        None
        """

        for _ in range(1, n-1):
            self.cutImage = self.__searchSeam(self.cutImage, self.energyPic)
        # write result to disk
        picture_path = Path.cwd()
        picture_path = picture_path.parent
        picture_path = picture_path / 'images/output/out.jpg'

        scipy.misc.imsave(picture_path, self.cutImage)
        self.plot(self.cutImage)

    def __calcDiff(self, image):
        """
        Calculate energy matrix for given image

        Parameters
        ----------
        image : ndarray
            image from which the energy matrix will be calculated.

        Returns
        -------
        ndarray
            Returns energy matrix

        """
        image_shape = image.shape

        # calculate difference along x axis
        diffx = np.diff(image, axis=1)
        # convert to larger datatype because of coming addition and squaring of entrys
        diffx = diffx.astype(np.uint32)
        diffx = diffx ** 2
        diffx = np.sum(diffx, axis=2)
        # sum for rgb

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
        diffy = np.sum(diffy, axis=2)
        diffy = diffy ** 2

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
        """
        Search the seam to delete, by caluclating the lowest energy path for each colum and then backtrace from pixel
        with lowest energy.
        Parameters
        ----------
        image :ndarray
            image from which the seam will be removed
        energy_pic : ndarray
            The energy matrix

        Returns
        -------
        ndarray
            Returns the cutet image

        """

        image_shape = image.shape
        seamImage = np.zeros((image_shape[0], image_shape[1]), dtype=np.int)

        rows, cols = (image_shape[0], image_shape[1])

        # copy first row
        seamImage[:][0] = energy_pic[:][0]

        lowEnergyPath = []

        # claculate energy for each row
        for i in range(1, rows):
            for j in range(0, cols):
                if j == 0:
                    seamImage[i][j] = energy_pic[i][j] + min(seamImage[i - 1][j], seamImage[i-1][j+1])
                elif j == cols-1:
                    seamImage[i][j] = energy_pic[i][j] + min(seamImage[i - 1][j], seamImage[i - 1][j - 1])
                else:
                    seamImage[i][j] = energy_pic[i][j] + min(seamImage[i - 1][j - 1], seamImage[i - 1][j],
                                                                seamImage[i - 1][j + 1])

        # coordinate of point of lowest energy
        cordX = np.argmin(seamImage[:][rows-1])
        cordY = rows
        cordMin = cordX, cordY

        lowEnergyPath.append(cordMin)

        # coordinates of pixels to delete
        lowPixelCoord = []

        # store seam image in class variable. This is only necessary to plot the seam image
        self.seamImage = seamImage

        # backtrace
        for i in range(rows-1, -1, -1):
            # works like top statement in stack
            j, _ = lowEnergyPath[-1]
            # check borders and which pixel has smallest value
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
            # faltten to delete
            lowPixelCoord.append(posFlat)

            lowEnergyPath.append(cordMin)

        # cut image
        splitImage = np.dsplit(image, 3)

        # cut energy matrix
        self.energyPic = np.delete(self.energyPic, lowPixelCoord)
        self.energyPic = np.reshape(self.energyPic, (rows, cols - 1))

        # delete pixels in every rgb channel and recombine these.
        for i in range(0, 3):
            splitImage[i] = np.delete(splitImage[i], lowPixelCoord)
            splitImage[i] = np.reshape(splitImage[i], (rows, cols - 1))

        cutImage = np.dstack((splitImage[0], splitImage[1]))
        cutImage = np.dstack((cutImage, splitImage[2]))

        return cutImage


# ---------------------------------------------------------------------------------
def test():

    image = '20150521_115436.jpg'
    # picture_path = input("Path and name of image: ")

   # image: str = 'Unbenannt.png'
    picture_path = Path.cwd()
    picture_path = picture_path.parent
    picture_path = picture_path / 'images/input' / image


    numberSeams: int = 5

    # numberSeams = int(input("Enter number of Seams to delete: "))


    P = Seam_carving(picture_path)
    P.deleteNSeams(numberSeams)
    P.plot(P.energyPic)
    P.plot(P.seamImage)
    #P.plot(P.cutImage)

# ---------------------------------------------------------------------

if __name__ == '__main__': test()

#----------------------------------------------------------------------
