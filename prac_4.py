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

# Define callback functions that are called when event occurs for push buttons
def reset_callback(RESET):
    #print("\nThe reset button was pressed. The timer has started")
    
    global start
    
    # Reset the timer
    start = time.time()

    # Clear the queue
    outerArray = [0,0,0,0,0]

    # Clear the console (by printing 50 blank lines)
    #print("\n" *50)

    # Clear the console using an os system call
    # A simple and cross-platform solution is to use either the 'cls' command on Windows, or 'clear' on Unix systems
    os.system('cls' if os.name == 'nt' else 'clear')
    #os.system('clear')

    # Print column header each time the console is cleared
    print('| {0:>4}     | {1:>4}    |{2:>4}   | {3:>4}  | {4:>4} |'.format(*col_header)) # Note that the spacing was adjusted so that it prints correctly


























