import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

ECHO = 24
TRIG = 25

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

LEAD_Motor_Input1 =  17    # Input Pin (direction) Lead Motor
LEAD_Motor_Input2 =  18    # Input Pin (direction) Lead Motor
# #LEAD_Motor_Enable = 25    # Enable Lead Motor

DIR_Motor_Input1 =  22    # Input Pin (direction) Lead Motor
DIR_Motor_Input2 =  23    # Input Pin (direction) Lead Motor
#DIR_Motor_Enable = 18    # Enable Lead Motor

GPIO.setup(LEAD_Motor_Input1, GPIO.OUT)
GPIO.setup(LEAD_Motor_Input2, GPIO.OUT)
#GPIO.setup(LEAD_Motor_Enable, GPIO.OUT)

GPIO.setup(DIR_Motor_Input1, GPIO.OUT)
GPIO.setup(DIR_Motor_Input2, GPIO.OUT)
#GPIO.setup(DIR_Motor_Enable, GPIO.OUT)

time.sleep(2)

def right(duration):
    print("Turn to the right!")

    GPIO.output(LEAD_Motor_Input1, GPIO.HIGH)
    GPIO.output(LEAD_Motor_Input2, GPIO.LOW)
    
    GPIO.output(DIR_Motor_Input1, GPIO.HIGH)
    GPIO.output(DIR_Motor_Input2, GPIO.LOW)
    
    time.sleep(duration)

    GPIO.output(LEAD_Motor_Input1, GPIO.LOW)
    GPIO.output(DIR_Motor_Input1, GPIO.LOW)

def left(duration):
    print("Turn left!")   

    GPIO.output(LEAD_Motor_Input1, GPIO.LOW)
    GPIO.output(LEAD_Motor_Input2, GPIO.HIGH)
    
    GPIO.output(DIR_Motor_Input1, GPIO.LOW)
    GPIO.output(DIR_Motor_Input2, GPIO.HIGH)
    
    time.sleep(duration)

    GPIO.output(LEAD_Motor_Input2, GPIO.LOW)
    GPIO.output(DIR_Motor_Input2, GPIO.LOW)

def forward(duration):    
    print("Foward Motor")
#   pwm = GPIO.PWM(LEAD_Motor_Enable, 100)
#    pwm.start(0)

    GPIO.output(LEAD_Motor_Input1, GPIO.HIGH)
    GPIO.output(LEAD_Motor_Input2, GPIO.LOW)
    
    GPIO.output(DIR_Motor_Input1, GPIO.LOW)
    GPIO.output(DIR_Motor_Input2, GPIO.HIGH)
#    pwm.ChangeDutyCycle(100)
   # GPIO.output(LEAD_Motor_Enable, GPIO.HIGH)
    time.sleep(duration)

    GPIO.output(LEAD_Motor_Input1, GPIO.LOW)
    GPIO.output(DIR_Motor_Input2, GPIO.LOW)

def reverse(duration):
    print("Reverse Motor")

    GPIO.output(LEAD_Motor_Input1, GPIO.LOW)
    GPIO.output(LEAD_Motor_Input2, GPIO.HIGH)
    
    GPIO.output(DIR_Motor_Input1, GPIO.HIGH)
    GPIO.output(DIR_Motor_Input2, GPIO.LOW)

    time.sleep(duration)

    GPIO.output(LEAD_Motor_Input2, GPIO.LOW)
    GPIO.output(DIR_Motor_Input1, GPIO.LOW)
    

def stopBothMotors():
    print("Stop both motors")
    GPIO.output(LEAD_Motor_Input1, GPIO.LOW)
    GPIO.output(LEAD_Motor_Input2, GPIO.LOW)

    GPIO.output(DIR_Motor_Input1, GPIO.LOW)
    GPIO.output(DIR_Motor_Input2, GPIO.LOW)

def distance(iteration):
    print ("Distance Measurement in Progress")
    i = 0
    accumulatedDistance=0
    
    for i in range(iteration):   
        
        # Ensure that the Trigger pin is set low, and give the sensor a second to settle.
        GPIO.output(TRIG, False)
        print ("Wait for sensor to settle")
        time.sleep(0.1) #TODO decrease it to 0.1 for realtime usage.

        # The HC-SR04 sensor requires a short 10uS pulse to trigger the module.
        # (8 ultrasound bursts at 40 kHz)
        # To create our trigger pulse, we set out trigger pin high for 10uS then set it low again.
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)


        # We have sent our pulse signal we need to listen to our input pin
        # Timestamp of when the latest time pin was low
        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()
            
        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()
            
        pulse_duration = pulse_end - pulse_start

        # Speed = Distance / Time
        # Speed of sound at sea level: 343m/s, should be devided to 2 for going and returning
        distance = pulse_duration * 17150        
        accumulatedDistance += distance
        
        print ("Distance: ",distance,"cm")
        
    return accumulatedDistance

# Run the main program
if __name__ == '__main__':
    # Stop with ctrl + c
    try:

        iterations = 3
        while True:
            accDistance = distance(iterations);
            avgDistance = accDistance/iterations
            avgDistance = round(avgDistance, 2)
            print ("Average Distance: ", avgDistance," cm")

            flag = 0
            count = 0
            
#            f = True
            
#            if(f):
#                leftDirectionMotor(1)
#            else:    
            # if distance with obstacle is less than 15cm
            if avgDistance < 25:
                count = count + 1
                stopBothMotors()
                time.sleep(0.5)
                reverse(0.5)
                time.sleep(1)
                left(1)
                flag = 1
            else:    
                forward(0.2)
                flag = 0               
        
   
    except KeyboardInterrupt:
        # Remember to clean
        stopBothMotors()
        GPIO.cleanup()

