import argparse
import cv2
import numpy as np
from PIL import Image
from PIL import ImageDraw

gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\^`'."
gscale2 = "@%#*+=-:.M"


def averageL(img):
    image = np.array(img)

    w, h = image.shape

    return np.average(image.reshape(w * h))


def picture():
    global image

    cam = cv2.VideoCapture(0)

    cv2.namedWindow("test")

    img_counter = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("Prendre une photo", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            # SPACE pressed
            img_name = "images/opencv_frame_{}.png".format(img_counter)
            image = "images/opencv_frame_{}.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1

    cam.release()

    cv2.destroyAllWindows()

    return image


def convertIntoAscii(imgFile, colonnes, echelle, niveauxSup):
    global gscale1, gscale2

    imgFile = picture()

    image = Image.open(imgFile).convert('L')

    width, height = image.size

    left = width / 2 - 300
    bottom = height * 0.85
    right = width / 2 + 300
    top = height * 0.10

    image = image.crop((left, top, right, bottom))

    W, H = image.size[0], image.size[1]
    print(image.size[0], image.size[1])

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


def boucleImage(liste, file, banane=""):
    for row in liste:
        file.write(row + "\n")
    print(banane)
    return banane


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

    echelle = 0.50
    if args.echelle:
        echelle = float(args.echelle)

    colonnes = 150
    if args.colonnes:
        colonnes = int(args.colonnes)

    aimg = convertIntoAscii(imgFile, colonnes, echelle, args.niveauxSups)

    # base = Image.open("images/baseAsciiVideNew.png")
    # base = Image.open("images/testVide.svg")
    base = open("ascii.txt", "w+")

    base = boucleImage(aimg, base)

    # base.save("images/baseAsciiNew.png")
    # base.save("images/test.svg")

    template = Image.open("images/template.jpg")

    I1 = ImageDraw.Draw(template)

    listAscii = ''

    with open('ascii.txt') as base:
        while True:
            line = base.readline()
            if not line:
                break
            listAscii += line.strip() + "\n"

    I1.text((0, 0), listAscii, fill=(0, 0, 0))

    print(listAscii)

    template.show()


main()
