from gpiozero import Servo
import math
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()

servo = Servo(17, min_pulse_width = 0.5/1000, max_pulse_width = 2.33/1000, pin_factory=factory)

try:
    angle = 125 #Fixed angle of 150
    servo.value = math.cos(math.radians(angle)) * -1
    sleep(1)
except KeyboardInterrupt:
    #Add extra here for safety upon "Ctrl + C" keyboard input exit
    print("Goodbye!")

    

