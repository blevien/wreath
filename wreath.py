import RPi.GPIO as GPIO
import time
import pygame.mixer
from sys import exit

button = 18
lights = [8,7,11,9,10,22,27,17,4,1,0,14]


#configure Pin Modes
GPIO.setmode(GPIO.BCM)
for light in lights:
    GPIO.setup(light, GPIO.OUT)

GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

patterns = {}

# Turn off all LEDs
def clear_leds():
    for light in lights:
        GPIO.output(light, False)

def blink(x):
    for light in lights:
        GPIO.output(light, True)
    time.sleep(x)
    for light in lights:
        GPIO.output(light, False)
    time.sleep(x)

def finale():

    #Go CLockwise
    for light in lights:
        GPIO.output(light, True)
        time.sleep(.1)
        GPIO.output(light, False)

    #go Counterclockwise
    for light in reversed(lights):
        GPIO.output(light, True)
        time.sleep(.1)
        GPIO.output(light, False)

    #Blink all 3 Times
    for x in range(8):
        blink(.1)


def is_true(value):
    if value == "True":
        return True
    else:
        return False


#Loop through the program to continually test if buttons are high or low
try:
    clear_leds()
    finale()

    notes = open("Wreath - Sheet1.csv")
    for line in notes:
        pattern = line.split(",")
        patterns[pattern[0]] = pattern[1:13]
    print ("Notes Loaded")


    while True:

        input_value = GPIO.input(button)
        #input_value = True

        if input_value == True:

            pygame.mixer.init()
            pygame.mixer.music.load("12days.wav")
            pygame.mixer.music.play()
            start_time = time.time()

            while pygame.mixer.music.get_busy() == True:

                et = str(round(time.time() - start_time,2))

                if et in patterns.keys():

                    for x in range(len(lights)):
                        GPIO.output(lights[x], is_true(patterns[et][x]))
                        print is_true(patterns[et][x])

                    time.sleep(.1)

            finale()
            clear_leds()


except KeyboardInterrupt:
    clear_leds()
    GPIO.cleanup()
    exit(0)
