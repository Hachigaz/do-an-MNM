# fly war - A local online game created using Python
![image](https://github.com/Hachigaz/do-an-MNM/assets/58378033/f14da737-1ea7-4ace-aad2-7a4d218ad464)

## Overview
![image](https://github.com/Hachigaz/do-an-MNM/assets/58378033/4e9f23ec-223d-4bf0-b759-735f63584c53)

fly war is a simple game created using Python, with the use of additional libraries such as Pygame for GUI rendering, Pymunk for physics simulation, Shapely for presenting geometric shapes for rendering, and Python Socket for networking.
###
The game is multiplayer only, and more than two players can join the game.
##

## Gameplay
![image](https://github.com/Hachigaz/do-an-MNM/assets/58378033/d50675c9-3647-4b85-9eb5-b72ab24ba772)
![image](https://github.com/Hachigaz/do-an-MNM/assets/58378033/9f250279-0ff8-4592-84f2-f7bb70e00d35)

You control a spaceship and try to shoot down other players that are trying to do the same.
###
![image](https://github.com/Hachigaz/do-an-MNM/assets/58378033/38d2f720-6d08-4300-ae6e-e8d865c57168)
###
Game controls:
####
W - Move forward
####
A - Rotate left
####
D - Rotate right
####
S - Brake
####
Space - Shoot

## Installation
1. Install Python and pip
###
2. In your terminal install Pygame,Pymunk and Shapely using the command:
   ```bash
   pip install pygame pymunk shapely
###
3. Run the game by running main.py:
   ```bash
   ./main.py
###
###
## Playing
### Creating a lobby
In the main menu screen, click on the Multiplayer button, then click on the Host button and type in your player name and port number, then proceed to create lobby and wait for your friends to join.
### Joining a lobby
In the main menu screen, click on the Multiplayer button, then click on the Join by IP button and type in your player name, the host's IP address and port number, then click on Join and wait for the game to connect to the host lobby.
###
The game has a simple text chatbox in the game lobby for messaging with your friends:
###
![image](https://github.com/Hachigaz/do-an-MNM/assets/58378033/a2e37dc6-487b-4d27-815b-9465ecf7edf5)
