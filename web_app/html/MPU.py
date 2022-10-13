import smbus #import SMBus module of I2C
from time import sleep          #import
import math
import time


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
time.sleep(1)
Device_Address = 0x68   # MPU6050 device address

MPU_Init()



# print (" Reading Data of Gyroscope and Accelerometer")

def Average(l):
    avg = sum(l) / len(l)
    return avg

t = 0;
angle_x = 0;
angle_y = 0;
angle_z = 0;
pi = math.pi;
avg_Ax = [0]*20
avg_Ay = [0]*20
avg_single_Ax = 0;
avg_single_Ay = 0;

while True:

    for i in range(20):          
    
        #Read Accelerometer raw value
        acc_x = read_raw_data(ACCEL_XOUT_H)
        acc_y = read_raw_data(ACCEL_YOUT_H)
        acc_z = read_raw_data(ACCEL_ZOUT_H)
    
        #Read Gyroscope raw value
        gyro_x = read_raw_data(GYRO_XOUT_H)
        gyro_y = read_raw_data(GYRO_YOUT_H)
        gyro_z = read_raw_data(GYRO_ZOUT_H)
    
        #Full scale range +/- 250 degree/C as per sensitivity scale factor
        Ax = -0.07 + acc_x/16384.0
        Ay = 0.02 + acc_y/16384.0
        Az = -0.97 + acc_z/16384.0
    
        Gx = 0.56 + gyro_x/131.0
        Gy = 0.19 + gyro_y/131.0
        Gz = -0.24 + gyro_z/131.0
        
        avg_Ax[i] = Ax
        avg_Ay[i] = Ay
    
    
    avg_single_Ax = Average(avg_Ax);
    avg_single_Ay = Average(avg_Ay);
    angle_x = round(avg_single_Ax * 90, 4) # @90d Ax = 1... 1*x=90, x=90
    angle_y = round(avg_single_Ay * 91.4, 4) # @90d Ay=0.985... 0.985*y=90, y=91.4
    
    # print ("Gx=%.2f" %Gx, u'\u00b0'+ "/s", "\tGy=%.2f" %Gy, u'\u00b0'+ "/s", "\tGz=%.2f" %Gz, u'\u00b0'+ "/s", "\tAx=%.2f g" %Ax, "\tAy=%.2f g" %Ay, "\tAz=%.2f g" %Az)
    #sleep(0.1)
    # print ("\tTime=%.2f s" %t)
    #print("acc_x:", Ax, "acc_y:", Ay, "acc_z:", Az)
    # print("angle_x:", angle_x, "angle_y:", angle_y)
    file = open("angle_x.txt", "w")
    file.write(str(round(angle_x)))
    file.close()
    file = open("angle_y.txt","w")
    file.write(str(round(angle_y)))
    file.close()
    break
    #print ("Gx=%.2f" %Gx, "\tGy=%.2f" %Gy,"\tGz=%.2f" %Gz)
    #print("avg_Ax=%.2f" %avg_single_Ax, "avg_Ay=%.2f" %avg_single_Ay)
    #print ("angle_x=%.2f" %angle_x, "\tangle_y=%.2f" %angle_y)
    #print ("Ax=%.2f" %Ax, "\tAy=%.2f" %Ay,"\tAz=%.2f" %Az)
    #print ("gyro_x=%.2f" %gyro_x, "\tgyro_y=%.2f" %gyro_y,"\tgyro_z=%.2f" %gyro_z)
    #print ("acc_x=%.2f" %acc_x, "\tacc_y=%.2f" %acc_y,"\tacc_z=%.2f" %Gz)
    
