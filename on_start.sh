#!/bin/bash

echo "Initializing gpsd..."
sudo service gpsd start

echo "Initializing pigpiod..."
sudo service pigpiod start

echo "Initializing the setup environment..."
source /home/rpi/myenv/bin/activate
if [[$? -eq 0]]; then
	echo "Environment enabled"
else
	echo "Could not initialize the environment... try again manually"
fi

echo "Running the main program"
cd myenv
python3 main.py


if [[$? -ne 0]]; then
	echo "Restarting the system"
	sudo reboot
fi
