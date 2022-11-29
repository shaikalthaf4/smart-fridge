# @Shaik Althaf V. Shajihan {sav4@illinois.edu}
# Read LDR values using an I2C ADC
# Read the light sensor value and when it is high (LIGHT ON), print light ON, and when it is low (LIGHT OFF), print LIGHT OFF
import time
# Initilaize ADC
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from DFRobot_ADS1115 import ADS1115
ADS1115_REG_CONFIG_PGA_6_144V        = 0x00 # 6.144V range = Gain 2/3
ADS1115_REG_CONFIG_PGA_4_096V        = 0x02 # 4.096V range = Gain 1
ADS1115_REG_CONFIG_PGA_2_048V        = 0x04 # 2.048V range = Gain 2 (default)
ADS1115_REG_CONFIG_PGA_1_024V        = 0x06 # 1.024V range = Gain 4
ADS1115_REG_CONFIG_PGA_0_512V        = 0x08 # 0.512V range = Gain 8
ADS1115_REG_CONFIG_PGA_0_256V        = 0x0A # 0.256V range = Gain 16
ads1115 = ADS1115()
#Set the IIC address
ads1115.set_addr_ADS1115(0x48)
#Sets the gain and input voltage range.
ads1115.set_gain(ADS1115_REG_CONFIG_PGA_6_144V)

LS_PIN = 2 # light sensor on ADC PIN #2 

try:  
    while True:  
        # IF the light sensor senses light
        #Get the Digital Value of Analog of selected channel
        adc2 = ads1115.read_voltage(LS_PIN)
        if adc2 > 500: # Light detected ADC value threshold
          print("LIGHT ON!")
        else:
          print("LIGHT OFF!")
except KeyboardInterrupt:  
   print ("Exiting Program")  
except:  
   print ("Error Occurs, Exiting Program")  
finally:  
   # GPIO.cleanup() #clean all the ports used by the program
