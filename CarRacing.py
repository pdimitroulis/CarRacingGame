# Pantelis Dimitroulis
# CarRacing.py

import pygame
import ctypes
import time
import random
import winsound

# -- Initialization of pygame --
pygame.init()

# -- Play Soundtrack --
crash_sound = pygame.mixer.Sound("audio/Crash.wav")
pygame.mixer.music.load("audio/Root.wav")

# -- Variables Initialization --
display_width = 800 #Adjustable
display_height = 600 #Adjustable

car_width = 70 #width of carImg
car_height = 70 #height of carImg

# -- Set up colors --
black = (0,0,0)
white = (255,255,255)

dark_red = (150, 0, 0)
dark_green = (0, 150, 0)

bright_red = (255,0,0)
bright_green = (0, 255, 0)

# -- Set window --
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()

# -- Load images --
bg = pygame.image.load("images/road2.jpg")
bg2= pygame.image.load("images/road2.jpg")
carImg = pygame.image.load("images/racecar100.png")
blockImg = pygame.image.load("images/car1.png")

windowIcon = pygame.image.load("images/racecar20.png")

# -- Set window icon --
pygame.display.set_icon(windowIcon)

def blocks_dodged(count):
    font = pygame.font.SysFont("comicansms", 25)
    text = font.render("Dodged: "+str(count), True, white)
    gameDisplay.blit(text, (10,10))

def background(img, x, y):
    gameDisplay.blit(img, (x, y))

def updateCarPosition(x,y):
    gameDisplay.blit(carImg,(x,y))

def blocks(blockx, blocky, blockw, blockh, color):
    pygame.draw.rect(gameDisplay, color,[blockx, blocky, blockw, blockh])
    
def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def crashed():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(crash_sound)

    largeText = pygame.font.SysFont("comicansms", 115)
    TextSurf, TextRect = text_objects("You Crashed", largeText, black)
    TextRect.center = ((display_width/2),(display_height/3))
    gameDisplay.blit(TextSurf, TextRect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
                quit()

        button("Play again", 250, 450, 100, 50, bright_green, dark_green, "", game_loop)
        button("Quit", 450, 450, 100, 50, bright_red, dark_red, "", game_quit)

        pygame.display.update()
        clock.tick(15)

def button(msg, x, y, w, h, inactive_color, active_color,  action_msg, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, active_color, (x, y, w , h))
        if click[0] == 1:
            if action !=None:                   # GO and EXIT/QUIT button
                action()
            elif action_msg == "cont":          # Continue button
                return False
    else:
        pygame.draw.rect(gameDisplay, inactive_color, (x, y, w , h))

    smallText = pygame.font.SysFont("comicansms", 25)
    textSurf, textRect = text_objects(msg, smallText, black)
    textRect.center = (x+(w/2), y+(h/2))
    gameDisplay.blit(textSurf, textRect)
    return True

def paused():
    pygame.mixer.music.pause()

    largeText = pygame.font.SysFont("comicansms", 115)
    TextSurf, TextRect = text_objects("Car Crash", largeText, black)
    TextRect.center = ((display_width/2),(display_height/3))
    gameDisplay.blit(TextSurf, TextRect)

    flag_paused = True

    while flag_paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
                quit()

        flag_paused = button("Continue", 250, 450, 100, 50, bright_green, dark_green, "cont")    #create buttons
        button("Quit", 450, 450, 100, 50, bright_red, dark_red, "", game_quit)

        pygame.display.update()
        clock.tick(15)

    pygame.mixer.music.unpause()


def game_quit():
    pygame.quit()
    quit()

def game_intro():

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
                quit()
        gameDisplay.fill(white)
        largeText = pygame.font.SysFont("comicansms", 115)
        TextSurf, TextRect = text_objects("Car Crash", largeText, black)
        TextRect.center = ((display_width/2),(display_height/3))
        gameDisplay.blit(TextSurf, TextRect)

        button("GO!", 250, 450, 100, 50, bright_green, dark_green, "", game_loop)
        button("EXIT", 450, 450, 100, 50, bright_red, dark_red, "", game_quit)

        pygame.display.update()
        clock.tick(15)


def game_loop():
    pygame.mixer.music.play(-1)

    x = (display_width * 0.45)
    y = (display_height * 0.8)

    block_color = (200, 50, 100)

    x_change = 0

    bg_x = 0
    bg_y = 0
    bg2_x = 0
    bg2_y = -1360

    block_x = random.randrange(0, display_width)
    block_y = -600
    block_speed = 8
    block_width =  100
    block_height = 100

    blockCount = 1

    dodged = 0

    gameExit = False

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -10
                elif event.key == pygame.K_RIGHT:
                    x_change = 10
                elif event.key == pygame.K_ESCAPE:
                    paused()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change
        gameDisplay.fill(white)
        background(bg, bg_x, bg_y)
        background(bg2, bg2_x, bg2_y)

        blocks(block_x, block_y, block_width, block_height, block_color)
        block_y += block_speed
        bg_y += block_speed
        bg2_y += block_speed
        updateCarPosition(x,y)

        blocks_dodged(dodged)


        #-- display borders --
        if x > (display_width - car_width) or x < 0 :  #Remember x,y is the farthest left point of the car
            gameExit = True
            crashed()

        #-- spawn block --
        if block_y > display_height:
            block_y = 0 - block_height
            block_x = random.randrange(0, round(display_width - block_width))
            dodged += 1
            block_speed += 1
            block_height = random.randrange(70, 150)
            block_width = block_height
            block_color = (random.randrange(70, 255), random.randrange(70, 255), random.randrange(70, 255))

        #-- spawn background --
        if bg_y > 600:
            bg_y -= 1360*2
        elif bg2_y > 600:
            bg2_y -= 1360*2

        #-- block crash --
        if block_y + block_height >= y and (not (block_y > y + car_height)):
            if block_x + block_width >= x and (not (block_x > x + car_width)):
                gameExit = True
                crashed()

        pygame.display.update()
        clock.tick(60)

# -- Code flow --
game_intro()
