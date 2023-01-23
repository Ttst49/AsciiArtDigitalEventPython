import sys, random, argparse
import numpy as banane
import math
from PIL import Image

gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\^`'."

gscale2 = "@%#*+=-:."


def averageL(img):

    image = banane.array(img)

    w, h = image.shape

    return banane.average(image.reshape(w*h))
