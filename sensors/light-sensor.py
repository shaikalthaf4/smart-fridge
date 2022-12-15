# TODO: Althaf
# Read the light sensor value and when it is high (LIGHT ON), print light ON, and when it is low (LIGHT OFF), print LIGHT OFF
import time
import RPi.GPIO as GPIO  
GPIO.setwarnings(False)

LS_PIN = 8 # light sensor PIN number
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LS_PIN, GPIO.IN)
try:  
    while True:  
        # IF the light sensor senses light
        # print("LIGHT ON!")
        # ELSE
        # print("LIGHT OFF!")
        time.sleep(1)
except KeyboardInterrupt:  
   print ("Exiting Program")  
except:  
   print ("Error Occurs, Exiting Program")  
finally:  
   GPIO.cleanup() #clean all the ports used by the program