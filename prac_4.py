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

# The stop switch stops or starts the monitoring of the sensors - NB: by default, the system monitors the sensors so monitor = True
# The timer is not affected by this functionality    
def stop_callback(STOP):
    print("\nThe stop button was pressed")
    
    global stopbtncount
    global monitor
    
    stopbtncount +=1
    
    if(stopbtncount%2 == 0):
        monitor = True
    else:                   # For odd number of btn presses
        monitor = False

    #print("The stop button was pressed this many times: ", stopbtncount)
    print("State of monitor variable is: ", monitor)
    print("")


def display_callback(DISPLAY):
    print("The display button was pressed\n")

    global outerArray
    
    for i in range(len(outerArray)):
        #print('| {0:>4} | {1:>4} | {2:>4}V | {3:>4}C | {4:>4}% |'.format(*outerArray[i]))
        # Find out from tutor why this method only prints the same thing (i.e the last element in outerArray) 5 times

        print(outerArray[i])
        

    print("")
    #time.sleep(0.2)

    
    # Setup events for the buttons
    # add rising-edge detection on a channel, ignoring further edges for 1s for switch debounce handling
    GPIO.add_event_detect(RESET, GPIO.RISING, callback = reset_callback, bouncetime = 1000)
    GPIO.add_event_detect(FREQUENCY, GPIO.RISING, callback = frequency_callback, bouncetime = 1000)
    GPIO.add_event_detect(STOP, GPIO.RISING, callback = stop_callback, bouncetime = 1000)
    GPIO.add_event_detect(DISPLAY, GPIO.RISING, callback = display_callback, bouncetime = 1000)
    
    
=======
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
    
# The display switch displays the first five reading since the stop switch was pressed
def display_callback(DISPLAY):
    print("The display button was pressed\n")

    global outerArray
    
    for i in range(len(outerArray)):
        #print('| {0:>4} | {1:>4} | {2:>4}V | {3:>4}C | {4:>4}% |'.format(*outerArray[i]))
        # Find out from tutor why this method only prints the same thing (i.e the last element in outerArray) 5 times

        print(outerArray[i])
        


    print("")
    #time.sleep(0.2)


#--------------------------------------------------------------------------------------------------------------
# Function to convert light data to percentage
def ConvertPercent(light_level):
    light_percent = (light_level/1023)*100
    light_percent = int(round(light_percent, 0))
    return light_percent

# Function to convert data to voltage level,
# rounded to specified number of decimal places.
def ConvertVolts(data,places):
  volts = (data * 3.3) / float(1023)
  volts = round(volts,places)
  return volts

# Function to calculate temperature from
# MCP9700A data, rounded to specified
# number of decimal places.
def ConvertTemp(data,places):
      temp = ((data * 190)/float(1023))
      temp = int(round(temp, places))
      return temp

<<<<<<< HEAD
=======



>>>>>>> general-changes
# Create a simple StopWatch function
# The input for the function is for example: value = time.time()
def StopWatch(value):
    '''Converts from seconds to Days:Hours:Minutes:Seconds'''

    valueD = (((value/365)/24)/60)
    Days = int (valueD)

    valueH = (valueD-Days)*365
    Hours = int(valueH)

    valueM = (valueH - Hours)*24
    Minutes = int(valueM)

    valueS = (valueM - Minutes)*60
    Seconds = int(valueS)

    timerStr = "%02d:%02d:%02d" % (Hours, Minutes, Seconds) # Format the string correctly
    return (timerStr)
<<<<<<< HEAD
=======

# Thanos function populates a single row
def Thanos():

    global end
    global timer
    global innerArray
    
    end = time.time()         
    timer = StopWatch(end-start)

    # Format of innerArray = [Time, Timer, Pot, Temp, Light]
    
    innerArray[0] = time.strftime("%H:%M:%S", time.localtime())
    innerArray[1] = timer

    # The read_adc function will get the value of the specified channel (0-2)
    innerArray[2] = mcp.read_adc(pot_channel)
    innerArray[3] = mcp.read_adc(temp_channel)
    innerArray[4] = mcp.read_adc(light_channel)


    # Convert the pot data to voltage with one dec place
    pot_level = innerArray[2]
    innerArray[2] = ConvertVolts(pot_level,1)

    # Convert the temp data to degrees celsius with zero dec places
    temp_level = innerArray[3]
    innerArray[3] = ConvertTemp(temp_level, 0)

    # Convert the light data to percentage with zero dec places
    light_level = innerArray[4]
    inverted_light_level = 1023 - light_level
    innerArray[4] = ConvertPercent(inverted_light_level)
    '''NB: the LDR decreases the voltage if you increase the amount of light shining on it,
    hence the reason for inverting the light_level reading'''


    #print(innerArray)
    return innerArray
    

#--------------------------------------------------------------
# Start the timer as soon as the program starts
start = time.time()

# Print column header once as soon as the program starts
print('| {0:>4}     | {1:>4}    |{2:>4}   | {3:>4}  | {4:>4} |'.format(*col_header)) # Note that the spacing was adjusted so that it prints correctly

# Main program loop.
while True:

    while(monitor == True):
        
        temp = Thanos()
        tempString = '| {0:>4} | {1:>4} | {2:>4}V | {3:>4}C | {4:>4}% |'.format(*temp)
        print(tempString)

        outerArray.insert(5, tempString)
        outerArray.pop(0)
        '''The above lines implement a FIFO queue. The insert command places the element at the end of the queue
        and the pop command gets rid off the first element in the queue, thus ensuring that the queue always contains
        the latest 5 lines for the table'''
            
        # Wait before repeating loop - this controls the frequency of monitoring the sensors
        time.sleep(delay)

GPIO.cleanup()
'''
except KeyboardInterrupt:
	print("\nStopping Program\n")
	GPIO.cleanup()       # clean up GPIO on CTRL+C exit

finally:
	GPIO.cleanup()           # clean up GPIO on normal exit
'''
>>>>>>> general-changes
