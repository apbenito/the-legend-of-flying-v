import pygame as pg
import os, time


#       ***********************VARIABLES:***********************
#let's define some variables

#path for file and data (images, sounds)
main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir,'data')


#screen variables
scrw = 960
scrh = 540
scalefactor = 1
reso = (scrw/scalefactor,scrh/scalefactor)

# time parameters
fps = 60 # frame rate
ani = 4  # animation cycles
clock = pg.time.Clock()

# initial position + velocities
dt = 0.9
g = 1
vx = 7.5
vy = -20

#Booleans and counters
sound_played = False
gamerunning = False
iswin = False
starting_time_game = 0
bg_count = 0
scene = 0     
pickup_count = 0
losetime = 60






#       ***********************FUNCTIONS***********************
#space to define functions

#functions to create resources
def load_image(path, colorkey = None, scale=1):
    
    #function to load an image. arguments:
        #name: string with document name (i.e.'background.png')
        #colorkey: background color to delete. use -1 to use it
    
    image = pg.image.load(path)
    image = image.convert()

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pg.transform.scale(image, size)
    
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()


def timer(starting_time, endtime):
    
    elapsed_time = (pg.time.get_ticks() - starting_time) / 1000
    counter_time = endtime - int(elapsed_time)

    return elapsed_time, counter_time

#font stuff
def printgametext (fontsize, string, screen, x, y, color):
    font = pg.font.Font('data/fonts/Pixeled.ttf', fontsize)
    fontsurface = font.render(string, True, color)
    fontrect = fontsurface.get_rect()
    screen.blit(fontsurface, (x, y))
    
def main_menu():
    global gamerunning
    
    pg.mixer.Channel(5).play(menubgm)
    running = True
    pg.event.pump()
    keys = pg.key.get_pressed()

    while running:
        #fills background and logo
        screen.blit(menubg,(0,0))
        screen.blit(logo, (80,90))
        printgametext(8, "MADE BY PABLO ARELLANO AND HANQIU LI", screen, 30, 510, (255,255,255))
        if startbutton.buttonclick():
            click_sound.play()
            running = False
            introscreen()
        if exitbutton.buttonclick():
            click_sound.play()
            running = False
        #updates screen
        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                running = False


def introscreen():
    global gamerunning, starting_time_game
    running = True

    while running:
        screen.fill((0, 0, 0))
        screen.blit(intro, (0,0))
        #updates screen
        pg.display.flip()
        pg.event.pump()
        keys = pg.key.get_pressed()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                pg.mixer.Channel(5).stop()
                click_sound.play()
                pg.mixer.music.play(-1)
                pg.mixer.music.set_volume(0.25)
                running = False
                gamerunning = True
                starting_time_game = pg.time.get_ticks()    
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pg.mixer.Channel(5).stop()
                click_sound.play()
                main_menu()
                running = False

