import cv2
import mediapipe as mp
import SquatPosture as sp
import pandas as pd
import numpy as np
import tensorflow as tf
from utils import *
from csv import writer
import serial
import os, time
port = serial.Serial("COM3", baudrate=9600, timeout=1)
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# df = pd.DataFrame([ , columns=['neck', 'knee', 'hip', 'ankle', 'y-knee'])
# df.to_csv('plot_data.csv', index=False)

dict = {'neck': [],
        'knee': [],
        'hip': [],
        'ankle': [],
        'y-knee': []
        }



# For video input:
cap = cv2.VideoCapture(0)

model = tf.keras.models.load_model("working_model_1")
counter_for_renewal = 0
with mp_pose.Pose() as pose:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            # continue
            break

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        results = pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        params = sp.get_params(results)

        if params is None:
            print("NO HUMAN!")
            continue

        flat_params = np.reshape(params, (5, 1))

        # if counter_for_renewal > 100:
        # csv_file.truncate(1)
        if len((dict['neck'])) > 10:
            dict['neck'].pop(0)
            dict['knee'].pop(0)
            dict['hip'].pop(0)
            dict['ankle'].pop(0)
            dict['y-knee'].pop(0)
        else:
            dict['neck'].append(flat_params.flatten().T[0])
            dict['knee'].append(flat_params.flatten().T[1])
            dict['hip'].append(flat_params.flatten().T[2])
            dict['ankle'].append(flat_params.flatten().T[3])
            dict['y-knee'].append(flat_params.flatten().T[3])

        df = pd.DataFrame.from_dict(dict)
        df.to_csv('visual_plotting.csv', index=False)

        counter_for_renewal += 1
        #print(flat_params)

        output = model.predict(flat_params.T)

        output[0][2] *= 5
        output[0][4] *= 3

        output = output * (1 / np.sum(output))

        output_name = ['c', 'k', 'h', 'r', 'x', 'i']

        label = ""

        for i in range(1, 4):
            label += output_name[i] if output[0][i] > 0.4 else ""

        if label == "":
            label = "c"

        label += 'x' if output[0][4] > 0.09 else ''

        #print(label, output)
        #print(output)

        print(output[0])
        #print(output[i])

        label_final_results(image, label)

        cv2.imshow('MediaPipe Pose', image)

        time.sleep(2)
        file = open('geek.txt','w')
        z=(output[0])
        z=str(z)
        file.write(z)
        #file.write("It allows us to write in a particular file")
        file.close()
        file = open("geek.txt", "r")
        y=(file.read(1))
        y=(file.read(4))
        #y=(file.read(5))
        print(y)
        file.close()
        if(y==("0.90")):
         print("head pain")
         port.write(b'A\r')
         rcv = port.read(10)
         print(rcv)
         time.sleep(1)
         port.write(b"AT+CMGF=1\r")
         print("text Mode Enabled…")
         time.sleep(3)
         port.write(b'AT+CMGS="7499221456"\r')
         msg = "headpain detected need help"
         print("sending message….")
         time.sleep(3)
         port.reset_output_buffer()
         time.sleep(1)
         port.write(str.encode(msg+chr(26)))
         time.sleep(30)
         print("message sent…")
        if(y==("0.82")):
         print("shoulder pain")
         port.write(b'A\r')
         rcv = port.read(10)
         print(rcv)
         time.sleep(1)
         port.write(b"AT+CMGF=1\r")
         print("text Mode Enabled…")
         time.sleep(3)
         port.write(b'AT+CMGS="7499221456"\r')
         msg = "sholder-pain detected need help"
         print("sending message….")
         time.sleep(3)
         port.reset_output_buffer()
         time.sleep(1)
         port.write(str.encode(msg+chr(26)))
         time.sleep(30)
         print("message sent…")
        if(y==("0.85")):
         print("cough pain")
         port.write(b'A\r')
         rcv = port.read(10)
         print(rcv)
         time.sleep(1)
         port.write(b"AT+CMGF=1\r")
         print("text Mode Enabled…")
         time.sleep(3)
         port.write(b'AT+CMGS="7499221456"\r')
         msg = "cough detected need help"
         print("sending message….")
         time.sleep(3)
         port.reset_output_buffer()
         time.sleep(1)
         port.write(str.encode(msg+chr(26)))
         time.sleep(30)
         print("message sent…")
        if(y==("0.87")):
         print("heart pain")
         port.write(b'A\r')
         rcv = port.read(10)
         print(rcv)
         time.sleep(1)
         port.write(b"AT+CMGF=1\r")
         print("text Mode Enabled…")
         time.sleep(3)
         port.write(b'AT+CMGS="7499221456"\r')
         msg = "heart-pain detected need help"
         print("sending message….")
         time.sleep(3)
         port.reset_output_buffer()
         time.sleep(1)
         port.write(str.encode(msg+chr(26)))
         time.sleep(30)
         print("message sent…")
         

        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
cv2.destroyAllWindows()
