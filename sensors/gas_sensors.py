# Gas sensor data for FreshIO
'''
  @Shaik Althaf V. Shajihan {sav4@illinois.edu}
'''

#Run 30 mins after fridge door opens/closes - and cycle at user specified frequency - like, every 4 hours
# STEPS
'''
1. Note average of 30 mins gas sensor reading for the 3 sensors - gas
2. Estimate % change in gas_avg in the next run cycle (after 4 hours)
3. Discard the data in levels where change in items took place within fridge (food taken out/in ) to remove influence of changes from quantity of a food item or introductionremoval of an item
'''

# DATA FUSION Framework

'''
1. Assign a weight to levels or food items close to a sensor based on % change in gas_avg (change_gas_avg)
    ---based on calibration with more data and time
        --- change_gas_avg = 25-50% : gas_weigh = 0.2
        --- change_gas_avg = 50-100% : gas_weigh = 0.5
        --- change_gas_avg = 100-200% : gas_weigh = 0.7
        --- change_gas_avg = >200% : gas_weigh = 1.0
2. Check if expiry table available for an item
    - if YES,
        expiry_weigh = remaining_dates/Estiamted_exiry  
'''

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import sys
sys.path.append('../')
import time
import csv

'''!
  @file demo_read_voltage.py
  @brief connect ADS1115 I2C interface with your board (please reference board compatibility)
  @n  The voltage value read by A0 A1 A2 A3 is printed through the serial port.
  @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @license     The MIT License (MIT)
  @author [luoyufeng](yufeng.luo@dfrobot.com)
  @version  V1.0
  @date  2019-06-19
  @url https://github.com/DFRobot/DFRobot_ADS1115
'''

# Bosch AI gas sensor


from bme68x import BME68X
import bme68xConstants as cnst
import bsecConstants as bsec
import gpiozero as gpio
from time import sleep

bme = BME68X(cnst.BME68X_I2C_ADDR_LOW, 0)
bme.set_sample_rate(bsec.BSEC_SAMPLE_RATE_LP)

print("sample rate:", bsec.BSEC_SAMPLE_RATE_LP)


def get_data(sensor):
    data = {}
    try:
        data = sensor.get_bsec_data()
    except Exception as e:
        print(e)
        return None
    if data == None or data == {}:
        sleep(0.1)
        return None
    else:
        sleep(1)
        return data

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
#from datetime import *

# READ and plot Gas sensors data

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from DFRobot_ADS1115 import ADS1115
ADS1115_REG_CONFIG_PGA_6_144V        = 0x00 # 6.144V range = Gain 2/3
ADS1115_REG_CONFIG_PGA_4_096V        = 0x02 # 4.096V range = Gain 1
ADS1115_REG_CONFIG_PGA_2_048V        = 0x04 # 2.048V range = Gain 2 (default)
ADS1115_REG_CONFIG_PGA_1_024V        = 0x06 # 1.024V range = Gain 4
ADS1115_REG_CONFIG_PGA_0_512V        = 0x08 # 0.512V range = Gain 8
ADS1115_REG_CONFIG_PGA_0_256V        = 0x0A # 0.256V range = Gain 16
ads1115 = ADS1115()

#### Write CSV
adc0_val = 0
adc1_val = 0

fieldnames = ['ADC_0','ADC_1']

with open('data_1s.csv','w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

# Parameters
x_len = 100         # Number of points to display
y_range = [0, 2000]  # Range of possible Y values to display

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = list(range(0, 100))
ys0 = [0] * x_len
ys1 = [0] * x_len
ys2 = [0] * x_len
ys3 = [0] * x_len
ax.set_ylim(y_range)

# Create a blank line. We will update the line in animate
line0, = ax.plot(xs, ys0, '-b', label = 'ADC0 - CH4 (Methane) ' )
line1, = ax.plot(xs, ys1, '-r', label = 'ADC1 - Ethane/Alcohol' )
line2, = ax.plot(xs, ys2, '-k', label = 'BoschAI- co2_equivalent' )
line3, = ax.plot(xs, ys3, '-g', label = 'BoschAI- Air Quality' )
plt.legend()

# Add labels
plt.title('Gas sensor reading vs. Samples')
plt.xlabel('Samples')
plt.ylabel('Sensor reading')

#Set the IIC address
ads1115.set_addr_ADS1115(0x48)
#Sets the gain and input voltage range.
ads1115.set_gain(ADS1115_REG_CONFIG_PGA_6_144V)
# This function is called periodically from FuncAnimation
def animate(i, ys0,ys1,ys2,ys3):
    

    #Get the Digital Value of Analog of selected channel
    adc0 = ads1115.read_voltage(0)
    time.sleep(0.2)
    adc1 = ads1115.read_voltage(1)
    time.sleep(0.2)
    adc2 = ads1115.read_voltage(2)
    time.sleep(0.2)
    adc3 = ads1115.read_voltage(3)
    print ("A0:%dmV A1:%dmV A2:%dmV A3:%dmV"%(adc0['r'],adc1['r'],adc2['r'],adc3['r']))
    #Boasch AI data
    bsec_data = get_data(bme)
    while bsec_data == None:
        bsec_data = get_data(bme)
    print(bsec_data)    
    print("value:", bsec_data["co2_equivalent"])
    
    #rint(adc0)
    # Add y to list
    ys0.append(adc0['r'])
    ys1.append(adc1['r'])
    ys2.append(bsec_data["co2_equivalent"])
    ys3.append(50*bsec_data["iaq"])

    # Limit y list to set number of items
    ys0 = ys0[-x_len:]
    ys1 = ys1[-x_len:]
    ys2 = ys2[-x_len:]
    ys3 = ys3[-x_len:]
    # Update line with new Y values
    line0.set_ydata(ys0)
    line1.set_ydata(ys1)
    line2.set_ydata(ys2)
    line3.set_ydata(ys3)
    
    with open('data_1s.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        info = {
            "ADC_0": adc0['r'],
            "ADC_1": adc1['r']
        }
        
        csv_writer.writerow(info)

    return line0,line1,line2,line3

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig,
    animate,
    fargs=(ys0,ys1,ys2,ys3),
    interval=50,
    blit=True)
plt.show()

#########################



dateconv = lambda s: datetime.strptime(s, "%H:%M:%S")
col_names = ["T", "V"]

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

def animate(i):
    bsec_data = get_data(bme)
    while bsec_data == None:
        bsec_data = get_data(bme)
    print(bsec_data)    
    print("value:", bsec_data["iaq"])   
    with open("air_qual.csv", 'a') as log:
        log.write("{0},{1}\n".format(datetime.now().strftime("%H:%M:%S"),str(bsec_data["iaq"])))
    with open('air_qual.csv','rb') as f:
        lines = f.readlines()

    mydata = np.genfromtxt(lines[-24:], delimiter=',', names=col_names, dtype=[('T', 'O'), ('V', 'u1')], converters={"Time": dateconv})
    ax.clear()
    ax.plot(mydata['T'], mydata['V'])

    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Air Quality Graph ')
    plt.ylabel('Air Quality (IAQ)')
    plt.xlabel('Time')
    
ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
