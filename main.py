from pygame import *

background = (200, 255, 255)
win_width = 800
win_height = 500
window = display.set_mode((win_width, win_height))
window.fill(back)

game = True
finish = False
clock = time.Clock()
FPS = 60

