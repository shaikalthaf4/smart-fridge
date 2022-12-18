
## Sensor hardware - ADS1115, MQ3, MQ4, BoschAI BME 6888
### Hardware Connection
1. Connect the Analog MQ3 and MQ4 Gas sensors to ADC 0 & ADC 1 of the ADS1115 via I2C to rpi4
2. Connect BME688 on a parllel channel of I2C pin of rpi4
### Install ADC library from source
https://www.dfrobot.com/product-1730.html
https://github.com/DFRobot/DFRobot_ADS1115
### Install BME688 library
https://github.com/pi3g/bme68x-python-library
```
pip3 install bme68x
```
