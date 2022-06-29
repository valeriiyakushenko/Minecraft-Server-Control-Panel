# Minecraft-Server-Control-Panel
Control panel for any minecraft server for Mac OS and Linux
---
![](documentation_images/started_screen.png)<br />
_Main screen for control panel *_

# Control Panel Functions
![](documentation_images/functions.gif)<br />
You can change the time, weather, and control the parameters of the player

# Installation

Download the latest release and extract it to your server folder

---
Install pip:
>Run in Control Panel directory 
```
python get-pip.py
```
---
Install pip library's:
```
pip install pyyaml

pip3 install customtkinter

pip install mcrcon
```
---
##### Enable rcon on server
Remember to enable these options for the program to work [```server.properties```](https://minecraft.gamepedia.com/Server.properties) file.
```
enable-query=true
enable-rcon=true
query.port=25565
rcon.port=25575
rcon.password=your_pasword
```
# Usage
##### Run scrip
```
python main.py 
```
---
Go to the main tab and open the settings<br />
Fill in all the parameters for the panel to work correctly<br />
![](documentation_images/settings.png)
---
Click on the file button in the upper right corner and select the jar file of your server which should be in the same folder as the control panel
