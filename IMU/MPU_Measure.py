import smbus #import SMBus module of I2C
from time import sleep          #import
import math
import time
import cv2
#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47


def MPU_Init():
    #write to sample rate register
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
    
    #Write to power management register
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
    
    #Write to Configuration register
    bus.write_byte_data(Device_Address, CONFIG, 0)
    
    #Write to Gyro configuration register
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
    
    #Write to interrupt enable register
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
    #Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)
    
        #concatenate higher and lower value
        value = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value


bus = smbus.SMBus(1) # or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address

MPU_Init()



# print (" Reading Data of Gyroscope and Accelerometer")

def Average(l):
    avg = sum(l) / len(l)
    return avg

t = 0
angle_x = 0
angle_y = 0
angle_z = 0
pi = math.pi
avg_Ax = [0]*20
avg_Ay = [0]*20
avg_single_Ax = 0
avg_single_Ay = 0
Vx = 0
Vy = 0
Vz = 0
prev_time = time.time()
Ax_max = 0
Ay_max = 0
Az_max = 0
while cv2.waitKey(100) != "q":

    # for i in range(20):          
    
        #Read Accelerometer raw value
    acc_x = read_raw_data(ACCEL_XOUT_H)
    acc_y = read_raw_data(ACCEL_YOUT_H)
    acc_z = read_raw_data(ACCEL_ZOUT_H)
    
        #Read Gyroscope raw value
    gyro_x = read_raw_data(GYRO_XOUT_H)
    gyro_y = read_raw_data(GYRO_YOUT_H)
    gyro_z = read_raw_data(GYRO_ZOUT_H)
    
        #Full scale range +/- 250 degree/C as per sensitivity scale factor
    Ax = -0.02 + acc_x/16384.0
    Ay = -0.07 + acc_y/16384.0
    Az = 1.06 + acc_z/16384.0
    
    if abs(Ax) > abs(Ax_max):
        Ax_max = Ax
    if abs(Ay) > abs(Ay_max):
        Ay_max = Ay
    if abs(Az) > abs(Az_max):
        Az_max = Az
    
    Gx = 0.56 + gyro_x/131.0
    Gy = 0.19 + gyro_y/131.0
    Gz = -0.19 + gyro_z/131.0
        
        #avg_Ax[i] = Ax
        #avg_Ay[i] = Ay
    
    
    #avg_single_Ax = Average(avg_Ax);
    #avg_single_Ay = Average(avg_Ay);
    #angle_x = round(avg_single_Ax * 90, 4) # @90d Ax = 1... 1*x=90, x=90
    #angle_y = round(avg_single_Ay * 91.4, 4) # @90d Ay=0.985... 0.985*y=90, y=91.4
    
    dt = time.time()-prev_time
    prev_time = time.time()
    
    # if abs(Ax) <0.05:
       # Ax = 0
    # if abs(Ay) <0.05:
      #   Ay = 0
    # if abs(Ay) <0.05:
      #   Ay = 0
    
    Vx += Ax *dt
    Vy += Ay *dt
    Vz += Az *dt
    # print ("Gx=%.2f" %Gx, u'\u00b0'+ "/s", "\tGy=%.2f" %Gy, u'\u00b0'+ "/s", "\tGz=%.2f" %Gz, u'\u00b0'+ "/s", "\tAx=%.2f g" %Ax, "\tAy=%.2f g" %Ay, "\tAz=%.2f g" %Az)
    #sleep(0.1)
    # print ("\tTime=%.2f s" %t)
    # print("acc_x:", Ax, "acc_y:", Ay, "acc_z:", Az)
    # Sprint("angle_x:", angle_x, "angle_y:", angle_y)

    #print(str(round(angle_y)))
    #print(str(round(angle_x)))
    print ("Current Gx=%.2f" %Gx, "\tCurrent Gy=%.2f" %Gy,"\tCurrent Gz=%.2f" %Gz)
    #print("avg_Ax=%.2f" %avg_single_Ax, "avg_Ay=%.2f" %avg_single_Ay)
    #print ("angle_x=%.2f" %angle_x, "\tangle_y=%.2f" %angle_y)
    print ("Current Ax=%.2f" %Ax, "\tCurrent Ay=%.2f" %Ay,"\tCurrent Az=%.2f" %Az)
    print ("Max Ax=%.2f" %Ax_max, "\t\tMax Ay=%.2f" %Ay_max,"\t\tMax Az=%.2f" %Az_max)
    # print("Vx=%.2f" %Vx, "\tVy=%.2f" %Vy,"\tVz=%.2f" %Vz)
    # print ("gyro_x=%.2f" %gyro_x, "\tgyro_y=%.2f" %gyro_y,"\tgyro_z=%.2f" %gyro_z)
    # print ("acc_x=%.2f" %acc_x, "\tacc_y=%.2f" %acc_y,"\tacc_z=%.2f" %Gz)