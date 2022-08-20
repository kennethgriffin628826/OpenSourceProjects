import pygame, sys, serial, time
# https://roboticsbackend.com/raspberry-pi-arduino-serial-communication/     # use an arduino as the A/D converter to the raspberry pi through USB
pygame.init()
window = pygame.display.set_mode((1024,600)) #pygame.FULLSCREEN
pygame.display.set_caption("383 Stroker")
background = pygame.image.load('background.png')
BG2 = pygame.image.load('background2.png')
font = pygame.font.SysFont('arial', 100)
smfont = pygame.font.SysFont('arial', 30)
lgfont = pygame.font.SysFont('comicsansmss',150)
window.fill((0,0,0))
color = (255,255,255)
try: # Try to connect to arduino. analog data ranges from 0 to 1023
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1) # Serial device name for the Arduino: usually ‘/dev/ttyACM0’, ‘/dev/ttyUSB0’, or similar.
    ser.reset_input_buffer()
except:
    ser = "error"
    print("error: no communication to Arduino")

def getData():
    try:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip() # get the string of data
    except:
        line= "000 0000" # this is the default speed and RPM that will show if no communication from arduino # speed RPM
    speed = int(line[0:3])
    RPM = int(line[4:8])
    return(speed, RPM)

def drawSpeed(color, speed):
    text = lgfont.render(str(speed), True, color)
    mph = smfont.render("MPH",True,color)
    tx = 440
    if speed < 10:
        tx = 470
    window.blit(text,(tx,400))
    window.blit(mph,(470,515))

def drawRPM(color, RPM):
    textrpm = smfont.render("RPM",True,color)
    window.blit(textrpm,(10,50))
    window.blit(textrpm,(470,250))
    numrpm = lgfont.render(str(RPM),True,color)
    tx = 375
    if RPM < 100:
        tx = 470
    elif RPM < 1000:
        tx = 400
    window.blit(numrpm,(tx,150))
    bars = int(RPM/100/2)
    x = 100
    barcolor = (255,255,255)
    for i in range(bars):
        if i > 25:
            if i > 30:
                barcolor = (255,0,0)# red bars at max RPM
            else:
                barcolor = (255,255,0)# make yellow bars for getting close to max RPM
        pygame.draw.rect(window,barcolor,[x,20,15,100])#(drawSurface,color,position and shape, border thickness)
        x = x + 20

def changeColor(color,change):
    listColor = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(0,255,255),(255,255,255),(0,0,0)]
    if change == True:
        position = 0
        for i in range(len(listColor)):
            if color == listColor[i]:
                if i == 0:
                    color = listColor[6]
                color = listColor[i-1]
    return(color)

def getKeyPresses():
    change = False
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q: # if letter e is pressed
                sys.exit()
            elif event.key == pygame.K_SPACE : # if space bar is pressed change color
                change = True
        if event.type == pygame.QUIT: # if x button on window pressed
            sys.exit()
    return(change)

for i in range(75):
    background.set_alpha(i)
    window.blit(background, [0,0])
    time.sleep(.015)
    pygame.display.update()
while True:
    speed, RPM = getData()
    window.fill((0,0,0))
    window.blit(BG2,[0,0])
    drawRPM(color, RPM)
    drawSpeed(color, speed)
    change = getKeyPresses()
    color = changeColor(color, change)
    pygame.display.update()
