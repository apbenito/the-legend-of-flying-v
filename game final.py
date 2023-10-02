import game_functions as f
import pygame as pg
pg.init()

f.main_menu()
gamerunning = f.gamerunning





while gamerunning:
    
    f.collisions()
    gamerunning = f.processevents()
    f.redrawScreeningame()


pg.quit()
