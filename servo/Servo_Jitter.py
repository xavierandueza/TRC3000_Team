import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(11,GPIO.OUT)
servo1 = GPIO.PWM(11,50)
servo1.start(0)
duty = 1;

while duty <= 12:
    servo1.ChangeDutyCycle(duty)
    time.sleep(3)
    duty = duty + 6

servo1.stop()

GPIO.cleanup()
