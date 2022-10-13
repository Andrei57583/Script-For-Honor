from cmath import isfinite
import numpy as np
from PIL import ImageGrab
import cv2
import matplotlib.pyplot as plt
import time
from IPython.display import Image
from DirectInputs import Right, Left, Up
from statistics import mean
from Interactiune import switch_guard,attack,parry


def ROI(img,vert):
    
    mask = np.zeros_like(img)
    cv2.fillPoly(mask,vert,255)
    masked = cv2.bitwise_and(img,mask)
    return masked


def draw(img,lin):
    try:
        for linie in lin:
            coord = linie[0]
            cv2.line(img,(coord[0],coord[1]),(coord[2],coord[3]),
                    [255,255,255],3)
    except:
        pass


def procesare_guard(imag):
    
    original = imag
    procesata = cv2.cvtColor(imag, cv2.COLOR_BGR2GRAY)
    
    vert = np.array([[601,360],[601,160],[735,160],[725,360]]) 
    procesata = ROI(procesata,[vert])
    
    _ , procesata = cv2.threshold(procesata, 155, 255, cv2.THRESH_BINARY)
    
    lines = cv2.HoughLinesP(procesata,rho=1 ,theta= np.pi/180,threshold= 17,minLineLength= 15,maxLineGap= 5 )
    
    gradients = []

    try:
        for linie in lines:
            actualLine = linie[0]
            gradient = (actualLine[3]-actualLine[1])/(actualLine[2]-actualLine[0])
            if isfinite(gradient):
                gradients.append(gradient)
    except:
        pass

    draw(procesata,lines)

    #print(gradients)
    return procesata,original,gradients


def procesare_attack(imag):
    LOW = np.array([0,234,74])
    HIGH = np.array([1,255,160])
    vertices = np.array([[510,500],[510,250],[780,250],[780,500]])

    HSV = cv2.cvtColor(imag, cv2.COLOR_RGB2HSV)
    #HSV = ROI(HSV,[vertices])
    mask = cv2.inRange(HSV,LOW, HIGH )

    whiteIMAGE = np.zeros_like(imag)
    whiteIMAGE[:] = 255
    locs = np.where(mask!=0)

    if len(imag.shape) == 3 and len(whiteIMAGE.shape) != 3:
        imag[locs[0], locs[1]] = whiteIMAGE[locs[0], locs[1],None]

    elif len(imag.shape) == 3 and len(whiteIMAGE.shape) == 3 or len(imag.shape) == 1 and len(whiteIMAGE.shape) == 1:
        imag[locs[0], locs[1]] = whiteIMAGE[locs[0], locs[1]]

    lines = cv2.HoughLinesP(mask,rho=1 ,theta= np.pi/180,threshold= 25,minLineLength= 50,maxLineGap= 5)

    slope = slopeAttack(lines)

    draw(mask,lines)

    return mask, locs, slope
    

def slopeAttack(lines):
    gradients2 = []

    try:
        for linie in lines:
            actualLine = linie[0]
            gradient = (actualLine[3]-actualLine[1])/(actualLine[2]-actualLine[0])
            if isfinite(gradient):
                gradients2.append(gradient)
    except:
        pass
    
    #print(gradients2)
    return gradients2


def find_guard(grad):

    avrg = int(mean(grad))
    #print(avrg)
    if avrg < -0.5: #Guard right
        return Left or Up

    elif avrg > -0.5 and avrg < 1: #Guard  up
        return Left or Right

    else: #Guard  Left
        return Right or Up


def find_attack(grad):
    avrg = int(mean(grad))

    #print(avrg)

    if avrg < -0.5: #Guard right
        return Right

    elif avrg > -0.5 and avrg < 1: #Guard  up
        return Up

    elif avrg: #Guard  Left
        return Left

# for i in list(range(4))[::-1]:
#     print(i+1)
#     time.sleep(1)

def runtime():
    while(True):
        printscreen = np.array(ImageGrab.grab(bbox=(0, 40, 1024, 768)))
        
        mask, locs, slope = procesare_attack(printscreen)
        guard,original,grad = procesare_guard(printscreen)        
        
        if grad:
            directie = find_guard(grad)
            attack(directie)
            print(directie)
        
        # if slope:
        #     directie2 = find_attack(slope)
        #     switch_guard(directie2)
            #parry(directie2)
            #print(directie2)

        #cv2.imshow('window guard',guard)
        cv2.imshow('window attack',mask)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

    # plt.imshow(printscreen,cmap='gray',interpolation='bicubic')
    # plt.show()


runtime()