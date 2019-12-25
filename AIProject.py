import cv2
from face_recognition import *
import PIL.Image
import time
import numpy as np
import threading
import os


def camera():
    global dic
    global counter
    camera = cv2.VideoCapture(0)
    cv2.namedWindow('MyCamera')
    ctime = time.time()
    while True:
        success, frame = camera.read()
        if time.time() - ctime > 0.8:
            ctime = time.time()
            locations = face_locations(frame)
            faces = face_encodings(frame)
            for i in range(0, len(locations)):
                location = locations[i]
                cv2.rectangle(frame, (location[3], location[0]), (location[1], location[2]), (255, 255, 255))
                have_same = False
                for key in dic:
                    if compare_faces([faces[i]], dic[key],tolerance=0.4)[0]:
                        # print('existed face',str(key))
                        cv2.putText(frame, str(key), (location[1], location[2]), font, font_scale, (255, 255, 255))
                        have_same = True
                        break
                if not have_same:
                    counter += 1
                    # print('new face!')
                    dic[str(counter)] = faces[i]
                    # print(dic)
                    cv2.putText(frame, str(counter), (location[1], location[2]), font, font_scale, (255, 255, 255))
        else:
            locations = face_locations(frame)
            faces = face_encodings(frame)
            for i in range(0, len(locations)):
                location = locations[i]
                cv2.rectangle(frame, (location[3], location[0]), (location[1], location[2]), (255, 255, 255))
        cv2.imshow('MyCamera', frame)
        if cv2.waitKey(1) & 0xff == ord(' '):
            break
    cv2.destroyWindow('MyCamera')
    camera.release()


def readKey():
    while True:
        i = input()
        global dic
        if ':' in list(i):
            old = i.split(':')[0]
            new = i.split(':')[1]
            if old in dic.keys():
                dic[new]=dic[old]
                dic.pop(old)
            file = open('data', 'r+')
            file.read()
            kv=new+':'+str(dic[new])
            # kv.replace('\n','')
            # kv.replace('\r','')
            file.writelines(kv)
            file.writelines('***')
            file.close()

def readData(path):
    global dic
    file = open(path, 'r+')
    data = file.read()
    data = data.split('***')
    print(data)
    for d in data:
        if d != '' and d != '\n':
            d = d.split(':')
            key = d[0]
            value = []
            d[1] = d[1].strip('[')
            d[1] = d[1].strip(']')
            d[1].replace('\n', '')
            d[1] = d[1].split(' ')
            for i in d[1]:
                if i != '':
                    i = float(i)
                    value.append(i)
            value=np.array(value)
            dic[key] = value


dic = {}
readData('data')
counter=0
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 2
task1 = threading.Thread(target=camera)
task2 = threading.Thread(target=readKey)
task1.start()
task2.start()