def winscreen_funct():
    running = True
    pg.mixer.Channel(7).play(menubgm)
    while running:
        pg.display.flip()
        pg.event.pump()
        keys = pg.key.get_pressed()
        screen.blit(winscreen,(0,0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                running = False
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                running = False

def losescreen_funct():
    running = True
    while running:
        pg.display.flip()
        pg.event.pump()
        keys = pg.key.get_pressed()
        screen.blit(losescreen,(0,0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                running = False
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                running = False

def collisions():
    nplatfoms = len(platforms)
    #Loop for platform processing
    for i in range(nplatforms):
        #if character collides with the platform it goes inside the if and checks where it has hit:
        if pg.Rect(char.hitbox).colliderect(pg.Rect(platforms[i].hitbox)):
            if platforms[i].scene == scene:
                #character hits the bottom: char.y under the platform and char.x between the edges of the platform
                if not platforms[i].block and char.y >= platforms[i].y + platforms[i].hitbox[3] - 30 and (char.x > platforms[i].x and char.x + 32 < platforms[i].x + platforms[i].hitbox[2]) :
                    char.y = platforms[i].y + platforms[i].hitbox[3] + 5  
                    char.vy = 0
                    char.isJumping = True

                #hit the lucky block
                elif platforms[i].block and char.vy <= 0 and char.y <= platforms[i].y + platforms[i].hitbox[3] and char.x + char.hitbox[2] >= platforms[i].x and char.x <= platforms[i].x + platforms[i].hitbox[2]:
                    char.y = platforms[i].y + platforms[i].hitbox[3] + 5
                    char.vy = 0
                    char.isJumping = True
                    platforms[i].hit = True
                    luckyblock_sound.play()
                    if i == 0:
                        pickup0.hit = True
                    elif i == 1:
                        pickup1.hit = True
                    elif i == 2:
                        pickup2.hit = True
 
                    
                #left side
                elif char.y + 5 <= platforms[i].y + platforms[i].hitbox[3] and char.y + char.hitbox[3] - 5 >= platforms[i].y and char.x + 32 >= platforms[i].x and char.x <= platforms[i].x - 5:
                    char.x = platforms[i].hitbox[0] - char.hitbox[2] - 2
                    char.vy += 1
                    char.vx = 6
                    
                #right side
                elif char.y + 5 <= platforms[i].y + platforms[i].hitbox[3] and char.y - 10 + char.hitbox[3] >= platforms[i].y and char.x <= platforms[i].x + platforms[i].hitbox[2] and char.x + 32 >= platforms[i].x + platforms[i].hitbox[2]:
                    char.x = platforms[i].hitbox[0] + platforms[i].hitbox[2] + 2
                    char.vy += 1
                    char.vx = 6

                #character is on top of the platform:

                elif char.vy > 0 and char.y + char.hitbox[3] <= platforms[i].y + 32:
                    char.y = platforms[i].y - char.hitbox[3] - 3
                    char.vy = 0
                    char.vx = vx
                    platforms[i].charOnPlatform = True
                    char.isJumping = False


        #When character goes out of the platform (on the x direction), jumping starts with vy=0 --> free fall
        if (char.x >= platforms[i].x + platforms[i].length * 32 or char.x + 34 <= platforms[i].x) and platforms[i].charOnPlatform:
            char.vy = 1
            char.outOfPlatform = True
            platforms[i].charOnPlatform = False

        if platforms[i].charOnPlatform == True and char.y + char.hitbox[3] <= platforms[i].y - 20:
            platforms[i].charOnPlatform = False

def processevents():
    global iswin, scene, pickup_count, wingametick,bg_count, losetime
    gamerunning = True
    char.isWalking = False
    clock.tick(fps)
    pg.event.pump()
    keys = pg.key.get_pressed()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            gamerunning = False
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            gamerunning = False
            
    if not iswin:
        elapsed_time, counter_time = timer(starting_time_game, losetime)
        printgametext(16, "TIME LEFT: " + str(counter_time) + " SECONDS", screen, 16, 460, (255,255,255))
        if int(elapsed_time) > losetime:
            gamerunning = False
            pg.mixer.music.stop()
            lose_sound.play()
            losescreen_funct()


    #Character colliding with the pick-up
    for i in pickups:
        if i.scene == scene:
            if pg.sprite.collide_rect(char,i) and i.y >= i.yf - 10:
                printgametext(10, "PRESS Z TO PICK UP", screen, char.x - 45, char.y - 40, (255,255,255))
                if keys[pg.K_z]:
                    pickup_sound.play()
                    pickups.remove(i)
                    pickups_sprite.remove(i)
                    all_sprites.remove(i)
                    pickup_count += 1

    #Character walks (left)
    if keys[pg.K_LEFT] or keys[pg.K_a]:
        if char.x < 5 and scene == 2:
            char.x = reso[0] - 5
            char.walk(d='left')
            scene = 1
        elif char.x < 5 and scene == 1:
            char.x = reso[0] - 5
            char.walk(d='left')
            scene = 0
        elif char.x >= 5:
            char.walk(d='left')


    #Character walks (right)
    if keys[pg.K_RIGHT] or keys[pg.K_d]:
        if char.x + char.hitbox[2] > reso[0] - 5 and scene == 0:
            char.x = 0
            char.walk(d='right')
            scene = 1
        elif char.x + char.hitbox[2] > reso[0] -5 and scene == 1:
            char.x = 0
            char.walk(d='right')
            scene = 2
        elif char.x + char.hitbox[2] < reso[0] - 5:
            char.walk(d='right')

       

                
    if keys[pg.K_m]:
        pickup_count = 3
        
    #Character jumps
    if not(char.isJumping) or char.outOfPlatform:
        if keys[pg.K_SPACE] or keys[pg.K_UP] or keys[pg.K_w]:
            char.vy = char.vy0
            jump_sound.play()
            char.outOfPlatform = False
            char.isJumping = True
    else:
        char.jump()

    #Finishing the game
    if airport.scene == scene:
        if pg.sprite.collide_rect(char,airport) and pickup_count == 3:
            printgametext(10, "PRESS Z TO SAVE THE WORLD", screen, char.x - 45, char.y - 40, (255,255,255))
            if keys[pg.K_z]:
                wingametick = pg.time.get_ticks()
                win_sound.play()
                pg.mixer.music.stop()
                bg_count = 1
                pickup_count += 1
                all_sprites.remove(bush_bad,wind_bad)
                all_sprites.add(bush_good1,bush_good2,bush_good3,bush_good4, wind_good, solar_panel)
                iswin = True
                
                
    if iswin:
        time_afterwin = timer(wingametick, 5)[0]
        if time_afterwin >= 5:
            gamerunning = False
            winscreen_funct()
    return gamerunning


def redrawScreeningame():        
    pg.display.flip()
    
    #background and sprites (except character)
    screen.blit(bg[bg_count],(0,0))
    all_sprites.update(scene)
    
    #Update and print character
    char.update() 

    if pickup_count == 0:
        printgametext(16, "0/3 PIECES COLLECTED", screen, 16, 490, (255,255,255))
    if pickup_count == 1:
        printgametext(16, "1/3 PIECES COLLECTED", screen, 16, 490, (255,255,255))
    if pickup_count == 2:
        printgametext(16, "2/3 PIECES COLLECTED", screen, 16, 490, (255,255,255))
    if pickup_count == 3:
        printgametext(16, "3/3 PIECES COLLECTED. GO TO THE AIRPORT TO SAVE TU DELFT", screen, 16, 490, (255,255,255))
    if pickup_count == 4:
        printgametext(16, "CONGRATS!! DELFTIE, YOU SAVED THE WORLD", screen, 16, 490, (255,255,255))





#       ***********************CLASSES***********************

class Char(pg.sprite.Sprite):
    
    def __init__(self,x,y,vx,vy,g,dt):
        pg.sprite.Sprite.__init__(self) #intialize Spritev
        self.x = x
        self.y = y
        self.y0 = y
        
        self.vx = vx
        self.vy = vy
        self.vy0 = vy
        
        self.g = g
        self.dt = dt
        
        self.imagelist = [load_image('data/sprites/delftie1.png', -1, 1)[0], load_image('data/sprites/delftie2.png', -1, 1)[0]]
        self.rect = load_image('data/sprites/delftie1.png')[1]
        self.image = self.imagelist[0]
        
        self.hitbox = (self.x, self.y, 32, 32)
        self.pos = (self.x,self.y)

        self.rect.x = x
        self.rect.y = y
        
        self.isWalking = False
        self.walkcount = 0
        self.isLeft = False
        self.isRight = False
        self.isJumping = False
        self.outOfPlatform = False
        self.fallcount = 0
        
    def update(self):
        self.pos = (int(self.x),int(self.y))
        self.hitbox = (int(self.x),int(self.y),32,32)
        self.rect.x = self.x
        self.rect.y = self.y

        if not self.isWalking:
            self.walkcount = 0
            if self.isLeft:
                self.image = self.imagelist[0]
            if self.isRight:
                self.image = pg.transform.flip(self.imagelist[0], True, False)

        if self.isWalking:
            if self.isLeft and 0 <= self.walkcount <= 15:
                self.image = self.imagelist[0]
            if self.isLeft and 15 < self.walkcount <= 30:
                self.image = self.imagelist[1]
            if self.isRight and 0 <= self.walkcount <= 15:
                self.image = pg.transform.flip(self.imagelist[0], True, False)
            if self.isRight and 15 < self.walkcount <= 30:
                self.image = pg.transform.flip(self.imagelist[1], True, False)

        if self.isJumping:
            if self.isLeft:
                self.image = self.imagelist[1]
            if self.isRight:
                self.image = pg.transform.flip(self.imagelist[1], True, False)
                
        if self.outOfPlatform:
            if self.fallcount < 15:
                self.fallcount += 1
                self.vy += self.g*self.dt
                self.y += self.vy*self.dt
            elif self.fallcount >= 15:
                self.fallcount = 0
                self.outOfPlatform = False
                self.isJumping = True

        screen.blit(self.image,self.pos)
    def walk(self, d):
        if d == 'right':
            self.x += self.vx*self.dt
            self.isRight = True
            self.isLeft = False
            self.isWalking = True
            if self.walkcount < 30:
                self.walkcount += 1
            if self.walkcount >=30:
                self.walkcount = 0
        elif d == 'left':
            self.x -= self.vx*self.dt
            self.isRight = False
            self.isLeft = True
            self.isWalking = True
            if self.walkcount < 30:
                self.walkcount += 1
            if self.walkcount >=30:
                self.walkcount = 0

    def jump(self):
        self.vy += self.g*self.dt
        self.y += self.vy*self.dt


class Platform(pg.sprite.Sprite):

    def __init__(self,x,y,length,name, scene, block = False):
        pg.sprite.Sprite.__init__(self) #intialize Sprite
        self.x = x
        self.y = y
        self.y0 = y
        self.length = length
        self.block = block
        
        self.image, self.rect = load_image(name, None)
        size = self.image.get_size()
        
        self.hitbox = (self.x,self.y,size[0]*self.length,size[1])
        
        self.charOnPlatform = False
        self.scene = scene

        self.vy0 = -8
        self.vy = self.vy0
        self.g = 1.5
        self.dt = 0.8
        self.hit = False
        
    def update(self,scene):
        pos = [self.x, self.y]
        if self.scene == scene:
            for i in range(self.length):
                screen.blit(self.image,pos)
                pos[0] += 32
        if self.hit:
            self.hit_funct()
            
    def hit_funct(self):
        if self.y <= self.y0 + 2:
            self.vy += self.g*self.dt
            self.y += self.vy*self.dt
        else:
            self.y = self.y0
            self.vy = self.vy0
            self.hit = False


class Pickup(pg.sprite.Sprite):
    
    def __init__(self,x,y,path, scene, y_final):
        pg.sprite.Sprite.__init__(self) #intialize Sprite
        self.image, self.rect = load_image(path,-1,0.5)
        self.rect.x = x
        self.rect.y = y


        self.x = x
        self.y = y
        self.yf = y_final

        self.scene = scene
        
        self.vy0 = -15
        self.vy = self.vy0
        self.g = 1
        self.dt = 0.8
        self.hit = False
        self.out = False
        
    def update(self, scene):
        self.rect.x = self.x
        self.rect.y = self.y
        
        if self.scene == scene and (self.out or self.hit):
            screen.blit(self.image,(self.x,self.y))
            
        if self.hit:
            self.popOut()


    def popOut(self):
        if not self.out:
            if self.y <= self.yf:
                self.vy += self.g*self.dt
                self.y += self.vy*self.dt
                self.x -= 2
            else:
                self.y = self.yf
                self.vy = self.vy0
                self.hit = False
                self.out = True

                
class Decoration(pg.sprite.Sprite):
    
    def __init__(self,x,y,path, scene, scale):
        pg.sprite.Sprite.__init__(self) #intialize Sprite
        self.image, self.rect = load_image(path,-1,scale)
        self.rect.x = x
        self.rect.y = y

        self.x = x
        self.y = y

        self.scene = scene
        
    def update(self, scene):
        self.rect.x = self.x
        self.rect.y = self.y
        
        if self.scene == scene:
            screen.blit(self.image,(self.x,self.y))
            
class Button():
    def __init__(self, x, y, name):
        self.image, self.rect = load_image(name, -1, 0.75)
        self.rect.center = (x,y)
        self.clicked = False

    def buttonclick(self):
        action = False
        #get mouse pos
        position = pg.mouse.get_pos()

        #check if on button, clicked
        if self.rect.collidepoint(position):
            if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False
        if self.clicked == True:
            action = True
        #draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action







#*****************SETUP***************************
#code to run once

#create screen
screen = pg.display.set_mode(reso)
screen_rect =  screen.get_rect()
pg.display.set_caption('Python Competition - Energy transition')

#initialize pyfont and mixer
pg.font.init()
pg.mixer.pre_init(44100, -16, 2, 256)
pg.mixer.init()

#load sounds
menubgm = pg.mixer.Sound('data/sounds/menu.mp3')
menubgm.set_volume(0.1)
jump_sound = pg.mixer.Sound('data/sounds/jumpsound.mp3')
luckyblock_sound = pg.mixer.Sound('data/sounds/luckyblock.wav')
pickup_sound = pg.mixer.Sound('data/sounds/pickupsound.wav')
click_sound = pg.mixer.Sound('data/sounds/click.wav')
win_sound = pg.mixer.Sound('data/sounds/win.wav')
lose_sound = pg.mixer.Sound('data/sounds/lose.wav')
bgm = pg.mixer.music.load('data/sounds/bgm.mp3')

#load logo, menubg and intro
logo, logo_rect = load_image('data/buttons/logo.png',-1,1.25)
menubg, menubg_rect = load_image('data/backgrounds/Menubg.png', None, 1)
intro, intro_rect = load_image('data/screens/intro.png', None, 1)
losescreen = load_image('data/screens/losescreen.png', None, 1)[0]
winscreen = load_image('data/screens/winscreen.png', None, 1)[0]

# load backgrounds
bg1, bg1_rect = load_image('data/backgrounds/bg_bad.png', None,0.5)
bg2, bg2_rect = load_image('data/backgrounds/bg_good.png', None, 0.5)
bg = [bg1,bg2]

#create platforms. arguments: (x,y,length,img path,scene). optional: block (only used for lucky blocks)
ground0 = Platform (0,444,37,'data/sprites/ground_small.png',0)
ground1 = Platform (0,444,37,'data/sprites/ground_small.png',1) #this is so unefficient omg askjdhsad
ground2 = Platform (0,444,37,'data/sprites/ground_small.png',2)

#Platforms for screen 1
platform0 = Platform(100,ground0.y - 128,5,'data/sprites/tile_00.png',0)
platform1 = Platform(400,ground0.y - 256,15,'data/sprites/tile_00.png',0)
platform2 = Platform(700,ground0.y - 330, 3, 'data/sprites/tile_00.png',0)

#Platforms for screen 2
platform3 = Platform(150,ground0.y - 270,23,'data/sprites/tile_00.png',1)
platform4 = Platform(400,ground0.y - 100,3,'data/sprites/tile_00.png',1)

#Platforms for screen 3
platform5 = Platform(60,ground0.y - 128,3,'data/sprites/tile_00.png',2)
platform6 = Platform(70,ground0.y - 300,4,'data/sprites/tile_00.png',2)
platform7 = Platform(150,ground0.y - 210,5,'data/sprites/tile_00.png',2)
platform8 = Platform(450,ground0.y - 350,7,'data/sprites/tile_00.png',2)
platform9 = Platform(700,ground0.y - 280,4,'data/sprites/tile_00.png',2)

#Lucky blocks
block1 = Platform(600, ground0.y - 350, 1, 'data/sprites/luckyblock.png', 0, True)
block2 = Platform(600, ground0.y - 380, 1, 'data/sprites/luckyblock.png', 1, True)
block3 = Platform(760, ground0.y - 360, 1, 'data/sprites/luckyblock.png', 2, True)

#create character. arguments: initial position (x,y), velocities (vx,vy), gravity and time step (both global vars)
char = Char(50, ground0.hitbox[1] - 34 , vx, vy, g,dt)
char_group = pg.sprite.Group()
char_group.add(char)

#Create pick-ups. Arguments: (x,y,img path, scene, y_final)
pickup0 = Pickup(block1.x + 5,block1.y + 5,'data/sprites/pickup0.png',0,platform1.y - 64)
pickup1 = Pickup(block2.x + 5,block2.y + 5,'data/sprites/pickup1.png',1,platform3.y - 64)
pickup2 = Pickup(block3.x,block3.y + 5,'data/sprites/pickup2.png',2,platform9.y - 64)

#Create decoration. Arguments: (x,y,img path, scene, scale)
airport = Decoration(400,175,'data/sprites/airport.png',2,0.27)
bush_bad = Decoration(500, ground0.y - 62, 'data/decoration/bush_bad.png',0, 1)
bush_good1 = Decoration(300, ground0.y - 62, 'data/decoration/bush_good.png',2, 1)
bush_good2 = Decoration(600, ground0.y - 62, 'data/decoration/bush_good.png',2, 1)
bush_good3 = Decoration(780, ground0.y - 62, 'data/decoration/bush_good.png',2, 1)
bush_good4 = Decoration(820, ground0.y - 62, 'data/decoration/bush_good.png',2, 1)
wind_bad = Decoration(750, ground0.y - 160, 'data/decoration/wind_bad1.png',2, 0.4)
wind_good = Decoration(780, ground0.y - 235, 'data/decoration/wind_good.png',2, 0.4)
solar_panel = Decoration(180, ground0.y - 165, 'data/decoration/solar_panel.png',2, 0.3)

#create button instance
startbutton = Button(480, 300, 'data/buttons/Play.png')
exitbutton = Button(480, 430, 'data/buttons/Exit.png')

#number of platforms. then makes a list with all heights and creates a list to check if character is on a platform
platforms = \
[block1, block2, block3, ground0, ground1, ground2,\
platform0, platform1, platform2,\
platform3, platform4, platform5,\
platform6, platform7, platform8, platform9]

nplatforms = len(platforms)
platforms_sprite = pg.sprite.Group()

#Loads platforms to sprite group
for i in range(nplatforms):
    platforms_sprite.add(platforms[i])

#Same but for pickups
pickups = [pickup0, pickup1, pickup2]
npickups = len(pickups)
pickups_sprite = pg.sprite.Group()
pickup_count = 0

for i in range(npickups):
    pickups_sprite.add(pickups[i])

#Same but for decoration
decoration = [airport, bush_bad, wind_bad]
ndecoration = len(decoration)
decoration_sprite = pg.sprite.Group()

for i in range(ndecoration):
    decoration_sprite.add(decoration[i])

all_sprites = pg.sprite.Group()
all_sprites.add(platforms_sprite)
all_sprites.add(pickups_sprite)
all_sprites.add(decoration_sprite)