#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
gpio-polling.py
Script for periodically polling a gpio pin and printing when it changes.

• usage:
usage: gpio_polling.py [-h] -p PIN [-T PERIOD] [-P PUD] [-i]

arguments:
  -h, --help            show this help message and exit
  -p PIN, --pin PIN     GPIO pin to poll
  -T PERIOD, --period PERIOD
                        polling period in seconds
  -P PUD, --pud PUD     set pin pull up/down. -1, 0, 1 for pull down, off, up.
  -i, --invert          invert output

• typical usage

• setup:
if running as daemon, edit gpio_pollingd to specific needs.
	make sure scripts have execute permissions.
sudo chmod 755 gpio-polling.py gpio-pollingd.sh
	copy scripts over to appropriate locations:
sudo cp gpio-polling.py /usr/local/bin/gpio-polling
sudo cp gpio-pollingd.sh /etc/init.d/gpio-pollingd
	register script at startup:
sudo update-rc.d gpio-pollingd defaults

	un-register script at startup:
sudo update-rc.d -f  gpio-pollingd remove  

• TODO:
-output file?
-format output?

• History
2015-09-14: created (Devon Fyson)

refs:
http://RasPi.tv/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio-part-3

# TODO:
# 

'''

import time
import datetime
import RPi.GPIO as GPIO
import sys
import argparse

#user variables
pin = 0 #pin to be used
invert = False #invert output
period = 10 #polling period in seconds
#number = 0 #number of polls. 0 is infinite. (Currently not impliments)
pud = 0 #pullup resistors. Either -1, 0, 1 for down, off, up.

#internal variables
stateOld = False #holds the last state of the pin.
i = 0 #iteration number

def args(): #parse arguments
	global pin
	global period
	global pud
	global invert

	parser = argparse.ArgumentParser(description = "Periodically poll a specified GPIO input and output whenever a change has been noticed.\nEach time program starts, the current state is printed along with 'start'.")
	parser.add_argument('-p', '--pin', help='GPIO pin to poll (required argument)', required=True)
	parser.add_argument('-T', '--period', help='polling period in seconds', default=10)
	parser.add_argument('-P', '--pud', help='set pin pull up/down. -1, 0, 1 for pull down, off, up.', default=0)
	parser.add_argument('-i', '--invert', help='invert output', action='store_true')

	args = parser.parse_args()
	if args.pin is not None:
		pin = int(args.pin)
	else:
		print >> sys.stderr, "No pin specified. Exiting."
		exit(1)
	period = float(args.period)
	pud = int(args.pud)
	if args.invert:
		invert = True

def main():
	global pin
	global period
	global pud
	global stateOld
	global i

	args()

	#print str(datetime.datetime.now())+"\tstart"
	#sys.stdout.flush() #won't flush buffer until process is killed (or maybe if buffer fills up) 
	#f = open('waterheater2.log', 'a')
	#f.write(str(datetime.datetime.now())+"\tstart\n")
	#f.flush()

	GPIO.setmode(GPIO.BCM) # tell the GPIO module that we want to use the chip's pin numbering scheme
	if pud == -1:
		pudp=GPIO.PUD_DOWN
	elif pud == 0:
		pudp=GPIO.PUD_OFF
	elif pud == 1:
		pudp=GPIO.PUD_UP
	else:
		print >> sys.stderr, "invalid pull-up/down state specified. Exiting."
		sys.exit(1)

	#Setup GPIO ports: internal pull up/down resistors.
	GPIO.setup(pin, GPIO.IN, pull_up_down=pudp)
	stateOld=False

	try:
		while True:
			poll()
			i += 1
			time.sleep(period)

	finally:
		GPIO.cleanup() # clean up GPIO on normal exit


def poll(): #callback?
	global pin
	global invert
	global stateOld #holds the last state of the pin.
	global invert
	global i
	stateNew = GPIO.input(pin) # = 1 if rising.
	start = ""
	if i == 0: #so no matter the state of the pin, it is output soon as the script starts up.
		stateOld = ~stateNew
		start = "\tstart"
	if stateNew != stateOld:
		print str(datetime.datetime.now())+"\t"+str(invert ^ stateNew)+start
		sys.stdout.flush()
		#f.write(str(datetime.datetime.now())+"\t"+str(stateNew)+"\n")
		#f.flush()
	stateOld = stateNew

if __name__ == "__main__":
	main()
