# Minecraft-Server-Control-Panel
Control panel for any minecraft server for Mac OS and Linux

![](documentation_images/started_screen.png)
_Main screen for control panel *_

# Control Panel Functions
Screenshot Functions *

# Installation
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
# Usege
---
##### Run scrip
```
python main.py 
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
---
