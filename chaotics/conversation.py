#!/usr/bin/env python

#Class to use the espeak TTS engine with python
#Author: fito_segrera / http://fii.to

from subprocess import Popen, PIPE
class Conversation:

	def say(self, tosay):
		command =[ 
				'espeak', 
				"-f",
				"output.txt" 
		]

		Popen(command, stdin = PIPE, stdout = PIPE, stderr = PIPE, shell = False)

	def writeWav(self, tosay, agent):
		command =[ 
				'espeak', 
				"-w",
				 "audio/" + agent + ".wav",
				tosay
		]

		Popen(command, stdin = PIPE, stdout = PIPE, stderr = PIPE, shell = False)

	def playWav(self, agent):
		if agent == "A":
			command =[ 
					"play", 
					"audio/A.wav",
					"remix",
					"1",
					"0"
			]
		if agent == "B":
			command =[ 
					"play", 
					"audio/B.wav",
					"remix",
					"1",
					"0"
			]

		Popen(command, stdin = PIPE, stdout = PIPE, stderr = PIPE, shell = False)