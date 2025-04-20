import os
import cv2
from deepface import DeepFace
import numpy as np
from pygame import mixer
import pygame
import RPi.GPIO as GPIO
import time
# Initialize webcam and buttons
cap = cv2.VideoCapture(0)
images = []
GPIO.setmode(GPIO.BCM)
button1_pin = 17
button2_pin = 27
GPIO.setup(button1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Capture five images
for i in range(5):
    ret, frame = cap.read()
    if ret:
        images.append(frame)

cap.release()
cv2.destroyAllWindows()

# Analyze emotions
emotions = []
for img in images:
    result = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)
    emotions.append(result[0]['dominant_emotion'])

# Calculate the most common emotion
mixer.init()
mixer.music.set_volume(1.0)
def playsound(sound):
	mixer.music.load(sound)
	mixer.music.play()
	while mixer.music.get_busy():
		time.sleep(1)
most_common_emotion = max(set(emotions), key=emotions.count)
playsound('intro.mp3')
playsound(most_common_emotion + ".mp3")
playsound('main.mp3')

#This part of the code checks what emotion the user is showing so it knows whether it is able to help 
#them with the emotion if they want that. I encountered errors when using if and or so I had to use the long way. 
#The point is it works!

if most_common_emotion == 'angry':
	canihelp = 'Yes'
elif most_common_emotion == 'sad':
	canihelp = 'Yes'
elif most_common_emotion == 'fear':
        canihelp = 'Yes'
elif most_common_emotion == 'disgust':
        canihelp = 'Yes'
elif most_common_emotion == 'happy':
        canihelp = 'No'
elif most_common_emotion == 'neutral':
        canihelp = 'No'
elif most_common_emotion == 'suprise':
        canihelp = 'No'

# the code for the buttons
if canihelp == 'Yes':
	while True:
		if GPIO.input(button1_pin) == GPIO.LOW:
			musicorhelp = True
			break
		if GPIO.input(button2_pin) == GPIO.LOW:
			musicorhelp = False
			break
else:
	musicorhelp = True
#a function that makes playing all the music in a specified folder easy

def playmusicsound():
        sound_folder = ('/home/pi/newrobot/' + most_common_emotion + '_music')
        sound_files = [f for f in os.listdir(sound_folder) if f.endswith('.wav') or f.endswith('.mp3')]
        for sound_file in sound_files:
                sound_path = os.path.join(sound_folder, sound_file)
                pygame.mixer.music.load(sound_path)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                        time.sleep(1)

if musicorhelp == True:
#this is for if they want to listen to music
	playmusicsound()
else:
#this is for if they want to get help with what they are feeling. Once it helps it plays music.
	helpsound = (most_common_emotion + 'help.mp3')
	pygame.mixer.music.load(helpsound)
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy():
		time.sleep(1)
	pygame.mixer.music.load('/home/pi/newrobot/nowplaying.mp3')
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy():
		time.sleep(1)
	playmusicsound()
