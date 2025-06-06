import board
import digitalio
#import RPi.GPIO as GPIO
import time

REFERENCE_SENSOR_PIN = 4  # GPIO pin for the reference sensor

#GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
#GPIO.setup(REFERENCE_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

switch = digitalio.DigitalInOut(board.D4)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP  # Set pull-up resistor

while True:
    # Check if the reference sensor is triggered
    #print(GPIO.input(REFERENCE_SENSOR_PIN))
    print(switch.value)  # Print the state of the switch
    time.sleep(0.5)  # Sleep for a short duration to avoid flooding the output