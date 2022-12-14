# CS5510 Final Soccerbot

This github contains the videos and source code for our final robotics challenge.  Note that running the code will require a mondern CPU paired with a GPU, as the speed required for proper interception is crucial for this program to run correctly.

## Videos

All videos can be found in the [./videos](videos) folder, as well as the included README for what videos contain what content.

## HOW TO RUN

> NOTE: Ip addresses need to be configured in both the yahboom-server and yahboom-raspi files to work correctly, with each on pointer to the IP of the other

1. Create a virtual environment running python 3.9 - 3.10
2. Install the required packages uing `pip install -r requirements.txt
3. Connect to the robot using ssh
4. Copy this folder to the robot
5. Run `python3 /robot/yahboom-server.py` on the host laptop / desktop
6. Run `python3 /robot/yahboom-raspi.py` on the robot

Several of the scripts can be ran as standalone, but these 2 scripts are the finishedstand alone product.

You can also disable ceratin features / functions by enabling their specific debug flags, located at the bottom of each yabhoom file.
All features are enabled by default
