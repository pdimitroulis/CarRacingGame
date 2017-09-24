import pygame
import ctypes
import time
import random
import winsound

pygame.init()

#Play soundtrack
winsound.PlaySound('audio/soundtrack2.wav', winsound.SND_LOOP | winsound.SND_ASYNC) #two flags for nonstop playing

display_width = 800 #Adjustable
display_height = 600 #Adjustable

car_width = 70 #from image_size
car_height = 70 #from image_size

black = (0,0,0)
white = (255,255,255)

red = (150, 0, 0)
green = (0, 150, 0)

bright_red = (255,0,0)
bright_green = (0, 255, 0)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()

bg = pygame.image.load("images/road2.jpg")
bg2= pygame.image.load("images/road2.jpg")
carImg = pygame.image.load("images/racecar100.png")

def things_dodged(count):
    font = pygame.font.SysFont("comicansms", 25)
    text = font.render("Dodged: "+str(count), True, white)
    gameDisplay.blit(text, (10,10))

def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color,[thingx, thingy, thingw, thingh])

def background(img, x, y):
    gameDisplay.blit(img, (x, y))

def car(x,y):
    gameDisplay.blit(carImg,(x,y))

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_display(text, color):
    largeText = pygame.font.SysFont("comicansms",115)
    TextSurf, TextRect = text_objects(text, largeText, color)
    TextRect.center = ((display_width/2),(display_height/3))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(2)
    game_loop()

def crash():
    message_display('You crashed', white)

def button(msg, x, y, w, h, inact_color, act_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, act_color, (x, y, w , h))
        if click[0] == 1 and action !=None:
            action()
    else:
        pygame.draw.rect(gameDisplay, inact_color, (x, y, w , h))

    smallText = pygame.font.SysFont("comicansms", 20)
    textSurf, textRect = text_objects(msg, smallText, black)
    textRect.center = (x+(w/2), y+(h/2))
    gameDisplay.blit(textSurf, textRect)

def game_quit():
    pygame.quit()
    quit()

def game_intro():

    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
                quit()
        gameDisplay.fill(white)
        largeText = pygame.font.SysFont("comicansms", 115)
        TextSurf, TextRect = text_objects("Car Crash", largeText, black)
        TextRect.center = ((display_width/2),(display_height/3))
        gameDisplay.blit(TextSurf, TextRect)

        button("GO!", 250, 450, 100, 50, bright_green, green, game_loop)
        button("EXIT", 450, 450, 100, 50, bright_red, red, game_quit)

        pygame.display.update()
        clock.tick(15)

def game_loop():
    x = (display_width * 0.45)
    y = (display_height * 0.8)

    block_color = (200, 50, 100)

    x_change = 0

    bg_x = 0
    bg_y = 0
    bg2_x = 0
    bg2_y = -1360

    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 4
    thing_width =  100
    thing_height = 100

    thingCount = 1

    dodged = 0

    gameExit = False

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change
        gameDisplay.fill(white)
        background(bg, bg_x, bg_y)
        background(bg2, bg2_x, bg2_y)

        things(thing_startx, thing_starty, thing_width, thing_height, block_color)
        thing_starty += thing_speed
        bg_y += thing_speed
        bg2_y += thing_speed
        car(x,y)

        things_dodged(dodged)


        #--display borders--
        if x > (display_width - car_width) or x < 0 :  #x,y is the farthest left point of the car
            gameExit = True
            crash()

        #--spawn thing--
        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, round(display_width - thing_width))
            dodged += 1
            thing_speed += 1
            thing_height += (dodged * 1.5)
            block_color = random.randrange(0, 255)

        #--spawn background --
        if bg_y > 600:
            bg_y = 600 - 1360 - 1360
        elif bg2_y > 600:
            bg2_y = 600 -1360 - 1360

        #--thing crash--
        if thing_starty + thing_height >= y and (not (thing_starty > y + car_height)):
            if thing_startx + thing_width >= x and (not (thing_startx > x + car_width)):
                gameExit = True
                crash()

        pygame.display.update()
        clock.tick(60)

game_intro()
