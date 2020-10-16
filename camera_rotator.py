# -*- coding: UTF-8 -*-

# import libraries
import RPi.GPIO as GPIO
import time


SERVO = 4
GPIO.setmode(GPIO.BCM)
# set pin as output, set servo1 as pin 04 as PWM
GPIO.setup(SERVO, GPIO.OUT)
servo= GPIO.PWM(SERVO, 50) # pin 11 -> 50Hz pulse

def initServo():   
    # start PWM running, but with value of 0 (pulse off)
    servo.start(0)
    time.sleep(0.2)


def rotateClockwise(angle):    
    duty = 2
    servo.ChangeDutyCycle(duty + (angle/18))
    time.sleep(0.5)
    servo.ChangeDutyCycle(0) # to optimize the movement of servo (avoid jitter), we set the motor to pulse off (stop)          

    # wait few seconds
    time.sleep(1)

def lookLeft():    
    duty = 2
    servo.ChangeDutyCycle(duty + (180/18))
    time.sleep(0.5)
    servo.ChangeDutyCycle(0) # to optimize the movement of servo (avoid jitter), we set the motor to pulse off (stop)          

    # wait few seconds
    time.sleep(1)
    
def lookRight():    
    duty = 2
    servo.ChangeDutyCycle(duty + (0/18))
    time.sleep(0.5)
    servo.ChangeDutyCycle(0) # to optimize the movement of servo (avoid jitter), we set the motor to pulse off (stop)          

    # wait few seconds
    time.sleep(1)

def lookForward():    
    duty = 2
    servo.ChangeDutyCycle(duty + (90/18))
    time.sleep(0.5)
    servo.ChangeDutyCycle(0) # to optimize the movement of servo (avoid jitter), we set the motor to pulse off (stop)          

    # wait few seconds
    time.sleep(1)

def cleanup():
    # Clean things up
    servo.stop()
