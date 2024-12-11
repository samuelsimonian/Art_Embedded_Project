#!/usr/bin/env python
from samplebase import SampleBase
from smbus2 import SMBus, i2c_msg
import time
from rgbmatrix import graphics
import random
import RPi.GPIO as GPIO

# I2C address of the sensor
address = 0x18 

# Constants for pressure calculation
MAXIMUM_PSI = 25
MINIMUM_PSI = 0
OUTPUT_MAX = 0xE66666
OUTPUT_MIN = 0x19999A

# GPIO pins
X_PIN = 24
Y_PIN = 25
START_PIN = 19
GPIO.setmode(GPIO.BCM) 

GPIO.setup(X_PIN, GPIO.IN)
GPIO.setup(Y_PIN, GPIO.IN)
GPIO.setup(START_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


bus = SMBus(1) 



def grass(self, counter):
    global level
    score = counter
    level = 0
    color = (255, 255, 0)
    for x in range (0, 32):
        for y in range (28, 32):
            self.matrix.SetPixel(x, y, 55, 148, 4)
    while counter >= 32:
        counter -= 32
        level += 1

    for x in range (0, 32):
        if level == 0:
            color = (255, 255, 0) # set color of level 0
        if level == 1:
            color = (255, 140, 0) # set color of level 1
            for y in range (28, 29):
                self.matrix.SetPixel(x, y, 255, 255, 0) # fill in level 0
        if level == 2:
            color = (255, 0, 0) # set color of level 2
            for y in range (28, 29):
                self.matrix.SetPixel(x, y, 255, 255, 0) # fill in level 0
            for y in range (29, 30):
                self.matrix.SetPixel(x, y, 255, 140, 0) # fill in level 1
        if level == 3:
            color = (255, 0, 255)
            for y in range (28, 29):
                self.matrix.SetPixel(x, y, 255, 255, 0) # fill in level 0
            for y in range (29, 30):
                self.matrix.SetPixel(x, y, 255, 140, 0) # fill in level 1
            for y in range (30, 31):
                self.matrix.SetPixel(x, y, 255, 0, 0) # fill in level 2
        if level == 4:
            you_win(score)
                
    for x in range (0, (counter % 32)):
        for y in range (28 + level, 29 + level):
            self.matrix.SetPixel(x, y, color[0], color[1], color[2])

def bird(self, y_dist, body, beak, foot):
    r_body, g_body, b_body = body
    r_beak, g_beak, b_beak = beak
    r_foot, g_foot, b_foot = foot
    self.matrix.SetPixel(1, y_dist + 1, r_body, g_body, b_body) # body
    self.matrix.SetPixel(1, y_dist , r_body, g_body, b_body) # body
    self.matrix.SetPixel(2, y_dist + 1, r_body, g_body, b_body) # body
    self.matrix.SetPixel(2, y_dist , r_body, g_body, b_body) # body
    self.matrix.SetPixel(3, y_dist + 1, r_beak, g_beak, b_beak) # beak
    self.matrix.SetPixel(4, y_dist + 1, r_beak, g_beak, b_beak) # beak
    self.matrix.SetPixel(2, y_dist + 2, r_foot, g_foot, b_foot) # foot
    self.matrix.SetPixel(3, y_dist , 227, 253, 218) # eye
    bird_x = [1, 2, 3, 4]
    bird_y = [y_dist, y_dist+1, y_dist+2]
    return bird_x, bird_y

def pipe(self, x_pos, mid_y, pipe_colors, level):
    pipe_x = []
    pipe_y = []
    r,g,b = pipe_colors
    for x in range (x_pos, x_pos + 6):
        pipe_x.append(x)
        if x in range (x_pos + 1, x_pos + 5):
            for y in range (0, mid_y - (6 - level)):
                # only append to pipe_y once
                if (x == x_pos + 2):
                    pipe_y.append(y)
                self.matrix.SetPixel(x, y, r, g, b)
            for y in range (mid_y + (6 - level), 29):
                # only append to pipe_y once
                if (x == x_pos + 2):
                    pipe_y.append(y)
                self.matrix.SetPixel(x, y, r, g, b)
        else:
            # make lip of pipe
            for y in range (mid_y - (8 - level), mid_y - (6 - level)):
                self.matrix.SetPixel(x, y, r, g, b)
            # make lip of pipe
            for y in range (mid_y + (6 - level), mid_y + (8 - level)):
                self.matrix.SetPixel(x, y, r, g, b)

        
    return pipe_x, pipe_y

def check(self, b_x, b_y, p_x, p_y):
    for i in b_x:
        for j in p_x:
            # if any x in bird corresponds with pipe x
            if i == j:
                for j in b_y:
                    for k in p_y:
                        # hit pipe
                        if j == k:
                            return True
    return False

def happy_face(self, offscreen_canvas, pos, f1, f2, hc):
    graphics.DrawText(offscreen_canvas, f1, pos - 32, 9, hc, ".  .  .  .  .  .  .  .  .  .  .  .  ")
    graphics.DrawText(offscreen_canvas, f1, pos - 32, 5, hc, ".  .  .  .  .  .  .  .  .  .  .  .  ")
    graphics.DrawText(offscreen_canvas, f2, pos - 28, 11, hc, ")  )  )  )  )  )  )  )  )  )  )  )  ")
    graphics.DrawText(offscreen_canvas, f1, pos - 32, 29, hc, ".  .  .  .  .  .  .  .  .  .  .  .  ")
    graphics.DrawText(offscreen_canvas, f1, pos - 32, 25, hc, ".  .  .  .  .  .  .  .  .  .  .  .  ")
    graphics.DrawText(offscreen_canvas, f2, pos - 28, 31, hc, ")  )  )  )  )  )  )  )  )  )  )  )  ")

def you_win(self, counter):
    offscreen_canvas = self.matrix.CreateFrameCanvas()
    # loading fonts
    font = graphics.Font()
    font.LoadFont("../../../fonts/7x13.bdf")
    font1 = graphics.Font()
    font1.LoadFont("../../../fonts/7x13.bdf")
    font2 = graphics.Font()
    font2.LoadFont("../../../fonts/7x13.bdf")
    # setting colors
    textColor = graphics.Color(255, 255, 255)
    happyColor = graphics.Color(0,255,0)

    pos = offscreen_canvas.width
    my_text = "YOU WIN! " + f" SCORE: {counter}"
    x = 1
    while (x > 0):
        offscreen_canvas.Clear()
        len = graphics.DrawText(offscreen_canvas, font, pos, 21, textColor, my_text)
        happy_face(self, offscreen_canvas, pos, font1, font2, happyColor)
        pos -= 1
        time.sleep(0.05)
        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
        x = pos + len
    menu(self)

def dead_face(self, offscreen_canvas, pos, f1, f2, dc):
    graphics.DrawText(offscreen_canvas, f1, pos - 32, 5, dc, "x  x  x  x  x  x  x  x  x  x  x  x  ")
    graphics.DrawText(offscreen_canvas, f1, pos - 32, 11, dc, "x  x  x  x  x  x  x  x  x  x  x  x  ")
    graphics.DrawText(offscreen_canvas, f1, pos - 32, 26, dc, "x  x  x  x  x  x  x  x  x  x  x  x  ")
    graphics.DrawText(offscreen_canvas, f1, pos - 32, 32, dc, "x  x  x  x  x  x  x  x  x  x  x  x  ")
    graphics.DrawText(offscreen_canvas, f2, pos - 26, 10, dc, "/  /  /  /  /  /  /  /  /  /  /  /  ")
    graphics.DrawText(offscreen_canvas, f2, pos - 26, 31, dc, "/  /  /  /  /  /  /  /  /  /  /  /  ")

def gg(self, counter):
    offscreen_canvas = self.matrix.CreateFrameCanvas()
    # loading fonts
    font = graphics.Font()
    font.LoadFont("../../../fonts/7x13.bdf")
    font1 = graphics.Font()
    font1.LoadFont("../../../fonts/6x12.bdf")
    font2 = graphics.Font()
    font2.LoadFont("../../../fonts/6x13.bdf")
    # setting colors
    textColor = graphics.Color(255, 255, 255)
    deadColor = graphics.Color(216,0,0)

    pos = offscreen_canvas.width
    my_text = "GAME OVER! " + f" SCORE- {counter}"
    x = 1
    while (x > 0):
        offscreen_canvas.Clear()
        len = graphics.DrawText(offscreen_canvas, font, pos, 20, textColor, my_text)

        dead_face(self, offscreen_canvas, pos, font1, font2, deadColor)
        pos -= 1
        time.sleep(0.05)
        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
        x = pos + len
    menu(self)
    
def bird_math(x1, x2, y1, y2, change):
    x1 = x1 + 1
    x2 = x2 + 1
    y1 += change
    if y1 > 3:
        change = -1
    if y1 < 1:
        change = 1
    y2 = 4 - y1
    return x1, x2, y1, y2, change

def menu(self):
    offscreen_canvas = self.matrix.CreateFrameCanvas()
    font = graphics.Font()
    font.LoadFont("../../../fonts/4x6.bdf")
    font2 = graphics.Font()
    font2.LoadFont("../../../fonts/6x10.bdf")
    textColor = graphics.Color(255, 255, 255)
    pos = offscreen_canvas.width
    my_text = "PRESS START TO PLAY"
    my_text2 = " FLAPPY BIRD"
    # variables
    x1 = 0
    y1 = 0
    x2 = 16
    y2 = 4
    change = 1
    c = 0
    while (GPIO.input(START_PIN) == GPIO.HIGH):
        c += 1
        if (c % 3 == 0):
            x1, x2, y1, y2, change = bird_math(x1, x2, y1, y2, change)
        drawbird(self, x1, y1)
        drawbird(self, x1, y1 + 22)
        drawbird(self, x2, y2 + 22)
        drawbird(self, x2, y2)
        offscreen_canvas.Clear()
        len = graphics.DrawText(offscreen_canvas, font, pos, 22, textColor, my_text)
        len2 = graphics.DrawText(offscreen_canvas, font2, pos, 17, graphics.Color(255,255,0), my_text2)
        pos -= 1
        if (pos + len < 0):
            pos = offscreen_canvas.width
        time.sleep(0.05)
        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
    time.sleep(0.2)

def drawbird(self, x, y):
    # body
    for i in range (x, x + 4):
        for j in range(y, y + 4):
            while i > 31:
                i -= 32
            self.matrix.SetPixel(i, j, 213, 195, 0)
    # beak
    for i in range (x + 4, x + 8):
        for j in range (y + 2, y + 4):
            while i > 31:
                i -= 32
            self.matrix.SetPixel(i, j, 255, 77, 68)
    # foot
    for i in range (x + 2, x + 4):
        for j in range (y + 4, y + 6):
            while i > 31:
                i -= 32
            self.matrix.SetPixel(i, j, 246, 131, 11)
    # eye
    for i in range (x + 4, x + 6):
        for j in range (y, y + 2):
            while i > 31:
                i -= 32
            self.matrix.SetPixel(i, j, 227, 253, 218)

global level
level = 0

class GrayscaleBlock(SampleBase):
    def __init__(self, *args, **kwargs):
        super(GrayscaleBlock, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Game over!")
        

    def run(self):
        max_brightness = self.matrix.brightness # set to 100
        count = 0
        c = 255
        self.matrix.brightness = 60

        # variables
        x_pos = 35
        mid_y = random.randint(9, 19)
        speed = 1
        counter = 0
        plus = 0
        n = 0

        menu(self)
        while (True):
            if (GPIO.input(START_PIN) == GPIO.LOW):
                time.sleep(0.2)
                menu(self)
            time.sleep(0.1)
            write = i2c_msg.write(address, [0xAA,0x00,0x00])
            read = i2c_msg.read(address, 4)
            bus.i2c_rdwr(write, read)
            data = list(read)
            reading = data[1] << 16 | data[2] << 8 | data[3]
            pressure = (reading - OUTPUT_MIN) * (MAXIMUM_PSI - MINIMUM_PSI)
            pressure = (pressure / (OUTPUT_MAX - OUTPUT_MIN)) + MINIMUM_PSI
            #print("Pressure:", pressure)
            # between 6 and 25, usually 14
            percent = ((pressure - 16)/10) # should bottom out when untouched
            #print("Percent:", percent * 100)

            y_dist = int(32 * (1-percent))
            #print(y_dist)
            if y_dist < 0:
                y_dist = 0
            if y_dist > 25:
                y_dist = 25

            # sky
            self.matrix.Fill(63, 108 , 113)

            # move pipe to the left
            x_pos -= speed
            if x_pos < -4:
                # max speed is 8
                if speed < (level + 1) * 2:
                    plus = int(random.uniform(0.16,1.16))
                else:
                    plus = 0
                speed += plus
                mid_y = random.randint(9, 19)
                x_pos = 35
                counter += 1


            
            # slow down blinking
            n += 1
            if plus == 1 and (n%3 == 0):
                # speed up
                body = [42, 60, 255]
                beak = [189, 33, 255]
                foot = [42, 226, 255]
                pipe_colors = [255, 172, 60]
            else:
                # normal
                body = [213, 195, 0]
                beak = [255, 77, 68]
                foot = [246, 131, 11]
                pipe_colors = [55, 195, 0]
            
            # display objects
            pipe_x, pipe_y = pipe(self, x_pos, mid_y, pipe_colors, level)
            bird_x, bird_y = bird(self, y_dist, body, beak, foot)
            grass(self, counter)

            # did bird hit pipe?
            if check(self, bird_x, bird_y, pipe_x, pipe_y):
                self.matrix.Fill(0,0,0)
                time.sleep(0.05)
                gg(self, counter)
                # reset variables
                x_pos = 35
                speed = 1
                counter = 0 


# Main function
if __name__ == "__main__":
    grayscale_block = GrayscaleBlock()
    if (not grayscale_block.process()):
        grayscale_block.print_help()
