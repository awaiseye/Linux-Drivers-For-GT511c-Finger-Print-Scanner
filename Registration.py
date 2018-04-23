#! /usr/bin/python 

#Registering a new fingerprint in module

#Created by awais ahmad siddiqi
#Email: awais_eye@yahoo.com




import time
import serial
import binascii
import sys
print 'Argument List:', str(sys.argv)
ser = serial.Serial('/dev/serial0',9600,timeout=1)
#the output of above line will be like this ---->Argument List: ['readwrite.py', 'awais', 'adeel', 'haris']
buffer=[00,00,00,00,00,00,00,00,00,00,00,00]
hexcmd = [0x55,0xaa,0x01,0x00,0x01,0x00,0x00,0x00,0x12,0x00,0x13,0x01]
ser.write(serial.to_bytes(hexcmd))
nflag = 0
response = ser.readline()
for i in range (0,12):
         print "0x" + str(binascii.hexlify(response[i])),
print ""


#function for Sending, Receiving, and showing the daga from serial
def srs():
    ser.write(serial.to_bytes(hexcmd))
    response = ser.readline()
    for i in range (0,12):
          buffer[i]= str(binascii.hexlify(response[i]))
          print buffer[i],
    print ""

def fpcheck():
     hexcmd = [0x55,0xaa,0x01,0x00,0x00,0x00,0x00,0x00,0x26,0x00,0x26,0x01]
     srs()
     ser.write(serial.to_bytes(hexcmd))
     response = ser.readline()

     while (str(binascii.hexlify(response[4]))!='00'):
        print('finger not pressed.. press finger')
        hexcmd = [0x55,0xaa,0x01,0x00,0x00,0x00,0x00,0x00,0x26,0x00,0x26,0x01]
        ser.write(serial.to_bytes(hexcmd))
        response = ser.readline()
        time.sleep(1)
srs()
#check for enrollment count
print 'checking enrolment count'
hexcmd = [0x55,0xaa,0x01,0x00,0x00,0x00,0x00,0x00,0x20,0x00,0x20,0x01]
srs()
cmdrun=[0x00,0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,0x0a,0x0b,0x0c,0x0d,0x0e,0x0f,0x10,0x11,0x12,0x13]
print(buffer[4])
hex_int = int (buffer[4], 16)
index=hex_int
print hex(hex_int)
print 'Light is on, now Enroll Request..'
hexcmd = [0x55,0xaa,0x01,0x00,cmdrun[index],0x00,0x00,0x00,0x22,0x00,0x22+cmdrun[index],0x01]
srs()
if (buffer[8]=='30'): 
     print ('press finger')
     fpcheck()
     hexcmd = [0x55,0xaa,0x01,0x00,0x00,0x00,0x00,0x00,0x60,0x00,0x60,0x01]
     srs()
     if (buffer[8]=='30'):
        print('ok, proceeding for making 1st enrollemnt ')

     while (buffer[4]=='12'):
        print('finger not pressed.. press finger')
        hexcmd = [0x55,0xaa,0x01,0x00,0x00,0x00,0x00,0x00,0x60,0x00,0x60,0x01]
        ser.write(serial.to_bytes(hexcmd))
        response = ser.readline()
        time.sleep(1)
     hexcmd = [0x55,0xaa,0x01,0x00,0x00,0x00,0x00,0x00,0x23,0x00,0x23,0x01]
     srs()
     if (buffer[8]=='30'):
        print('Remove and Press again ')
        nflag = 1
 # #    #    #    #    #    #    #    #    #    #    #   
 #    #    #    #    #    #    #    #    #    #    #    #    #   
 #    #    #    #    #    #    #    #    #    #    #### 

if (nflag==1):
   fpcheck()
   hexcmd = [0x55,0xaa,0x01,0x00,0x00,0x00,0x00,0x00,0x60,0x00,0x60,0x01]
   srs()
   if (buffer[8]=='30'):
        print('Second Captuered')
   hexcmd = [0x55,0xaa,0x01,0x00,cmdrun[index],0x00,0x00,0x00,0x24,0x00,0x24+cmdrun[index],0x01]
   srs()
   if (buffer[8]=='30'):
        print('Remove and Press again ')
        nflag = 2

if (nflag==2):
   fpcheck()
   hexcmd = [0x55,0xaa,0x01,0x00,0x00,0x00,0x00,0x00,0x60,0x00,0x60,0x01]
   srs()
   if (buffer[8]=='30'):
        print('3rd  Captuered')
   hexcmd = [0x55,0xaa,0x01,0x00,cmdrun[index],0x00,0x00,0x00,0x25,0x00,0x25+cmdrun[index],0x01]
   srs()
   if (buffer[8]=='30'):
        print('3rd  Temp Made ')
        nflag = 3
   
#turning light off
hexcmd = [0x55,0xaa,0x01,0x00,0x00,0x00,0x00,0x00,0x12,0x00,0x12,0x01]
srs()
if (nflag != 3):
 print ('error')



