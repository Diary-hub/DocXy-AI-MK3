import cv2
import numpy as np
import face_recognition
import os

# Getting the Images
path = "Photo"
imgs = []
classNames = []
mList = os.listdir(path)

for cl in mList:
    curIMG = cv2.imread(f"{path}/{cl}")
    imgs.append(curIMG)
    classNames.append(os.path.splitext(cl)[0])

# print(classNames)


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


encodeListKnown = findEncodings(imgs)
print("Encoding Complete")
