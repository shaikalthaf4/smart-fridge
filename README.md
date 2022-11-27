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
git clone https://github.com/Zilinghan/smart-fridge.git smart-fridge
```
Change the directory to the project directory.
```
cd smart-fridge
```
Install Scipy: first run `uname -m` to get the architecture of you raspberry Pi, you should see something like `armv7l`. Then go to [this link](https://www.piwheels.org/simple/scipy/) to download the correponding wheel for your python version and arch. For example you need to download `SciPy-1.8.1-cp39-cp39-linux_armv7l.whl` for `scipy 1.8.1` if your python version is `3.9.X `and your arch is `armv7l`. Then go to the download folder and run the following command to install it (you need to change the .whl name accrodingly).

```
pip install SciPy-1.8.1-cp39-cp39-linux_armv7l.whl
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