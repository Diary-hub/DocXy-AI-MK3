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

cap = ""

cap = cv2.imread("/path_to_image/opencv-logo.png", 0)


success, img = cap.read()
imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
facesCurFr = face_recognition.face_locations(imgS)
encodecurFr = face_recognition.face_encodings(imgS, facesCurFr)
for encodeFace, faceLok in zip(encodecurFr, facesCurFr):
    mathes = face_recognition.compare_faces(encodeListKnown, encodeFace)
    faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
    # print(faceDis)
    matchIndex = np.argmin(faceDis)
    if mathes[matchIndex]:
        name = classNames[matchIndex].upper()
        print(name)
    else:
        print("Nainasm")
cv2.imshow("Webcam", img)
cv2.waitKey(1)
