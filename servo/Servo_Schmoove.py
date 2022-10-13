from gpiozero import Servo
import math
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()

servo = Servo(17, min_pulse_width = 0.5/1000, max_pulse_width = 2.33/1000, pin_factory=factory)

servo.min()

try:
    while True:
        #Ask user for angle and turn servo to it
        try:
            angle = float(input('Enter an angle between 0 & 180: '))
        except ValueError:
            print("No... Input is not a number")
            continue
        else:
            if angle > 180:
                print('Not so high, between 0 and 180 please!')
                continue
            elif angle < 0:
                print('No negatives, between 0 and 180 please!')
                continue
            # print("Type of number ", type(angle))
            
            servo.value = math.cos(math.radians(angle)) * -1
            sleep(1)

except KeyboardInterrupt:
    sleep(1)
    servo.mid()
    sleep(1)
    #servo.stop() // These two lines are not functions of the library...
    #GPIO.cleanup()
    print("\nGoodbye!")
    
#while True:
#    for i in range (0, 360):
#        print(i)
#        servo.value = math.sin(math.radians(i))
#        sleep(0.01)
        
        
#while True:
 #   for i in range (0, 360,10):
  #      print(i)
   #     servo.value = math.sin(math.radians(i))
    #    sleep(0.1)

#servo.min()
#sleep(1)
#servo.mid()
#sleep(1)
#servo.max()
#sleep(1)

#servo.value = -1
#sleep(1)
#servo.value = 0
#sleep(1)
#servo.value = 1
#sleep(1)
