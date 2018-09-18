#!/usr/bin/python

"""Program for a simple environment monitor system.
The system includes a temperature sensor (MCP9700A), an LDR (1K), a pot (1K), an ADC (MCP3008 IC) and 4 push button switches"""

import RPi.GPIO as GPIO
import Adafruit_MCP3008
import spidev
import time
import os

# Open SPI bus - NB must have this. establishes the communication frequency
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000

GPIO.setwarnings(False)
# Set pin numbering as GPIO pin numbering
GPIO.setmode(GPIO.BCM)


# Define global variables
start = 0
end = 0
timer = 0
freqcount = 0
stopbtncount = 0
delay = 0.5         # The default frequency of montioring the sensors is 0.5s
monitor = True      # Monitor is set to True initially to establish the default state of the system such that as soon as the system is connected, it starts monitoring the sensors and printing the results
innerArray = [0,0,0,0,0]
outerArray = [0,0,0,0,0]

# Format column header
col_header = ["Time", "Timer", "Pot", "Temp", "Light"]



#------------------------------------------------------------------------------------------------------
# SPI pin definition using BCM pin numbering
CLK = 11
MISO = 9
MOSI = 10
CS = 8

# SPI pin setup
GPIO.setup(CLK, GPIO.OUT)
GPIO.setup(MISO, GPIO.IN)
GPIO.setup(MOSI, GPIO.OUT)
GPIO.setup(CS, GPIO.OUT)

# Set up MCP3008 ADC
mcp = Adafruit_MCP3008.MCP3008(clk = CLK,	miso = MISO,	mosi = MOSI,	cs = CS)

# Define sensor channels
light_channel = 0
temp_channel  = 1
pot_channel = 2

# Pushbutton definition using BCM pin numbering
RESET = 21
FREQUENCY = 20
STOP = 16
DISPLAY = 6

# Setup pushbuttons as GPIO digital inputs, in PULL-UP mode to avoid false detection (when pressed, pulls connection to ground)
GPIO.setup([RESET, FREQUENCY, STOP, DISPLAY], GPIO.IN, pull_up_down = GPIO.PUD_UP)

# The frequency switch changes the frequency of the monitoring. The possible
# frequencies are 500ms, 1s, 2s. The frequency must loop between those values per event occurrence
def frequency_callback(FREQUENCY):
    print("\nThe frequency button was pressed")
    
    global freqcount
    global delay
    
    freqcount += 1
    
    if(freqcount > 2): # Ensure that the counter does not exceed 3
        freqcount = 0

    # Cycle between the 3 frequency values
    if (freqcount == 0):
        delay = 0.5
    elif(freqcount == 1):
        delay = 1
    elif(freqcount == 2):
        delay = 2
    else:
        pass

    #print("The frequency button was pressed this many times: ", freqcount)
    print("The delay is currently set as this many seconds: ", delay)
    print("")
   
# The stop switch stops or starts the monitoring of the sensors - NB: by default, the system monitors the sensors so monitor = True
# The timer is not affected by this functionality   


def display_callback(DISPLAY):
    print("The display button was pressed\n")

    global outerArray
    
    for i in range(len(outerArray)):
        #print('| {0:>4} | {1:>4} | {2:>4}V | {3:>4}C | {4:>4}% |'.format(*outerArray[i]))
        # Find out from tutor why this method only prints the same thing (i.e the last element in outerArray) 5 times

        print(outerArray[i])
        

    print("")
    #time.sleep(0.2)