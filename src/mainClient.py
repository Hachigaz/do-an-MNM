import socket as socket
import pygame as pg

clientSocket = socket.create_connection(("192.168.1.18",22705),5)

print(socket)


screen:pg.Surface = pg.display.set_mode((1366, 768))

clock = pg.time.Clock()
is_running = True
while is_running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            is_running = False

    screen.fill(pg.Color(100,100,100))
    
    
    pg.display.flip()

    clock.tick(60)