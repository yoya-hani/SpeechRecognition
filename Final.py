#!/usr/bin/python3

import pyaudio
import wave
import os
import pathlib

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import tensorflow as tf

import socket

import time

#from tensorflow.keras import layers
#from tensorflow.keras import models


chunk = 372  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 16000  # Record at 44100 samples per second
seconds = 2.5
#filename = "output.wav"
filename = "C:/Users/Youssef/Downloads/output.wav"

p = pyaudio.PyAudio()  # Create an interface to PortAudio

print('start in 2')

time.sleep(1)

print('start in 1')

time.sleep(1)

print('Recording...')
stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

frames = []  # Initialize array to store frames

# Store data in chunks for 3 seconds
for i in range(0, int(fs / chunk * seconds)):
    data = stream.read(chunk)
    frames.append(data)

# Stop and close the stream 
stream.stop_stream()
stream.close()
# Terminate the PortAudio interface
p.terminate()

print('Finished recording')



# Save the recorded data as a WAV file
wf = wave.open(filename, 'wb')
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(fs)
wf.writeframes(b''.join(frames))
wf.close()
x = "C:/Users/Youssef/Downloads/output.wav"
x = tf.io.read_file(str(x))
x, sample_rate = tf.audio.decode_wav(x, desired_channels=1, desired_samples=16000,)
x = tf.squeeze(x, axis=-1)
waveform = x

#print('Hello 1')
imported = tf.saved_model.load("C:/Users/Youssef/Downloads/saved")
imported(waveform[tf.newaxis, :])
#print('Hello 2')
output_command = imported(tf.constant(str("C:/Users/Youssef/Downloads/output.wav")))
class_name_tensor = output_command['class_names']
#print('Hello 3')
class_name_string = class_name_tensor.numpy()[0].decode('utf-8')
print(class_name_string)




server = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
#mac address of the bluetooth
server.bind(("e0:2b:e9:13:4b:5a", 4))
#allow one connectionb at a time
server.listen(1)

client, addr = server.accept()

try:
    while True:
        #data = client.recv(1024)
        #if not data:
        #    break  
        #print(f"Message: {data.decode('utf-8')}")
        #message = input("Enter message:")
        client.send(class_name_string.encode('utf-8'))
except OSError as e:    
    pass

client.close()
server.close()

