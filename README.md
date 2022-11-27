# SmartFridge

## Configure the Enviornment
Update packages on your raspberry Pi OS
```
sudo apt-get update
```
Check the python version, you should have version 3.7 or later for running the code.
```
python --version
```
Install virtual environment
```
pip install virtualenv
```
Create a Python virtual environment for TFlite
```
python -m venv ~/tflite
```
Run the following command whenever you open a new terminal window to activate the virtual environment.
```
source ~/tflite/bin/activate
```
Clone this repository
```
git clone https://github.com/Zilinghan/smart-fridge.git
```
Install the dependencies
```
pip install -r requirements.txt
```
Download the trained detection model from [this link](https://drive.google.com/file/d/1Cy8NWsV4fdJhDaV_MI3B06O7aaSgD7fE/view?usp=share_link), and save it into the `models` folder as `models/model.tflite`.

Run the code
```
python run.py
```