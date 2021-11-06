import cv2
import numpy as np

def afinamentoZhang(img):
    resultado = img.copy()
    
    flag = True
    while flag:
        flag = False
        pixels = []

        passo1(resultado, pixels)
        if len(pixels) > 0:
            flag = True
            remover_pixels(resultado, pixels)
        passo2(resultado, pixels)
        if len(pixels) > 0:
            flag = True
            remover_pixels(resultado, pixels)
    return resultado


def passo1(img, pixels):
    row, col = img.shape
    for r in range(1, row-1):
        for c in range(1, col-1):
            v = definir_vizinhos(img, r, c)
            vizinhos_preto = (int(v["P2"]) + int(v["P3"]) + int(v["P4"]) + int(v["P5"]) +
                              int(v["P6"]) + int(v["P7"]) + int(v["P8"]) + int(v["P9"]))
            if (img[r][c] == 0  and 
                2*255 <= vizinhos_preto <= 6*255 and 
                conectividade(v) == 1 and 
                int(v["P2"])+int(v["P4"])+int(v["P8"]) >= 255 and 
                int(v["P2"])+int(v["P6"])+int(v["P8"]) >= 255
                ):
                pixels.append((r,c))


def passo2(img, pixels):
    row, col = img.shape
    for r in range(1, row-1):
        for c in range(1, col-1):
            v = definir_vizinhos(img, r, c)
            vizinhos_preto = (int(v["P2"]) + int(v["P3"]) + int(v["P4"]) + int(v["P5"])
                            + int(v["P6"]) + int(v["P7"]) + int(v["P8"]) + int(v["P9"]))
            if (img[r][c] == 0 and  2*255 <= vizinhos_preto <= 6*255 and
                conectividade(v) == 1 and
                int(v["P2"])+int(v["P4"])+int(v["P6"]) >= 255 and 
                int(v["P4"])+int(v["P6"])+int(v["P8"]) >= 255
                ):
                pixels.append((r,c))

def definir_vizinhos(img, r, c):
    return {
        "P2": img[r-1][c], "P3": img[r-1][c+1],
        "P4": img[r][c+1], "P5": img[r+1][c+1],
        "P6": img[r+1][c], "P7": img[r+1][c-1],
        "P8": img[r][c-1], "P9": img[r-1][c-1]
    }


def conectividade(v):
    count = 0

    for i in range(2, len(v)+1):
        if v["P"+str(+i)] == 255 and v["P"+str(+i+1)] == 0:
            count += 1
    if v["P9"] == 255 and v["P2"] == 0:
        count += 1

    return count



def remover_pixels(img, pixels):
    for r,c in pixels:
        img[r][c] = 255
    pixels = []
    return img


def main():
    img = cv2.imread("letraforma.jpeg")
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    (thresh, img_bw) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    img_afinada = afinamentoZhang(img_bw)
    cv2.imshow("", img_afinada)
    cv2.imwrite("resultado-afinamento.jpeg", img_afinada)
    cv2.waitKey(0)


if __name__ == "__main__":
    main()