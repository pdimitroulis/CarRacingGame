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
red = (255,0,0)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()

carImg = pygame.image.load('images/racecar100.png')

def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: "+str(count), True, black)
    gameDisplay.blit(text, (0,0))

def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color,[thingx, thingy, thingw, thingh])

def car(x,y):
    gameDisplay.blit(carImg,(x,y))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/3))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(2)
    game_loop()

def crash():
    message_display('You crashed')


def game_loop():
    x = (display_width * 0.45)
    y = (display_height * 0.8)

    block_color = (200, 50, 100)

    x_change = 0

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

        things(thing_startx, thing_starty, thing_width, thing_height, block_color)
        thing_starty += thing_speed
        car(x,y)
        things_dodged(dodged)


        #--display borders--
        if x > (display_width - car_width) or x < 0 :
            gameExit = True
            crash()

        #--spawn thing--
        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, display_width)
            dodged += 1
            thing_speed += 1
            thing_width += (dodged * 1.3)
            block_color = random.randrange(0, 255)

        #--thing crash--
        if thing_starty + thing_height >= y and (not (thing_starty > y + car_height)):
            if thing_startx + thing_width >= x and (not (thing_startx > x + car_width)):
                gameExit = True
                crash()

        pygame.display.update()
        clock.tick(60)


game_loop()
pygame.quit()
quit()
