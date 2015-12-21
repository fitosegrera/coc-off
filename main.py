#!/usr/bin/python

import RPi.GPIO as GPIO
from chaotics import conversation
from chaotics import noise
from markov import MarkovChain
import os
import sys
import time
import string
import random

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.output(23, False)

cycleLimit = 120
(rows, columns) = os.popen('stty size', 'r').read().split()

audio = noise.Noise()
voice = conversation.Conversation()

def run(agentName, useSound):
    if len(sys.argv) != 4:
        print "usage:"
        print "python main.py $ORDER $DATAFILE $OUTLENGTH"
        print "example:"
        print "python main.py 3 data.txt 300"
        sys.exit(1)
    
    order    = int(sys.argv[1])
    inputFile = sys.argv[2]
    length   = int(sys.argv[3])

    m = MarkovChain(order)
    m.observe_file(inputFile, True)
    start = m.get_random_prestate()
    result = m.random_walk_string(length, start)
    
    with open("texts/"+agentName+".txt", "w") as text_file:
        text_file.write(result)
    with open("texts/output.txt", "a") as text_file:
        text_file.write(agentName + ": " + result + "\n\n")

    if useSound:
        audio.alert(12, 0.2, 3000)
        for i in range(5):
            for i in string.split(result):
                print i
                rand = random.random() * (0.01 - 0.001) + 0.001
                audio.whitenoise(rand, random.randint(10, 50))
                time.sleep(0.05)

        points = ""
        for c in range(int(columns)):
            points += "."

        for i in range(10):
            print points
            audio.generate(5, 2)
            time.sleep(0.01)    

    printMsg('SPEAKING...')
    time.sleep(5)

    voice.writeWav(result, agentName)
    voice.playWav(agentName)
    printMsg(agentName + ": " + result)
    time.sleep(10)

def printMsg(msg):
    line = ''
    for c in range(int(columns) * int(rows) / 2):
        line += ' '
    print line
    half = int(columns) / 2
    print 
    halfLine = ''
    for i in range(half - int(len(msg)) / 2):
        halfLine += ' '
    print halfLine, msg
    print 
    line = ''
    for c in range(int(columns) * int(rows) / 2):
        line += ' '
    print line

def main():
    global cycleLimit
    printMsg('CHAOTIC CYCLE INITIATED...')
    GPIO.output(23, True)
    time.sleep(cycleLimit)
    print '\n'
    printMsg('RECEIVING DATA FROM AGENTS...')
    sinewave(3, 5000)
    time.sleep(5)
    GPIO.output(23, False)


while True:
    try:
        main()
        time.sleep(10)
        run("A", True)
        time.sleep(8)
        run("B", False)
        time.sleep(8)

    except KeyboardInterrupt:
        GPIO.output(23, False)
        exit(0)