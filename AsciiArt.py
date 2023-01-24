import sys, random, argparse
import cv2
import numpy as np
import math
from PIL import Image

gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\^`'."
gscale2 = "@%#*+=-:.M"


def averageL(img):
    image = np.array(img)

    w, h = image.shape

    return np.average(image.reshape(w * h))


def convertIntoAscii(imageFile, colonnes, echelle, niveauxSup):
    global gscale1, gscale2

    image = Image.open(imageFile).convert('L')

    W, H = image.size[0], image.size[1]

    w = W / colonnes
    h = w / echelle
    rows = int(H / h)

    aimg = []

    for i in range(rows):
        y1 = int(i * h)
        y2 = int((i + 1) * h)

        if i == rows - 1:
            y2 = H

        aimg.append("")

        for j in range(colonnes):

            x1 = int(j * w)
            x2 = int((j + 1) * w)

            if j == colonnes - 1:
                x2 = W

            img = image.crop((x1, y1, x2, y2))

            avg = int(averageL(img))

            if niveauxSup:
                gsval = gscale1[int((avg * 68) / 255)]
            else:
                gsval = gscale2[int((avg * 8) / 255)]

            aimg[i] += gsval
    return aimg


def main():
    descStr = "make ascii art"
    parser = argparse.ArgumentParser(description=descStr)

    parser.add_argument('--file', dest='imgFile', required=False)
    parser.add_argument('--echelle', dest='echelle', required=False)
    parser.add_argument('--colonnes', dest='colonnes', required=False)
    parser.add_argument('--niveauxSup', dest='niveauxSups', action='store_true')

    # parse args
    args = parser.parse_args()

    imgFile = args.imgFile

    echelle = 0.40
    if args.echelle:
        echelle = float(args.echelle)

    colonnes = 250
    if args.colonnes:
        colonnes = int(args.colonnes)

    aimg = convertIntoAscii("images/image3.jpg", colonnes, echelle, args.niveauxSups)

    for row in aimg:
        print(row + '\n')


main()
