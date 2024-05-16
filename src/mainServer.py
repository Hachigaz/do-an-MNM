import socket as socket
import pygame as pg

hostSocket = socket.create_server(("",22705),family=socket.AF_INET,dualstack_ipv6=False)
clientSocket = hostSocket.accept()

print("client connected",clientSocket)


screen:pg.Surface = pg.display.set_mode((1366, 768))

clock = pg.time.Clock()
is_running = True
while is_running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            is_running = False

    screen.fill(pg.Color(20,20,20))
    
    
    pg.display.flip()

    clock.tick(60)