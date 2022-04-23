import os
import cv2
import time
import numpy as np
import pywinauto
import pyautogui
import pygetwindow
from PIL import ImageGrab
from skimage.metrics import structural_similarity


path = r"C:/Users/username/Pictures/Captures"
title = "scrcpy"
savename = "Book Name"

os.startfile(path)

windows = pygetwindow.getWindowsWithTitle(title)[0]
margin = -10
x1 = windows.left - margin
y1 = windows.top + 31
x2 = windows.right + margin
y2 = windows.bottom + margin

if not windows.isActive:
    pywinauto.application.Application().connect(handle=windows._hWnd).top_window().set_focus()
    windows.activate()

def shot():
    img_crop = ImageGrab.grab([x1,y1,x2,y2])
    return img_crop


def save(img_crop, filename, uniq=0):
    file = os.path.join(path, filename+"_%s.jpg" % (uniq))
    while os.path.exists(file):
        uniq += 1
        file = os.path.join(path, filename+"_%s.jpg" % (uniq))

    img_crop.save(file)


def isLoading(before, img_crop):
    opencv_image = cv2.cvtColor(np.array(img_crop), cv2.COLOR_BGR2GRAY)
    before_opencv_image = cv2.cvtColor(np.array(before), cv2.COLOR_BGR2GRAY)
    if structural_similarity(before_opencv_image, opencv_image, full=True)[0] * 100 >= 99:
        return True
    # SM-P610 tablet
    opencv_image[505:549, 293:335] = 255
    opencv_image[625:629, 251:371] = 255
    opencv_image[1037:1053, 0:43] = 255
    opencv_image = cv2.bitwise_not(opencv_image)
    mask = cv2.inRange(opencv_image, np.array(1), np.array(3))
    opencv_image[mask>0] = 0
    loading = (cv2.countNonZero(opencv_image) == 0)
    # loading = (np.mean(opencv_image) < 0.1)
    # print(str(np.mean(opencv_image)) + ", " + str(loading))
    return loading
    

# ans = ""
# while ans == "":
#     ans = input("Enter to Shot. Write to Stop.")
time.sleep(1)
pywinauto.application.Application().connect(handle=windows._hWnd).top_window().set_focus()
uniq = 0
before = None
while True:
    before = shot()
    save(before, savename, uniq)
    # next button
    pyautogui.click(1200, 630)
    img_crop = ImageGrab.grab([x1,y1,x2,y2])
    while isLoading(before, img_crop):
        img_crop = ImageGrab.grab([x1,y1,x2,y2])
    uniq += 1
