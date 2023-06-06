# Read a small image in png format, traverse its pixels and for each pixel create a tile of a given color
# MODULES
import pygame
import random
import cv2
import PIL
import numpy as np

# DD
WIDTH = 1000
HEIGHT = 600
SCREEN = (WIDTH, HEIGHT)
display = pygame.display.set_mode(SCREEN)
RES = 12
OFFSETX = 8*RES
OFFSETY = 3*RES
THICKNESSLINE = 4
FILEROOTNAME = "cabinet"


# DD. PIXELGRID
# pixelGrid = numpy.Array()
# interp. a 2D array of pixels represented by three channels R,G,B
pixelGrid = cv2.imread(f'{FILEROOTNAME}.png')
print(pixelGrid.shape)

# DD. TILE
# tile = Tile()
# interp. a tile in a 2D array
class Tile:
    def __init__(self,c,r,color):
        self.c = c
        self.r = r
        self.x = OFFSETX + c * RES
        self.y = OFFSETY + r * RES
        self.rect = pygame.Rect(self.x,self.y,RES,RES)
        self.color = color
        self.isActive = False #whether or not to draw this tile
    
    def draw(self,display):
        self.updateRect()
        if self.isActive:
            pygame.draw.rect(display,self.color,self.rect)
            pygame.draw.rect(display,"black",self.rect,1)

    def updateRect(self):
        self.rect.topleft = self.x, self.y
        
# DD. GRID
# grid = [[TILE, ...],TILE, ...]
# interp. the 2D array of tiles
grid = []
for r in range(pixelGrid.shape[0]):
    row = []
    for c in range(pixelGrid.shape[1]):
        pixelColor = pixelGrid[r][c]
        # if tile is not white, then add it
        tile = Tile(c,r,pixelColor)
        if not np.array_equal(pixelColor,(255,255,255)):
            tile.isActive = True
        row.append(tile)
    grid.append(row)


# TEMPLATE FOR GRID
# for row in grid:
#   for tile in row:
#       ... tile


# DD. CTRL_PRESSED
# ctrl_pressed = bool
# interp. whether or not ctrl is being pressed
ctrl_pressed = False

# DD. Z_PRESSED
# z_pressed = bool
# interp. whether or not z is being pressed
z_pressed = False

# DD. ERASED_STACK
# erasedStack = [TILE, ...]
# interp. the collection of tiles that the player has erased
erasedStack = []

# DD. TIMER_CTRLZ
# timerCtrlZ = float
# interp. a timer to wait in between Ctrl+Z commands to avoid reverting too many changes
RESETTIMERCZ = 10
timerCtrlZ = RESETTIMERCZ

# CODE

def draw():
    display.fill("#1e1e1e")
    for row in grid:
      for tile in row:
          tile.draw(display)
    pygame.display.flip()

def update():
    global ctrl_pressed
    global z_pressed
    global timerCtrlZ

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mpos = pygame.mouse.get_pos()
                for row in grid:
                  for tile in row:
                      if tile.rect.collidepoint(mpos):
                          tile.isActive = False
                          erasedStack.append(tile)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                ctrl_pressed = True
            if event.key == pygame.K_s:
                pygame.image.save(display,f"{FILEROOTNAME}_{RES}_{THICKNESSLINE}.png")
 

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                ctrl_pressed = False
            elif event.key == pygame.K_z:
                z_pressed = True

    # if the player pressed ctrl + z, then undo the last action
    if ctrl_pressed and z_pressed:
        if timerCtrlZ <0:
            # access the last element in the stack
            if len(erasedStack)>0:
                erasedStack[-1].isActive = True
                erasedStack.pop(-1)
            timerCtrlZ = RESETTIMERCZ
            z_pressed = False

        else:
            timerCtrlZ-=0.1


while True:
    draw()
    update()